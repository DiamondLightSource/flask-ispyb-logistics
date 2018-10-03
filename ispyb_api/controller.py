import re
import logging

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
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
    d = Dewar.query.filter_by(FACILITYCODE = fc).order_by(desc(Dewar.dewarId)).first()

    if d:
        result = {'barcode': d.barCode,  'storageLocation': d.storageLocation}
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
        logging.getLogger('ispyb-logistics').error("Error barcode {} not exist in ISPyB".format(barcode))
    except MultipleResultsFound:
        logging.getLogger('ispyb-logistics').error("Error multiple results found for barcode {}".format(barcode))

    return result

def find_dewars_by_location(locations):
    """
    This method will find a dewar based on its location.
    """
    logging.getLogger('ispyb-logistics').debug("find_dewars_by_location {}".format(','.join(locations)))
    
    results = {}

    try: 
        # Query for dewars with transporthistory locations in the list
        # Use case insensitive search for storageLocation
        # Get the timestamp and location from the transport history 
        # Order so we get the most recent first...
        # The Dewar storageLocation does not always match the transport history
        dewars = Dewar.query.join(DewarTransportHistory).filter(func.lower(Dewar.storageLocation).in_(locations)).\
            filter(Dewar.dewarId == DewarTransportHistory.dewarId).\
            order_by(desc(DewarTransportHistory.arrivalDate)).\
            values(Dewar.barCode, Dewar.bltimeStamp, Dewar.storageLocation, DewarTransportHistory.arrivalDate)

        for dewar in dewars:
            # If we already have an entry, it means there is a more recent change for a dewar in this location
            # Note we store the data in upper case - SynchWeb uses lower case while the UI requests data in upper case...
            if dewar.storageLocation.upper() in results:
                logging.getLogger('ispyb-logistics').debug('Ignoring older entry for dewar {} location {} at {}'.format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
            else:
                logging.getLogger('ispyb-logistics').info('Found entry for this dewar {} to {} at {}'.format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
                results[dewar.storageLocation.upper()] = [dewar.barCode, dewar.arrivalDate]

    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error retrieving dewars")

    # Now add entries for those locations we did not find (to support the front end logic)
    for location in locations:
        if location not in results:
            results[location] = ["", ""]

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
