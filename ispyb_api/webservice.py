import os
import logging
import requests
from urllib.parse import urljoin

# Build the URL for the POST route (using env settings)
synchweb_host = os.environ.get("SYNCHWEB_HOST", "https://192.168.33.10")
synchweb_url = urljoin(synchweb_host, "/api/shipment/dewars/history")
verify_ssl = True

def set_location(barcode, location, awb=None):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    global synchweb_url
    result = None

    payload = {'BARCODE': barcode, 'LOCATION': location}

    if awb:
        payload['TRACKINGNUMBERFROMSYNCHROTRON'] = awb

    try:
        # Added timeout to request
        r = requests.post(synchweb_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set location in ISPyB via SynchWeb bc: {} loc: {} awb: {}".format(barcode, location, payload.get('TRACKINGNUMBERFROMSYNCHROTRON', 'No AWB provided')))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(synchweb_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(synchweb_url))

    return result

