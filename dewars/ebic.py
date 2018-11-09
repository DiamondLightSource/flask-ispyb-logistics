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

rack_prefix = 'EBIC-RACK'

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
                 ]

rack_locations = ['-'.join([rack_prefix, suffix])
                    for suffix in rack_suffixes]

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

ebic_locations = ['EBIC-IN-{}'.format(i) for i in range(10,1)]

"""
App to demonstrate use of vuejs
"""
@api.route('/vdewars')
def vdewars():
    return render_template('vue-dewars.html', title='Zone6 Dewars', api_prefix='zone6', rack_locations=rack_locations)


@api.route('/')
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
        result = controller.find_dewars_by_location(rack_locations)

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

    return jsonify(result), status_code

@api.route('/dewars/find', methods=['GET'])
def find():
    """
    Return a list of matching dewars with this facility code

    Should be requested with parameters in the URL ?fc=DLS-MS-1234 request
    We specifically return the status code so the front end can show feedback
    """
    facilitycode = request.args.get('fc')

    result, status_code = common.find_dewar(facilitycode)

    return jsonify(result), status_code
