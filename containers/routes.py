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

from . import lab14

locations = {'lab14': lab14.rack_locations
             }

beamlines = {'lab14': lab14.beamline_locations
             }


api = Blueprint('containers', __name__, url_prefix='/api')

@api.route('/containers/locations/<zone>', methods=['GET'])
def get_container_locations(zone='lab14'):
    """
    API route for container (lab14) management
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
        # Get any dewar with provided rack locations
        # There should only be one per location
        result, status_code = common.find_containers_by_location(rack_locations)
    else:
        result = {'location': '',
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'Method/route not implemented yet'}
        status_code = 501

    return __json_response(result, status_code)

@api.route('/containers/find/', methods=['GET'])
def find_container(zone='lab14'):
    """
    API route for container (lab14) management
    """
    result = {}
    status_code = 200

    barcode = request.args.get('barcode')

    result, status_code = common.find_container(barcode)

    return __json_response(result, status_code)

@api.route('/containers/locations', methods=['POST'])
def update_location():
    """
    API route for container management

    This does not check the location for a specific zone - front end will do that
    """
    result = {}
    status_code = 200

    logging.getLogger('ispyb-logistics').info("Update container locations")

    if request.method == 'POST':
        location = request.form.get('location')
        cid = request.form.get('containerId')      
        barcode = request.form.get('barcode')

        logging.getLogger('ispyb-logistics').info("Update container locations {}".format(location))

        if cid:
            result, status_code = common.update_container_location(cid, None, location)
        else:
            result, status_code = common.update_container_location(None, barcode, location)

    else:
        result = {'location': '',
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'Method/route not implemented yet'}
        status_code = 501

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
