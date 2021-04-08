"""
Module to hold common code for ebic and zone6 routes

All methods should return a result and status_code tuple
The calling method will jsonify the result
"""
import logging
from collections import OrderedDict
from ispyb_api import controller


def find_containers_by_location(locations):
    # Could use an ordered dict here but jsonify step will break it
    results = OrderedDict([(location, {'barcode':"", 'arrivalDate':"", 'facilityCode':"", 'status':"", 'onBeamline':False}) for location in locations])
    # Initialise here so we can preserve the order
    # for location in locations:
    #     results[location] = ["", "", ""]

    status_code = 200

    containers = controller.find_containers_by_location(locations)

    if containers is None:
        results = {'location': locations,
                  'status': 'fail',
                  'reason': 'Error retrieving containers from database'}
        status_code = 503
    else:
        # If no containers return 404 (and also return a blank list)
        if len(containers.keys()) == 0:
            logging.getLogger('ispyb-logistics').debug("Did not find any containers for these locations {}".format(locations))
            status_code = 404
        else:
            # Now update the list of containers to our results dictionary (Make sure to preseve upper case locations)
            for key, value in containers.items():
                results[key.upper()] = value

    return results, status_code

def find_container(barcode):
    """
    Return container details for this item
    """
    result = {}
    status_code = 200
    # Do we have a valid facility code?
    if barcode:
        container = controller.find_container_by_barcode(barcode)

        if container:
            # All good so status code is 200 (default)
            result = container
        else:
            result = {'status': 'fail',
                      'reason': 'facility/barcode not found'}
            # controller unable to find container
            status_code = 404
    else:
        result = {'status': 'fail',
                  'reason': 'invalid facility or barcode'}
        status_code = 400

    return result, status_code