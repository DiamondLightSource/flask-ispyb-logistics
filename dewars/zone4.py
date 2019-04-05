# System imports
from datetime import datetime
import time
import json
import logging

# Package imports
from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

# Local imports
import common

api = Blueprint('zone4', __name__, url_prefix='/zone4')

rack_prefix = 'TRAY'

rack_suffixes = ['1A', '2A', '3A', '4A', '5A', '6A',
                 '1B', '2B', '3B', '4B', '5B', '6B',
                 '1C', '2C', '3C', '4C', '5C', '6C',
                 '1D', '2D', '3D', '4D', '5D', '6D',
                 '1E', '2E', '3E', '4E', '5E', '6E',
                 '1F', '2F', '3F', '4F', '5F', '6F',
                 ]

rack_locations = ['-'.join([rack_prefix, suffix])
                    for suffix in rack_suffixes]

beamline_locations = ['I03',
                      'I04',
                      'I04-1',
                      'I19',
                      'I24',
                      'USER-COLLECTION',
                      'STORES-OUT',
                      'EBIC'
                      ]

"""
App to demonstrate use of vuejs
"""
@api.route('/')
def vdewars():
    return render_template('vue-dewars.html',
                            title='Zone4 Dewars',
                            api_prefix='zone4',
                            rack_locations=rack_locations,
                            beamline_locations=beamline_locations)

@api.route('/dewars', methods=['GET', 'POST', 'DELETE'])
def location():
    """
    API route for dewar management
    """
    result = {}
    status_code = 200

    if request.method == 'GET':
        # Get any dewar with any rack location
        # There should only be one per location
        # Simple call so use controller directly
        result, status_code = common.find_dewars_by_location(rack_locations)

    elif request.method == 'POST':
        location = request.form['location']
        barcode = request.form['barcode']

        result, status_code = common.update_dewar_location(barcode, location)

    elif request.method == 'DELETE':
        try:
            location = request.form['location']
        except KeyError:
            # No form data (used axios?) Try params
            location = request.args.get('location')

        result, status_code = common.remove_dewar_from_location(location)
    else:
        result = {'location': '',
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'Method/route not implemented yet'}
        status_code = 501

    response = jsonify(result)
    response.status_code = status_code

    return response


@api.route('/dewars/find', methods=['GET'])
def find():
    """
    Return a list of matching dewars with this facility code

    Should be requested with parameters in the URL ?fc=DLS-MS-1234 request
    We specifically return the status code so the front end can show feedback
    """
    facilitycode = request.args.get('fc')

    # We actually accept a dewar barcode or a facility code.
    # The controller handles both instances...
    result, status_code = common.find_dewar_history(facilitycode)

    response = jsonify(result)
    response.status_code = status_code

    return response
