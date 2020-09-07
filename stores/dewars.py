import time
import logging

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

import requests

from ispyb_api import controller
from .destinations import EBIC, MX, I14 SCM

api = Blueprint('stores', __name__, url_prefix='/api/stores')


@api.route('/dewars', methods=['GET', 'POST'])
def location():
    """
    Main method that returns a list of dewars that are stores in/out.
    Destination if either derived from rules based on barcode prefix (for stores-in)
    or from the return lab contact address (if stores-out)
    """
    result = {}
    status_code = 200

    if request.method == 'GET':
        try:
            result = controller.find_dewar_history_for_locations(['STORES-IN', 'STORES-OUT'], max_entries=50)
            # Append the destination to the results
            # It's not stored in the database so we determine it here based on barcode or lab contact address
            for key in result.keys():
                dewar = result[key]
                if dewar['storageLocation'].upper() == 'STORES-IN':
                    dewar['destination'] = get_destination_from_barcode(dewar['barcode'])
                elif dewar['storageLocation'].upper() == 'STORES-OUT':
                    shipping = controller.get_shipping_return_address(dewar['barcode'])
                    # Depending on how the address is filled out we may not have a city field
                    # Should have a country but checking just in case
                    if shipping:
                        city = shipping['city'] if shipping['city'] else ''
                        country = shipping['country'] if shipping['country'] else ''

                        if city:
                            dewar['destination'] = ', '.join([city, country])
                        else:
                            dewar['destination'] = country
                else:
                    dewar['destination'] = ''
        except AttributeError:
            logging.getLogger('ispyb-logistics').warning('No dewar history found for stores locations')

    elif request.method == 'POST':
        location = request.form['location']
        barcode = request.form['barcode']
        awb = request.form['awb']

        if location and barcode:
            result, status_code = update_dewar_location(barcode, location, awb)
        else:
            logging.getLogger('ispyb-logistics').warning('Warning barcode and/or location not set, ignoring request.')

            result = {'location': location,
                      'barcode': barcode,
                      'awb': awb,
                      'status': 'fail - location and/or barcode not set',
                      }
            status_code = 400

    response = jsonify(result)
    response.status_code = status_code

    return response

# Currently only working for DHL but could be extended...
@api.route('/dewars/courier/destination', methods=["GET"])
def destination():
    awb = request.args.get('awb')
    url = 'https://www.dhl.com/shipmentTracking?AWB={}'.format(awb)

    result = {}
    status_code = 200

    try:
        # Added timeout to request
        r = requests.get(url, timeout=5)

        if r.status_code == requests.codes.ok:
            data = r.json()
            result = data['results'][0]['destination']
            logging.getLogger('ispyb-logistics').info("Got Destination from DHL {}".format(result))
        else:
            logging.getLogger('ispyb-logistics').error("Error getting dewar destination from DHL {} {}".format(r.status_code, r.text))
            status_code = 404

    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to contact DHL")
        status_code = 404
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to contact DHL")
        status_code = 500

    response = jsonify(result)
    response.status_code = status_code

    return response


def update_dewar_location(barcode, location, awb=None):
    """
    Update the records for this dewar

    If it gets here we have already tested that the barcode and location are ok.
    """
    status_code = 200

    if awb:
        awb = awb.replace('+', '_')

    result = controller.set_location(barcode, location, awb)

    if result is None:
        result = {'location': location,
                  'barcode': barcode,
                  'awb': awb,
                  'status': 'fail - controller did not set location',
                  }
        status_code = 400

    return result, status_code

def get_destination_from_barcode(barcode):
    """
    Given a barcode (prefix) determine the destination.

    Call this method when the location is STORES-IN to help identify where it should go
    """
    destination = None

    try:
        barcode_prefix = barcode.upper()[0:2]

        if barcode_prefix in I14.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in I14.instruments):
            destination = I14.destination
        elif barcode_prefix in EBIC.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in EBIC.instruments):
            destination = EBIC.destination
        elif barcode_prefix in MX.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in MX.instruments):
            destination = MX.destination
        elif barcode_prefix in SCM.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in SCM.instruments):
            destination = SCM.destination
        else:
            # Try to derive the destination from proposal type
            session = controller.get_instrument_from_dewar(barcode)

            instrument = session.get('instrument', '').upper()

            if instrument in EBIC.instruments:
                destination = EBIC.destination
            elif instrument in MX.instruments:
                destination = MX.destination
            elif instrument in I14.instruments:
                destination = I14.destination
            elif instrument in SCM.instruments:
                destination = SCM.destination
            else:
                destination = 'Unknown'
    except:
        logging.getLogger('ispyb-logistics').error('Could not get destination from barcode {}'.format(barcode))

    return destination
