import os
import logging
import requests
from urllib.parse import urljoin

# Build the URL for the POST route (using env settings)
synchweb_host = os.environ.get("SYNCHWEB_HOST", "https://192.168.33.10")
synchweb_url = urljoin(synchweb_host, "/api/shipment/dewars/history")
synchweb_dewar_comments_url = urljoin(synchweb_host, "/api/shipment/dewars/comments")
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

def update_comments(dewarId, comments):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar comments and triggers e-mails
    """
    global synchweb_dewar_comments_url

    url = synchweb_dewar_comments_url
    result = None

    payload = {'DEWARID': dewarId, 'COMMENTS': comments}

    logging.getLogger('ispyb-logistics').info("Try to Update dewar comments in ISPyB via SynchWeb payload: {}".format(payload))

    try:
        # Added timeout to request
        r = requests.post(url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set dewar comments in ISPyB via SynchWeb id: {} comments: {}".format(dewarId, comments))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(url))

    return result

