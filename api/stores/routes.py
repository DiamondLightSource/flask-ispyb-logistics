import time
import logging
import os

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

from api.ispyb_api import controller
from . import destinations

api = Blueprint('stores', __name__, url_prefix='/api/stores')

def _read_secret(path):
    p = Path(path)
    if p.is_file():
        try:
            return p.read_text(encoding='utf-8').strip()
        except OSError as e:
            logging.getLogger('ispyb-logistics').error(f'Error reading secret file {path}: {e}')
            return default
    return default

SHIPPING_SERVICE_HOST = _read_secret('/secrets/shipping-service/host')
SHIPPING_SERVICE_USERNAME = _read_secret('/secrets/shipping-service/username')
SHIPPING_SERVICE_PASSWORD = _read_secret('/secrets/shipping-service/password')


def get_awb_from_shipping_service(shipmentRequestId):
    if not SHIPPING_SERVICE_HOST or not SHIPPING_SERVICE_USERNAME or not SHIPPING_SERVICE_PASSWORD:
        return ''
    try:
        basic = HTTPBasicAuth(SHIPPING_SERVICE_USERNAME, SHIPPING_SERVICE_PASSWORD)
        url = f'{SHIPPING_SERVICE_HOST}/api/shipment_requests/{shipmentRequestId}/shipments/FROM_FACILITY'
        r = requests.get(url, auth=basic, timeout=5)
        r.raise_for_status()
        j = r.json()
        return j.get('tracking_number', '')
    except Exception as e:
        logging.getLogger('ispyb-logistics').error(f'Failed to fetch AWB for request {shipmentRequestId}: {e}')
        return ''


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
            page = request.args.get('page', default=1, type=int)
            result = controller.find_dewar_history_for_locations(['STORES-IN', 'STORES-OUT'], per_page=50, page=page)
            # Append the destination to the results
            # It's not stored in the database so we determine it here based on barcode or lab contact address
            for key in result.keys():
                dewar = result[key]
                dewar['shippingServiceAWB'] = ''
                if dewar['storageLocation'].upper() == 'STORES-IN':
                    dewar['destination'] = get_destination_from_barcode(dewar['barcode'])
                elif dewar['storageLocation'].upper() == 'STORES-OUT':
                    dewar['shippingServiceAWB'] = get_awb_from_shipping_service(dewar['externalShippingIdFromSynchrotron'])
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
    url = 'https://api-eu.dhl.com/track/shipments?trackingNumber={}'.format(awb)
    dhl_key = os.environ.get('DHL_KEY', 'demo-key')
    headers = {'DHL-API-Key': dhl_key}

    result = {}
    status_code = 200

    try:
        # Added timeout to request
        r = requests.get(url, timeout=5, headers=headers)

        if r.status_code == requests.codes.ok:
            data = r.json()
            result = data['shipments'][0]['destination']
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
        destination = destinations.get_destination_from_barcode(barcode)
        if destination == 'Unknown':
            # Try to derive the destination from proposal type
            session = controller.get_instrument_from_dewar(barcode)
            instrument = session.get('instrument', '').upper()
            destination = destinations.get_destination_from_instrument(instrument)
    except:
        logging.getLogger('ispyb-logistics').error('Could not get destination from barcode {}'.format(barcode))

    return destination
