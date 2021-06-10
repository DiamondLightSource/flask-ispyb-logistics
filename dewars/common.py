"""
Module to hold common code for ebic and zone6 routes

All methods should return a result and status_code tuple
The calling method will jsonify the result
"""
import logging
from collections import OrderedDict
from ispyb_api import controller


def find_dewar(facilitycode):
    """
    Return a list of matching dewars with this facility code

    Common method to find dewar based on facility code like DLS-MS-1234
    We specifically return the status code so the front end can show feedback
    """
    result = {}
    status_code = 200

    # Do we have a valid facility code?
    if facilitycode:
        dewar = controller.get_dewar_by_facilitycode(facilitycode)

        if dewar:
            # All good so status code is 200 (default)
            result['status'] = 'ok'
            result['facilityCode'] = facilitycode
            result['barcode'] = dewar.get('barcode')
            result['storageLocation'] = dewar.get('storageLocation')
        else:
            result = {'status': 'fail',
                      'reason': 'facilitycode not found'}
            # controller unable to find dewar
            status_code = 404

    else:
        result = {'status': 'fail',
                  'reason': 'invalid facilitycode'}
        status_code = 400

    return result, status_code

def find_dewar_history(dewarcode):
    """
    Return a recent history for this dewar by facility code (or barcode)

    Common method to find dewar based on facility code like DLS-MS-1234
    We specifically return the status code so the front end can show feedback
    """
    result = {}
    status_code = 200
    # Upped the request to avoid duplicate entries on beamlines
    # Let the client side display a subset if required
    history_depth = 50

    # Do we have a valid facility code?
    if dewarcode:
        dewar = controller.find_dewar_history_for_dewar(dewarcode, history_depth)

        if dewar:
            # All good so status code is 200 (default)
            result['status'] = 'ok'
            result['facilityCode'] = dewar.get('facilityCode')
            result['barcode'] = dewar.get('barCode')
            result['storageLocations'] = dewar.get('storageLocations')
        else:
            result = {'status': 'fail',
                      'reason': 'facility/barcode not found'}
            # controller unable to find dewar
            status_code = 404
    else:
        result = {'status': 'fail',
                  'reason': 'invalid facility or barcode'}
        status_code = 400

    return result, status_code

def remove_dewar_from_location(location):
    result = {}
    status_code = 401 # Default unauthorized request

    # Find the dewar in this location (pass in as a list item)
    result = controller.find_dewars_by_location([location])

    if location in result:
        barcode = result[location]['barcode']

        logging.getLogger('ispyb-logistics').debug("Remove barcode %s from location %s" % (barcode, location))
        # Should we update the transport history to show its been taken out?
        # It would affect the LN2 top up assumption
        result = controller.set_location(barcode, 'REMOVED FROM {}'.format(location))

        if result:
            status_code = 200
        else:
            result = {'status': "fail",
                      'reason': 'webservice failed to accept delete request'}
    else:
        logging.getLogger('ispyb-logistics').warn('Could not find a dewar in location {}'.format(location))

        result = {'location': location,
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'No dewar at location found'}
        status_code = 404

    return result, status_code


def update_dewar_location(barcode, location, awb=None):
    result = {}
    status_code = 200

    logging.getLogger('ispyb-logistics').debug("Update barcode %s to location %s" % (barcode, location))

    result = controller.set_location(barcode, location, awb)

    if result is None:
        result = {'location': location,
                  'barcode': barcode,
                  'status': 'fail',
                  'reason': 'Dewar or location not found'}
        status_code = 404

    return result, status_code


def find_dewars_by_location(locations):
    # Could use an ordered dict here but jsonify step will break it
    results = OrderedDict([(location, {'barcode':"", 'arrivalDate':"", 'facilityCode':"", 'status':"", 'onBeamline':False}) for location in locations])
    # Initialise here so we can preserve the order
    # for location in locations:
    #     results[location] = ["", "", ""]

    status_code = 200

    dewars = controller.find_dewars_by_location(locations)

    if dewars is None:
        results = {'location': locations,
                  'status': 'fail',
                  'reason': 'Error retrieving dewars from database'}
        status_code = 503
    else:
        # If no dewars return 404 (and also return a blank list)
        if len(dewars.keys()) == 0:
            logging.getLogger('ispyb-logistics').debug("Did not find any dewars for these locations {}".format(locations))
            status_code = 404
        else:
            # Now update the list of dewars to our results dictionary (Make sure to preseve upper case locations)
            for key, value in dewars.items():
                results[key.upper()] = value

            # For locations showing as empty - check that the dewars are not actually on beamline...
            # Required for main zone4 use case where the case is left in the storageLocation
            empty_locations = [location for location in locations if results[location]['barcode'] == '']

            processing_dewars = controller.find_recent_storage_history(empty_locations)
            # Add dewars that are in processing to our return list
            # Make sure to preseve upper case locations
            # Front end can filter 'onBeamline'
            for key, value in processing_dewars.items():
                logging.getLogger('ispyb-logistics').debug("Adding empty locations {}".format(key))
                if value['onBeamline']:
                    results[key.upper()] = value
                # Else ignore as the dewar is elsewhere....

    return results, status_code

def update_dewar_comments(dewarId, comments):
    result = {}
    status_code = 200

    logging.getLogger('ispyb-logistics').debug("Update dewarId %s with comments %s" % (dewarId, comments))

    result = controller.update_comments(dewarId, comments)

    if result is None:
        result = {'location': comments,
                  'dewarId': dewarId,
                  'status': 'fail',
                  'reason': 'Dewar not found'}
        status_code = 404

    return result, status_code