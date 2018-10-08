"""
Module to hold common code for ebic and zone6 routes

All methods should return a result and status_code tuple
The calling method will jsonify the result
"""
import logging
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


def remove_from_location(location):
    result = {}
    status_code = 200

    # Find the dewar in this location (pass in as a list item)
    result = controller.find_dewars_by_location([location])

    logging.getLogger('ispyb-logistics').debug("Find dewar by location {} got result: {}".format(location, result))

    if location in result:
        barcode = result[location][0]

        logging.getLogger('ispyb-logistics').debug("Update barcode %s to location %s" % (barcode, location))
        # Should we update the transport history to show its been taken out?
        # It would affect the LN2 top up assumption
        result = controller.set_location(barcode, 'REMOVED FROM {}'.format(location))
    else:
        logging.getLogger('ispyb-logistics').warn('Could not find a dewar in location {}'.format(location))

        result = {'location': location,
                  'barcode': '',
                  'status': 'fail',
                  'reason': 'No dewar at location found'}
        status_code = 404

    return result, status_code


def update_dewar_location(barcode, location):
    result = {}
    status_code = 200

    logging.getLogger('ispyb-logistics').debug("Update barcode %s to location %s" % (barcode, location))

    result = controller.set_location(barcode, location)

    if result is None:
        result = {'location': location,
                  'barcode': barcode,
                  'status': 'fail',
                  'reason': 'Dewar or location not found'}
        status_code = 404

    return result, status_code
