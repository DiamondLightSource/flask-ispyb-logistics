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

api = Blueprint('zone6', __name__, url_prefix='/zone6')

rack_prefix = 'RACK'

rack_suffixes = ['A1', 'A2', 'A3', 'A4',
                 'B1', 'B2', 'B3', 'B4',
                 'C1', 'C2', 'C3', 'C4',
                 'D1', 'D2', 'D3', 'D4',
                 'E1', 'E2', 'E3', 'E4',
                 'F1', 'F2', 'F3', 'F4',
                 'G1', 'G2', 'G3', 'G4',
                 'H1', 'H2', 'H3', 'H4',
                 'J1', 'J2', 'J3', 'J4',
                 'K1', 'K2', 'K3', 'K4',
                 'L1', 'L2', 'L3', 'L4',
                 'M1', 'M2', 'M3', 'M4',
                 'N1', 'N2', 'N3', 'N4',
                 'P1', 'P2', 'P3', 'P4',
                 'Q1', 'Q2', 'Q3', 'Q4',
                 'R1', 'R2', 'R3', 'R4',
                 'X1', 'X2', 'X3', 'X4',
                 'X5', 'X6', 'X7', 'X8',
                 'X9', 'X10', 'X11', 'X12',
                 ]

rack_locations = ['-'.join([rack_prefix, suffix])
                    for suffix in rack_suffixes]

beamlines = ['i03',
             'i04',
             'i04-1',
             'i24',
             ]

beamline_prefix = 'BEAMLINE'

beamline_locations = ['{}-{}'.format(beamline_prefix, x.upper()) for x in beamlines]

beamline_locations.extend(['USER-COLLECTION',
                           'STORES-OUT',
                           'ZONE-6-STORE',
                           ])

"""
App to demonstrate use of vuejs
"""
@api.route('/')
def vdewars():
    return render_template('vue-dewars.html', title='Zone6 Dewars', api_prefix='zone6', rack_locations=rack_locations)

@api.route('/original')
def index():
    """
    Main page for dewar management
    """
    return render_template('dewars.html',
                           title='zone6 Dewar Management',
                           rack_locations=rack_locations,
                           rack_suffixes=rack_suffixes,
                           rack_prefix=rack_prefix,
                           beamlines=beamline_locations,
                           api_prefix='zone6',
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
