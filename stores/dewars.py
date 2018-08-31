import time

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

import logs
from ispyb_api import ISPyBManager


api = Blueprint('stores', __name__, url_prefix='/stores')

jsonfilename = 'logs/stores.json'

# Create our interface to ISPyB - specialised for ebic/mx etc.
# For store use we don;t need to specifiy beamlines etc...
ispyb_api = ISPyBManager()


@api.route('/dewars')
def index():
    return render_template('stores.html',
                           title="Stores Dewar Management",
                           api_prefix="stores",
                           max_dewar_history=logs.max_stores_dewars
                           )


@api.route('/dewars/location', methods=["GET", "POST"])
def location():
    result = {}

    if request.method == "GET":
        deque_data = logs.readStoresFile(jsonfilename)

        # Marshall the data into a serializable json array with 
        # indexes {1, {}, 2, {}} etc. to match the front end
        for index, item in enumerate(deque_data, 1):
            result[str(index)] = item

    elif request.method == "POST":
        location = request.form['location']
        barcode = request.form['barcode']
        awb = request.form['awb']

        if location and barcode:
            result = updateDewarLocation(barcode, location, awb)
        else:
            print("Warning barcode and/or location not set, ignoring request.")

            result = {'location': location,
                      'barcode': barcode,
                      'awb': awb,
                      'status': 'fail - location and/or barcode not set',
                      'your_ip': remote_ip}

    return jsonify(result)


def updateDewarLocation(barcode, location, awb=None):
    """
    Update the records for this dewar.this

    If it gets here we have already tested that the barcode and location are ok.
    """
    # if remote_ip not in allowed_ips:
    #     print json.dumps({'location':location,'barcode':barcode,'awb':awb,'status':'fail','your_ip':remote_ip})

    if awb:
        awb = awb.replace('+', '_')

    destination = ''

    if location == 'STORES-IN':
        if barcode[0:2] == 'SP' or 'I14' in barcode:
            destination = 'I14'
        elif barcode[0:2] == 'EM' or any(b in barcode for b in ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07']):
            destination = 'eBIC'
        elif barcode[0:2] == 'MX' or any(b in barcode for b in ['I03', 'I04', 'I23', 'I24']):
            destination = 'Zone 6 store'
        else:
            destination = 'Unknown'

    # Next part is new and uses a deque to ensure last 10 dewars are processed
    data = logs.readStoresFile(jsonfilename)

    data.appendleft({'barcode': barcode,
                     'inout': location,
                     'date': time.strftime('%a %d %b, %H:%M:%S'),
                     'destination': destination,
                     'awb': awb})

    logs.writeStoresFile(jsonfilename, data)

    dewarid = ispyb_api.setLocation(barcode, location, awb)

    return {'location': location, 'barcode': barcode, 'awb': awb, 'status': 'ok', 'dewarid': dewarid}
