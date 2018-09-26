import logging
import requests

synchweb_url = "http://192.168.33.10/api/shipment/dewars/history"


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
        r = requests.post(synchweb_url, data=payload)

        if r.status_code == requests.codes.ok:
            result = r.json()
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {}".format(r.status_code))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error trying to post to {}".format(synchweb_url))

    return result

