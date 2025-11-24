import os
import logging
import requests
from urllib.parse import urljoin

# Build the URL for the routes (using env settings)
synchweb_host = os.environ.get("SYNCHWEB_HOST", "https://192.168.33.10")
set_dewar_history_url = urljoin(synchweb_host, "/api/shipment/dewars/history")
container_history_url = urljoin(synchweb_host, "/api/shipment/containers/history")
dewar_comments_url = urljoin(synchweb_host, "/api/shipment/dewars/comments")

# New endpoints to avoid SQLAlchemy calls
rest_api_host = os.environ.get("REST_API_HOST", "http://172.23.168.164")
dewar_location_endpoint = os.environ.get("DEWAR_LOCATION_ENDPOINT", "/api/beamlines/cage")
dewar_location_url = urljoin(rest_api_host, dewar_location_endpoint)
recent_storage_history_endpoint = os.environ.get("RECENT_STORAGE_HISTORY_ENDPOINT", "/api/dewars/recent")
recent_storage_history_url = urljoin(rest_api_host, recent_storage_history_endpoint)
dewar_history_endpoint = os.environ.get("DEWAR_HISTORY_ENDPOINT", "/api/dewars/history")
get_dewar_history_url = urljoin(rest_api_host, dewar_history_endpoint)
find_dewar_endpoint = os.environ.get("DEWAR_ENDPOINT", "/api/dewars/find")
find_dewar_url = urljoin(rest_api_host, find_dewar_endpoint)

# In production we want to use ssl and verify the certificate. 
# Not for debug though so we can disable the ssl check via environment variable SYNCHWEB_SSL=0
verify_ssl = True if os.environ.get("SYNCHWEB_SSL", "1") == "1" else False

def set_location(barcode, location, awb=None):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    result = None

    payload = {'BARCODE': barcode, 'LOCATION': location}

    if awb:
        payload['TRACKINGNUMBERFROMSYNCHROTRON'] = awb

    try:
        # Added timeout to request
        r = requests.post(set_dewar_history_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set location in ISPyB via SynchWeb bc: {} loc: {} ".format(barcode, location))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(set_dewar_history_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(set_dewar_history_url))

    return result


def set_status(barcode, status):
    """
    This updates ISPyB dewar history with a status (eg LN2 Topped Up)
    """
    result = None

    payload = {'BARCODE': barcode, 'STATUS': status}

    try:
        r = requests.post(set_dewar_history_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set status in ISPyB via SynchWeb bc: {} loc: {} ".format(barcode, status))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting status in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(set_dewar_history_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(set_dewar_history_url))

    return result


def set_container_location(code, location):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    global container_history_url
    result = None

    payload = {'CODE': code, 'LOCATION': location}

    logging.getLogger('ispyb-logistics').info("Set container location in ISPyB via SynchWeb payload: {}".format(payload))
    
    try:
        # Added timeout to request
        r = requests.post(container_history_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set location in ISPyB via SynchWeb bc: {} loc: {} ".format(code, location))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(container_history_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(container_history_url))

    return result

def set_container_location_from_id(id, location):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    global container_history_url
    result = None

    payload = {'CONTAINERID': id, 'LOCATION': location}

    try:
        # Added timeout to request
        r = requests.post(container_history_url, data=payload, timeout=5, verify=verify_ssl)

        if r.status_code == requests.codes.ok:
            result = r.json()
            logging.getLogger('ispyb-logistics').info("Set location in ISPyB via SynchWeb id: {} loc: {} ".format(id, location))
        else:
            logging.getLogger('ispyb-logistics').error("Error setting location in ISPyB via SynchWeb {} {}".format(r.status_code, r.text))
    except requests.ConnectionError:
        logging.getLogger('ispyb-logistics').error("Error (connection) trying to post to {}".format(container_history_url))
    except requests.Timeout:
        logging.getLogger('ispyb-logistics').error("Error (timeout) trying to post to {}".format(container_history_url))

    return result

def update_comments(dewarId, comments):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar comments and triggers e-mails
    """
    global dewar_comments_url

    url = f"{dewar_comments_url}/{dewarId}"
    result = None

    # The comments payload is actually json for this use case
    # Combination of posting to the patch endpoint works
    payload = {'COMMENTS': comments}
    headers = {'X-HTTP-Method-Override':'PATCH'}

    try:
        # Added timeout to request
        r = requests.post(url, data=payload, timeout=5, verify=verify_ssl, headers=headers)

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


def find_dewars_by_location():
    r = requests.get(dewar_location_url)
    results = r.json()
    return results


def find_dewar_history_for_locations(locations, max_entries=20):
    payload = {"locations": locations, "max_entries": max_entries}
    r = requests.get(get_dewar_history_url, params=payload)
    results = r.json()
    return results


def find_recent_storage_history(locations):
    payload = {"locations": locations}
    r = requests.get(recent_storage_history_url, params=payload)
    results = r.json()
    return results


def find_dewar_history_for_dewar(dewarCode, max_entries=3):
    payload = {"DEWARCODE": dewarCode, "MAX_ENTRIES": max_entries}
    r = requests.get(find_dewar_url, params=payload)
    results = r.json()
    return results
