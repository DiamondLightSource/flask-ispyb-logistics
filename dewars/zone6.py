from datetime import datetime
import time
import json

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

import logs
from ispyb_api import ISPyBManager

# Remove remote ip when deployed
remote_ip = '127.0.0.1'
allowed_ips = ['127.0.0.1']

api = Blueprint('zone6', __name__, url_prefix='/zone6')

jsonfilename = 'logs/dewars.json'

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

# Abstract our interface to ISPyB - specialised for ebic/zone6 etc.
ispyb_api = ISPyBManager(beamlines, beamline_prefix, rack_prefix)


@api.route('/')
def index():
    rack_locations = ['-'.join([rack_prefix, suffix])
                      for suffix in rack_suffixes]

    return render_template('dewars.html',
                           title="zone6 Dewar Management",
                           rack_locations=rack_locations,
                           rack_suffixes=rack_suffixes,
                           rack_prefix=rack_prefix,
                           beamlines=beamline_locations,
                           api_prefix="zone6",
                           )


@api.route('/dewars', methods=["GET", "POST"])
def location():
    result = {}

    if request.method == "GET":
        result = logs.readJsonFile(jsonfilename)

        # The web page makes this request every x minutes.
        # Hence it will call this within a minute - feels a bit hacky...
        minute = datetime.time(datetime.now()).minute

        if minute == 0 and remote_ip in allowed_ips:
            result = ispyb_api.checkDewars(result)
            logs.writeJsonFile(result)

    elif request.method == "POST":
        location = request.form['location']
        barcode = request.form['barcode']

        print("Update barcode %s to location %s" % (barcode, location))

        result = _api_write(location, barcode)
    else:
        result = {'location': '',
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'Method/route not implemented yet'}

    return jsonify(result)


@api.route('/dewars/find', methods=["GET"])
def find():
    """
    Return a list of matching dewars with this facility code

    Should be requested with parameters in the URL ?fc=DLS-MS-1234 request
    """
    result = []

    facilitycode = request.args.get('fc')

    # Do we have a valid facility code?
    if facilitycode is not None:
        print "FIND METHOD: FacilityCode = ", facilitycode

        dewars = ispyb_api.getDewars()

        for dewar in dewars:
            if dewar['barCode'] is not None and dewar['facilityCode'] is not None and facilitycode in dewar['facilityCode']:
                result.append(dewar['barCode'])

    # Potentially extend this to search through the json or ispyb records.
    # Currently the front end does the searching to find where this barcode is located

    return jsonify(result)

def _api_write(location, barcode):
    """
	Why is the remote ip address check at the bottom?
	Implies the json file is updated and then if ip address does not match, 
	fail to update ISPyB???

	Writes/Updates a RACK Location with the Dewar barcode and datetime
	Example "RACK-A1: ["mx18938-I04-1-20180806", "Mon 06 Aug, 2018 10:19:28"]

    Returns a dictionary which will be turned into json by flask jsonify
	"""
    result = {}

    if location is not None and barcode is not None:
        data = logs.readJsonFile(jsonfilename)

        for key in data.keys():
            if key.startswith(rack_prefix):
                if data[key][0] == barcode:
                    data[key] = ['',0] # Why 0 and not ""?
            else:
                if barcode in data[key]:
                    data[key].remove(barcode)

        if location not in data:
            result = {'location':location,
                        'barcode':barcode,
                        'status':'fail',
                        'reason':'new location'}
        else:
            if location.startswith(rack_prefix):
                data[location] = [barcode, time.strftime('%a %d %b, %Y %H:%M:%S')]
            else:
                data[location].append(barcode)

            logs.writeJsonFile(jsonfilename, data)

            # Assuming that we move the ip authorization out
            # if remote_ip in allowed_ips:
            dewarid = ispyb_api.setLocation(barcode, location)

            if dewarid is not None:
                result = {'location':location,
                          'barcode':barcode,
                          'status':'ok',
                          'dewarid':dewarid}
            else:
                result = {'location':location,
                          'barcode':barcode,
                          'status':'fail',
                          'reason': 'Did not get valid dewar id from ISPyB'}
    print result
    return result