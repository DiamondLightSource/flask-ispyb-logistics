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
from flask import make_response

# Local imports
from . import common

from . import ebic
from . import zone4
from . import zone6
from . import cage
from . import i19

locations = {'zone6': zone6.rack_locations,
             'zone4': zone4.rack_locations,
             'ebic': ebic.rack_locations,
             'cage': cage.rack_locations,
             'i19': i19.rack_locations,
             }

suffixes = {'i19': i19.suffixes}

api = Blueprint('zones', __name__, url_prefix='/api')

@api.route('/dewars/locations/<zone>', methods=['GET'])
def get_location(zone='zone6'):
    """
    API route for dewar management
    """
    result = {}
    status_code = 200

    if zone not in locations:
        result = {'status': 'fail',
                   'message': 'Zone parameter not valid for this application'}
        status_code = 400

        return __json_response(result, status_code)

    if request.method == 'GET':
        # Get Rack Locations for this zone
        rack_locations = locations.get(zone)
        rack_suffixes = suffixes.get(zone) or ('',)
        # Get any dewar with provided rack locations
        # There should only be one per location
        result, status_code = common.find_dewars_by_location(rack_locations, rack_suffixes)
    else:
        result = {'location': '',
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'Method/route not implemented yet'}
        status_code = 501

    return __json_response(result, status_code)

@api.route('/dewars/locations', methods=['POST', 'DELETE'])
def update_location():
    """
    API route for dewar management

    This does not check the location for a specific zone - front end will do that
    """
    result = {}
    status_code = 200

    if request.method == 'POST':
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

    return __json_response(result, status_code)


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

    return __json_response(result, status_code)

@api.route('/dewars/comments/<dewarId>', methods=['PATCH'])
def comments(dewarId):
    comments = request.form.get('comments')

    result, status_code = common.update_dewar_comments(dewarId, comments)

    return __json_response(result, status_code)

def __json_response(result, code):
    """
    Build and send the response - preseve dict order by using response object
    jsonify is simpler but does not preserve order
    """
    response = make_response()

    response.data=json.dumps(result)
    response.status_code=code
    response.mimetype='application/json'

    return response
