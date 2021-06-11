"""
Module to hold common code for ebic and zone6 routes

All methods should return a result and status_code tuple
The calling method will jsonify the result
"""
import logging
from collections import OrderedDict
from api.ispyb_api import container_controller as controller


def results_to_list(result):
    return [ {"location": key, "containers": result[key]} for key in result.keys()]

def find_containers_by_location(locations):
    results = OrderedDict([(location, []) for location in locations])

    status_code = 200

    containers = controller.find_containers_by_location(locations)

    if containers is None:
        return _send_error_result('Error retrieving containers from database', 503)

    # If containers is empty array return 404 (and also return a blank list)
    if len(containers.keys()) == 0:
        logging.getLogger('ispyb-logistics').debug("Did not find any containers for these locations {}".format(locations))
        status_code = 404
    else:
        # Now update the list of containers to our results dictionary (Make sure to preseve upper case locations)
        for key, value in containers.items():
            results[key.upper()] = value

    return results_to_list(results), status_code

def find_container(barcode):
    """
    Return container details for this item
    """
    # Do we have a valid facility code?
    if barcode is None:
        return __send_error_result('invalid facility or barcode', 400)

    container = controller.find_container_by_barcode(barcode)

    if container is None:
        return __send_error_result('facility/barcode not found', 404)
    else:
        return container, 200

def __send_error_result(message, code=400):
    result = {
        'status': 'fail',
        'reason': message
    }
    return result, code

def update_container_location(id, barcode, location):
    result = {}
    status_code = 200
    
    logging.getLogger('ispyb-logistics').debug("Update container location")

    if id: logging.getLogger('ispyb-logistics').debug("Update container %s to location %s" % (id, location))
    if barcode: logging.getLogger('ispyb-logistics').debug("Update container %s to location %s" % (barcode, location))

    if id: result = controller.set_container_location_from_id(id, location)
    else: result = controller.set_container_location(barcode, location)

    if result is None:
        return __send_error_result('Container or location not found', 404)

    return result, status_code