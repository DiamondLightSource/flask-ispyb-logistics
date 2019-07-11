import time
import logging

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

from ispyb_api import controller

api = Blueprint('stores', __name__, url_prefix='/api/stores')


"""
Route for vue.js version
"""
# @api.route('/')
# def vstores():
#     return render_template('vue-stores.html', api_prefix='stores')

# @api.route('/original')
# def index():
#     """
#     Main page for dewar management
#     """
#     return render_template('stores.html',
#                            title='Stores Dewar Management',
#                            api_prefix='stores',
#                            max_dewar_history=20
#                            )


@api.route('/dewars', methods=['GET', 'POST'])
def location():
    result = {}
    status_code = 200

    if request.method == 'GET':
        result = controller.find_dewar_history_for_locations(['STORES-IN', 'STORES-OUT'], max_entries=20)
        # Append the destination to the results
        # Its not stored in the database so we determine it here based on barcode
        # Only relevant for incoming dewars though (stores-in)
        for key in result.keys():
            dewar = result[key]
            if dewar['inout'].upper() == 'STORES-IN':
                dewar['destination'] = get_destination_from_barcode(dewar['barcode'])
            else:
                dewar['destination'] = ''

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

        if barcode_prefix == 'SP' or 'I14' in barcode.upper():
            destination = 'I14'
        elif barcode_prefix == 'EM' or barcode_prefix == 'BI' or any(b in barcode.upper() for b in ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07']):
            destination = 'eBIC'
        elif barcode_prefix == 'MX' or any(b in barcode.upper() for b in ['I03', 'I04', 'I19', 'I23', 'I24']):
            destination = 'Zone 6 store'
        else:
            destination = 'Unknown'
    except:
        logging.getLogger('ispyb-logistics').error('Could not get destination from barcode {}'.format(barcode))

    return destination
