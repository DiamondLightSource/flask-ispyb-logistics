import re
import logging
import itertools

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc, func

import webservice
from models import Dewar, DewarTransportHistory, Shipping, Proposal


def set_location(barcode, location, awb=None):
    """
    Redirect this request to SynchWeb to trigger e-mail alerts etc

    This might be a facility code (if the label is unreadable)
    So first check if this is a facility code, then use the actual barcode
    """
    # Test if this is actually a facility code
    if is_facility_code(barcode):
        dewar = get_dewar_by_facilitycode(barcode)
        if dewar:
            actual_barcode = dewar.get('barcode')
        else:
            actual_barcode = None
    else:
        actual_barcode = barcode

    return webservice.set_location(actual_barcode, location, awb)

def get_dewar_by_facilitycode(fc):
    """
    This method will find a dewar based on its facilitycode.
    """
    result = None

    # Facility codes are reused, so we want the most recent version 
    # We work that out based on the newest (highest) dewarId
    # Could also specify that its a dewar on site, at-facility perhaps?
    d = Dewar.query.filter(Dewar.FACILITYCODE == fc).order_by(desc(Dewar.dewarId)).first()

    if d:
        result = {'barcode': d.barCode,  'dewarId': d.dewarId, 'storageLocation': d.storageLocation}
        logging.getLogger('ispyb-logistics').info("Found dewar with FacilityCode {} in location {}".format(fc, d.storageLocation))
    else:
        logging.getLogger('ispyb-logistics').warn("Could not find dewar with FacilityCode {}".format(fc))

    return result

def get_dewar_by_barcode(barcode):
    """
    This method will find a dewar based on its barcode.

    It enforces only one result and will throw an error if there is not one.
    """
    logging.getLogger('ispyb-logistics').debug("get_dewar_by_barcode {}".format(barcode))
    result = {}

    try: 
        d = Dewar.query.filter_by(barCode = barcode).one()

        result['dewarId'] = d.dewarId
        result['barCode'] = d.barCode
        result['storageLocation'] = d.storageLocation
        result['facilityCode'] = d.FACILITYCODE

    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error barcode {} does not exist in ISPyB".format(barcode))
    except MultipleResultsFound:
        logging.getLogger('ispyb-logistics').error("Error multiple results found for barcode {}".format(barcode))

    return result

def find_dewars_by_location(locations):
    """
    This method will find the most recent dewar stored in each location.
    """
    logging.getLogger('ispyb-logistics').debug("find_dewars_by_location {}".format(','.join(locations)))
    
    results = {}

    try: 
        # Query for dewars with transporthistory locations in the list
        # Use case insensitive search for storageLocation
        # Get the timestamp and location from the transport history 
        # Order so we get the most recent first...
        # The Dewar storageLocation does not always match the transport history
        dewars = Dewar.query.join(DewarTransportHistory).\
            filter(func.lower(Dewar.storageLocation).in_(locations)).\
            filter(Dewar.dewarId == DewarTransportHistory.dewarId).\
            filter(func.lower(Dewar.storageLocation) == func.lower(DewarTransportHistory.storageLocation)).\
            order_by(desc(DewarTransportHistory.arrivalDate)).\
            values(Dewar.barCode, 
                   Dewar.FACILITYCODE, 
                   Dewar.bltimeStamp, 
                   Dewar.storageLocation, 
                   DewarTransportHistory.arrivalDate,
                   DewarTransportHistory.dewarStatus,
                   )

        for dewar in dewars:
            # If we already have an entry, it means there is a more recent change for a dewar in this location
            # Note we store the data in upper case - SynchWeb uses lower case while the UI requests data in upper case...
            if dewar.storageLocation.upper() in results:
                logging.getLogger('ispyb-logistics').debug('Ignoring older entry for dewar {} location {} at {}'.format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
            else:
                logging.getLogger('ispyb-logistics').info('Found entry for this dewar {} in {} at {}'.format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
                # Returning three items per location [barcode, arrivalDate and FacilityCode]
                results[dewar.storageLocation.upper()] = [dewar.barCode, dewar.arrivalDate, dewar.FACILITYCODE, dewar.dewarStatus]

    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error retrieving dewars")
    except DBAPIError:
        logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')
        results = None

    return results

def find_dewar_history_for_locations(locations, max_entries=20):
    """
    This method will find 'n' entries from the dewar transport history table filtered by location.

    Returns {'1', {'barcode':barcode, 'awb':awb, 'date':arrivalDate...}, }
    """
    results = {}

    try:
        # Query for dewars with transporthistory locations in the list
        # Use case insensitive search for storageLocation
        # Get the timestamp and location from the transport history
        # Order so we get the most recent first...
        # Check if the locations match between dewar and transport history
        dewars = DewarTransportHistory.query.join(Dewar).join(Shipping).\
            filter(func.lower(DewarTransportHistory.storageLocation).in_(locations)).\
            filter(Dewar.dewarId == DewarTransportHistory.dewarId).\
            filter(Dewar.shippingId == Shipping.shippingId).\
            filter(Dewar.storageLocation == DewarTransportHistory.storageLocation).\
            order_by(desc(DewarTransportHistory.arrivalDate)).\
            limit(max_entries).\
            values(Dewar.barCode,
                   Dewar.FACILITYCODE,
                   Dewar.bltimeStamp,
                   Dewar.trackingNumberFromSynchrotron,
                   DewarTransportHistory.storageLocation,
                   DewarTransportHistory.arrivalDate,
                   DewarTransportHistory.dewarStatus,
                   Shipping.shippingId,
                   )

        for index, dewar in enumerate(dewars):
            logging.getLogger('ispyb-logistics').info('Found entry {} for this dewar {} in {} at {}'.format(index, dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
            # Build the return object - format aligns a previous iteration of the app
            results[str(index)] = {
                'barcode':dewar.barCode,
                'date': dewar.arrivalDate,
                'inout': dewar.storageLocation, # should really change 'inout' to location
                'facilitycode': dewar.FACILITYCODE,
                'status': dewar.dewarStatus,
                'awb': dewar.trackingNumberFromSynchrotron,
                'sid': dewar.shippingId,
                 }

    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error retrieving dewars")
    except DBAPIError:
        logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')
        results = None

    return results

def find_dewar_history_for_dewar(dewarCode, max_entries=3):
    """
    This method will find 'n' entries from the dewar transport history table filtered by dewarId.

    Accepts facilityCode or barcode as the dewar Code

    Returns {'dewarId':dewarId, 'barcode': barcode, facilityCode': facilityCode, storageLocations': [location1, location2...] }
    """
    results = None

    try:
        # Query for dewar transporthistory for specific dewarId
        # Get the timestamp and location from the transport history
        # Order so we get the most recent first...
        query = DewarTransportHistory.query.join(Dewar).\
            filter(Dewar.dewarId == DewarTransportHistory.dewarId)

        if is_facility_code(dewarCode):
            query = query.filter(Dewar.FACILITYCODE == dewarCode)
        else:
            # Try using the passed variable as barcode
            query = query.filter(Dewar.barCode == dewarCode)

        dewarHistory = query.order_by(desc(DewarTransportHistory.arrivalDate)).\
            limit(max_entries).\
            values(Dewar.barCode,
                   Dewar.dewarId,
                   Dewar.FACILITYCODE,
                   DewarTransportHistory.storageLocation,
                   DewarTransportHistory.arrivalDate,
                   )
        # Temporary store for locations/dates (so we can post-process the results)
        locations = []

        # Return is a generator so we need to iterate through results
        for index, dewar in enumerate(dewarHistory):
            logging.getLogger('ispyb-logistics').info('Found entry {} for this dewar {} in {}'.format(index, dewar.barCode, dewar.storageLocation))

            if results is None:
                results = {}
                results['dewarId'] = Dewar.dewarId
                results['storageLocations'] = []
                # Only one barcode/facilitycode, so just grab first one...?
                results['barCode'] = dewar.barCode
                results['facilityCode'] = dewar.FACILITYCODE
            # Content that differs for each entry...
            item = {'location': dewar.storageLocation, 'arrivalDate': dewar.arrivalDate}
            locations.append(item)

        # Annoyingly we find lots of entries where the locations are the same (i04, i04, i04... for every puck scan)
        # This method removes all duplicate sequential entries for us...
        results['storageLocations'] = [g.next() for k,g in itertools.groupby(locations, lambda x: x.get('location'))]
        
    except DBAPIError:
        logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')
        results = None

    return results

def find_dewars_by_proposal(proposal_code, proposal_number):
    """
    Example of retrieving all dewars for a given proposal...
    """
    results = Dewar.query.join(Shipping).join(Proposal).\
        filter(Proposal.proposalCode == proposal_code, Proposal.proposalNumber == proposal_number).\
        filter(Proposal.proposalId == Shipping.proposalId).\
        filter(Shipping.shippingId == Dewar.shippingId).\
        values(Dewar.dewarId, 
               Dewar.shippingId,
               Dewar.barCode,
               Dewar.code,
               Dewar.comments,
               Dewar.storageLocation,
               Dewar.dewarStatus,
               Dewar.isStorageDewar,
               Dewar.barCode,
               Dewar.firstExperimentId,
               Dewar.type,
               Dewar.FACILITYCODE,
               Dewar.weight,
               Dewar.deliveryAgent_barcode,
               Proposal.title, 
               Shipping.shippingName)
               
    return results

def is_facility_code(code):
    """
    Utiliy method to check if the string provided is a facilitycode
    i.e. matches 'DLS-MX-1234' pattern
    Note we test for 3chars-2chars-number (case insensitive)
    """
    result = False

    expr = re.compile(r'[A-Z]{3}-[A-Z]{2}-\d', re.IGNORECASE)
    match = expr.match(code)
    
    if match:
        logging.getLogger('ispyb-logistics').debug('{} is a facility code'.format(code))
        result = True
    else:
        logging.getLogger('ispyb-logistics').debug('{} is NOT a facilitycode'.format(code))
        result = False

    return result
