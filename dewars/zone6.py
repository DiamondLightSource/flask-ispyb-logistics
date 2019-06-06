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

beamline_locations = ['I03',
                      'I04',
                      'I04-1',
                      'I19',
                      'I24',
                      'USER-COLLECTION',
                      'STORES-OUT',
                      'EBIC'
                      ]
