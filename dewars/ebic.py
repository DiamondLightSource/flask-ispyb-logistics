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

