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
from ispyb_api import controller

api = Blueprint('ebic', __name__, url_prefix='/ebic')

# Build list of rack locations e.g. EBIC-IN-[1..10]
in_racks = ['EBIC-IN-{}'.format(i) for i in range(1,11)]
out_racks = ['EBIC-OUT-{}'.format(i) for i in range(1,11)]

rack_locations = in_racks + out_racks

beamlines = ['m01',
             'm02',
             'm03',
             'm04',
             'm05',
             'm06',
             'm07',
            ]

beamline_prefix = 'MICROSCOPE'

beamline_locations = ['{}-{}'.format(beamline_prefix, x.upper()) for x in beamlines]

# Add the common locations on for the web ui
beamline_locations.extend(['USER-COLLECTION',
                           'STORES-OUT',
                           'ZONE-6-STORE',
                           ])


"""
App to demonstrate use of vuejs
"""
@api.route('/')
def vdewars():
    return render_template('vue-dewars.html', title='eBIC Dewars', api_prefix='ebic', rack_locations=rack_locations)


@api.route('/original')
def index():
    """
    Main page for dewar management
    """
    return render_template('dewars.html',
                           title='eBIC Dewar Management',
                           rack_locations=rack_locations,
                           rack_suffixes=rack_suffixes,
                           rack_prefix=rack_prefix,
                           beamlines=beamline_locations,
                           api_prefix='ebic',
                           )


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
        location = request.form['location']

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

    result, status_code = common.find_dewar(facilitycode)

    response = jsonify(result)
    response.status_code = status_code

    return response
