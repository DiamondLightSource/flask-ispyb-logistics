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
