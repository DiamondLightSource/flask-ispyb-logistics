import requests

synchweb_url = "http://192.168.33.10/api/shipment/dewars/history"


def set_location(barcode, location, awb=None):
    """
    New method that calls the SynchWeb rest services

    This updates ISPyB with dewar history and triggers e-mails
    """
    payload = {'BARCODE': barcode, 'LOCATION': location}

    if awb:
        payload['TRACKINGNUMBERFROMSYNCHROTRON'] = awb

    r = requests.post(synchweb_url, data=payload)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        print("Error setting location in ISPyB via SynchWeb {}".format(r.status_code))
        return None