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
from api.dewars import zone6
from api.dewars import zone4
from api.dewars import ebic
from api.containers import lab14

beamlines = {'zone6': zone6.beamline_locations,
             'zone4': zone4.beamline_locations,
             'ebic': ebic.beamline_locations,
             'lab14': lab14.beamline_locations
             }


api = Blueprint('beamlines', __name__, url_prefix='/api')

@api.route('/beamlines/<zone>', methods=['GET'])
def get_beamlines(zone='zone6'):
    """
    API route for dewar management
    """
    result = {}
    status_code = 200

    if zone not in beamlines:
        result = {'status': 'fail',
                   'message': 'Zone parameter not valid for this application'}
        status_code = 400

        return __json_response(result, status_code)

    if request.method == 'GET':
        # Get Rack Locations for this zone
        result = beamlines.get(zone)
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
