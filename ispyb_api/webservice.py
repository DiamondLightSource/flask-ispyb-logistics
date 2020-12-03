import os
import logging
import requests
from urllib.parse import urljoin

# Build the URL for the POST route (using env settings)
synchweb_host = os.environ.get("SYNCHWEB_HOST", "https://192.168.33.10")
dewar_history_url = urljoin(synchweb_host, "/api/shipment/dewars/history")
container_history_url = urljoin(synchweb_host, "/api/shipment/containers/history")
verify_ssl = False

def set_location(barcode, location, awb=None):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    global dewar_history_url
    result = None

    payload = {'BARCODE': barcode, 'LOCATION': location}

    if awb:
        payload['TRACKINGNUMBERFROMSYNCHROTRON'] = awb

    try:
        # Added timeout to request
        r = requests.post(dewar_history_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set location in ISPyB via SynchWeb bc: {} loc: {} ".format(barcode, location))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(dewar_history_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(dewar_history_url))

    return result

def set_container_location(barcode, location):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    global container_history_url
    result = None

    payload = {'BARCODE': barcode, 'LOCATION': location}

    try:
        # Added timeout to request
        r = requests.post(dewar_history_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set location in ISPyB via SynchWeb bc: {} loc: {} ".format(barcode, location))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(container_history_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(container_history_url))

    return result

