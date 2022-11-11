import os
import re
import logging
import itertools
from datetime import datetime
import json

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc, func
from sqlalchemy.orm import aliased

from . import db
from . import webservice
from . import send_email
from .models import Dewar, DewarTransportHistory, LabContact, Laboratory, Shipping, Proposal, Person, BLSession, Container

# What age do we ignore container history entries
CONTAINER_FILTER_DAYS_LIMIT = 30
email_domain = os.environ.get('EMAIL_DOMAIN', '@diamond.ac.uk')


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

    dewar_details = get_dewar_by_barcode(actual_barcode)
    previous_location = dewar_details['storageLocation']

    if location == 'LN2TOPUP':
        dewarId = dewar_details['dewarId']
        comments = json.loads(dewar_details['comments'])
        now = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
        if 'toppedUp' in comments and type(comments['toppedUp']) == list:
            comments['toppedUp'].insert(0, now)
            comments['toppedUp'] = comments['toppedUp'][:5]
        else:
            comments['toppedUp'] = [now]
        return update_comments(dewarId, json.dumps(comments))

    result = webservice.set_location(actual_barcode, location, awb)

    if is_arriving_at_ebic(location, previous_location):
        lc_details = get_lc_from_dewar(actual_barcode)
        send_email.email_lc_incoming(actual_barcode, lc_details)
    elif is_leaving_ebic(location):
        lc_details = get_lc_from_dewar(actual_barcode)
        send_email.email_lc_outgoing(actual_barcode, lc_details)

    return result

def get_dewar_by_facilitycode(fc):
    """
    This method will find a dewar based on its facilitycode.
    """
    result = None

    # Facility codes are reused, so we want the most recent version
    # We work that out based on the newest (highest) dewarId
    # Could also specify that its a dewar on site, at-facility perhaps?
    d = Dewar.query.filter(Dewar.facilityCode == fc).order_by(desc(Dewar.dewarId)).first()

    if d:
        result = {'barcode': d.barCode,  'dewarId': d.dewarId, 'storageLocation': d.storageLocation}
        logging.getLogger('ispyb-logistics').info("Found dewar with FacilityCode {} in location {}".format(fc, d.storageLocation))
    else:
        logging.getLogger('ispyb-logistics').warning("Could not find dewar with FacilityCode {}".format(fc))

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
        result['facilityCode'] = d.facilityCode
        result['comments'] = d.comments

    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error barcode {} does not exist in ISPyB".format(barcode))
    except MultipleResultsFound:
        logging.getLogger('ispyb-logistics').error("Error multiple results found for barcode {}".format(barcode))

    return result

def find_dewars_by_location(locations):
    """
    This method will find the most recent dewar stored in each location.
    It matches the Dewar.storageLocation with DewarTransportHistory.storageLocation
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
            join(Container).\
            filter(func.lower(Dewar.storageLocation).in_(locations)).\
            filter(Dewar.dewarId == DewarTransportHistory.dewarId).\
            filter(Dewar.dewarId == Container.dewarId).\
            filter(func.lower(Dewar.storageLocation) == func.lower(DewarTransportHistory.storageLocation)).\
            order_by(desc(DewarTransportHistory.arrivalDate)).\
            values(Dewar.dewarId,
                   Dewar.barCode,
                   Dewar.facilityCode,
                   Dewar.bltimeStamp,
                   Dewar.storageLocation,
                   Dewar.comments,
                   DewarTransportHistory.arrivalDate,
                   DewarTransportHistory.dewarStatus,
                   Container.code,
                   )

        for dewar in dewars:
            # If we already have an entry, it means there is a more recent change for a dewar in this location
            # Note we store the data in upper case - SynchWeb uses lower case while the UI requests data in upper case...
            if dewar.storageLocation.upper() in results:
                if dewar.code not in results[dewar.storageLocation.upper()]['dewarContainers']:
                    results[dewar.storageLocation.upper()]['dewarContainers'].append(dewar.code)
            else:
                logging.getLogger('ispyb-logistics').debug('Found entry for this dewar {} in {} at {}'.format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
                results[dewar.storageLocation.upper()] = {
                    'dewarId': dewar.dewarId,
                    'barcode': dewar.barCode,
                    'arrivalDate': dewar.arrivalDate.isoformat(),
                    'facilityCode': dewar.facilityCode,
                    'status': dewar.dewarStatus,
                    'comments': dewar.comments,
                    'onBeamline': False,
                    'dewarLocation': dewar.storageLocation,
                    'dewarContainers': [dewar.code],
                }

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
            order_by(desc(DewarTransportHistory.arrivalDate)).\
            limit(max_entries).\
            values(Dewar.barCode,
                   Dewar.facilityCode,
                   Dewar.bltimeStamp,
                   Dewar.trackingNumberFromSynchrotron,
                   DewarTransportHistory.storageLocation,
                   DewarTransportHistory.arrivalDate,
                   DewarTransportHistory.dewarStatus,
                   Shipping.shippingId,
                   )

        for index, dewar in enumerate(dewars):
            logging.getLogger('ispyb-logistics').debug('Found entry {} for this dewar {} in {} at {}'.format(index, dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
            # Build the return object - format aligns a previous iteration of the app
            results[str(index)] = {
                'barcode':dewar.barCode,
                'date': dewar.arrivalDate.isoformat(),
                'storageLocation': dewar.storageLocation, # should really change 'inout' to location
                'facilitycode': dewar.facilityCode,
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

def find_recent_storage_history(locations):
    """
    This method was designed specifically for zone4.
    The aim is to find out if the passed locations are actually empty or if the case is still present.
    We do this by finding the most recent entry for each location - then check to see if the dewar location is different.
    If it's at a beamline return true
    else if at stores out or "removed" then show as empty

    Returns {'<location>': {'barcode':barcode, 'dewarLocation': dewarLocation, 'date':arrivalDate...}, }
    """
    results = {}

    try:
        # Query for dewars in passed locations list
        # Use case insensitive search for storageLocation
        # We want to find the latest entry for each location.
        # If the dewar is still on site (on Beamline) return a value, else pass empty object
        subq = db.session.query(
            DewarTransportHistory.DewarTransportHistoryId, func.max(DewarTransportHistory.arrivalDate).label('lastArrival')
        ).group_by(DewarTransportHistory.storageLocation).subquery()

        dewars = DewarTransportHistory.query.join(subq, DewarTransportHistory.arrivalDate == subq.c.lastArrival).\
            join(Dewar, Dewar.dewarId == DewarTransportHistory.dewarId).\
            filter(func.lower(DewarTransportHistory.storageLocation).in_(locations)).\
                values(
                    Dewar.dewarId,
                    Dewar.barCode,
                    Dewar.facilityCode,
                    Dewar.dewarStatus,
                    DewarTransportHistory.DewarTransportHistoryId,
                    DewarTransportHistory.arrivalDate,
                    DewarTransportHistory.storageLocation.label('storageLocation'),
                    Dewar.storageLocation.label('dewarLocation')
                )
        for dewar in dewars:
            logging.getLogger('ispyb-logistics').debug('Found entry for this dewar {} = {}'.format(dewar.storageLocation, dewar))
            # Build the return object - format aligns a previous iteration of the app

            # Conditions
            # - if the dewarStatus is 'processing...' then show as still occupied
            # - if the location begins with i then its at a beamline, show as still occupied
            onBeamline = False
            if dewar.dewarStatus.lower().startswith('processing'):
                onBeamline = True
            elif any(b in dewar.dewarLocation.lower() for b in ['i02', 'i03', 'i04', 'i04-1', 'i19', 'i23', 'i24']):
                onBeamline = True

            results[dewar.storageLocation] = {
                'barcode': dewar.barCode,
                'facilityCode': dewar.facilityCode,
                'dewarStatus': dewar.dewarStatus,
                'arrivalDate': dewar.arrivalDate.isoformat(),
                'onBeamline': onBeamline,
                'dewarLocation': dewar.dewarLocation,
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
            query = query.filter(Dewar.facilityCode == dewarCode)
        else:
            # Try using the passed variable as barcode
            query = query.filter(Dewar.barCode == dewarCode)

        dewarHistory = query.order_by(desc(DewarTransportHistory.arrivalDate)).\
            limit(max_entries).\
            values(Dewar.barCode,
                   Dewar.dewarId,
                   Dewar.facilityCode,
                   DewarTransportHistory.storageLocation,
                   DewarTransportHistory.arrivalDate,
                   )
        # Temporary store for locations/dates (so we can post-process the results)
        locations = []

        # Return is a generator so we need to iterate through results
        for index, dewar in enumerate(dewarHistory):
            logging.getLogger('ispyb-logistics').debug('Found entry {} for this dewar {} in {}'.format(index, dewar.barCode, dewar.storageLocation))

            if results is None:
                results = {}
                results['dewarId'] = Dewar.dewarId
                results['storageLocations'] = []
                # Only one barcode/facilitycode, so just grab first one...?
                results['barCode'] = dewar.barCode
                results['facilityCode'] = dewar.facilityCode
            # Content that differs for each entry...
            item = {'location': dewar.storageLocation, 'arrivalDate': dewar.arrivalDate.isoformat()}
            locations.append(item)

        # Annoyingly we find lots of entries where the locations are the same (i04, i04, i04... for every puck scan)
        # This method removes all duplicate sequential entries for us...
        results['storageLocations'] = [next(g) for k,g in itertools.groupby(locations, lambda x: x.get('location'))]

    except DBAPIError:
        logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')
        results = None

    return results

def get_shipping_return_address(barcode):
    # Get the return lab address for this dewar.
    # Dewar=>Shipping=>LabContact=>Laboratory
    results = None
    try:
        records = Dewar.query.join(Shipping, Dewar.shippingId == Shipping.shippingId).\
            join(LabContact, Shipping.returnLabContactId == LabContact.labContactId).\
            join(Person, LabContact.personId == Person.personId).\
            join(Laboratory, Person.laboratoryId == Laboratory.laboratoryId).\
            filter(Dewar.barCode == barcode).\
            order_by(desc(Dewar.dewarId)).\
            limit(1).\
            values(
                Laboratory.address,
                Laboratory.city,
                Laboratory.country
                )
        # Get first item in generator list
        shipment = next(records)

        results = {
            "address" : shipment[0],
            "city"    : shipment[1],
            "country" : shipment[2]
        }

    except DBAPIError:
        logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')

    except Exception:
        logging.getLogger('ispyb-logistics').error('No shipping record for this dewar: '+barcode)

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
               Dewar.facilityCode,
               Dewar.weight,
               Dewar.deliveryAgent_barcode,
               Proposal.title,
               Shipping.shippingName)

    return results

def get_instrument_from_dewar(dewarBarCode):
    """
    If there is no other indication of a target location from the barcode look up similar sessions
    This looks at the dewar => sessions and picks the most recent session with a beamline
    """
    results = None

    records = Dewar.query.join(Shipping).join(Proposal).join(BLSession).\
        filter(Shipping.shippingId == Dewar.shippingId).\
        filter(Proposal.proposalId == Shipping.proposalId).\
        filter(BLSession.proposalId == Proposal.proposalId).\
        filter(Dewar.barCode == dewarBarCode).\
        filter(BLSession.beamLineName != None).\
        order_by(desc(BLSession.sessionId)).\
        limit(1).\
        values(Dewar.dewarId,
               Dewar.barCode,
               Proposal.proposalCode,
               Proposal.proposalNumber,
               BLSession.beamLineName,
               BLSession.visit_number)

    try:
        firstRecord = next(records)

        logging.getLogger('ispyb-logistics').debug('get_instrument_from_dewar first: {}'.format(firstRecord))

        results = {
            'barcode': firstRecord.barCode,
            'visit_number': firstRecord.visit_number,
            'instrument': firstRecord.beamLineName,
            }
    except:
        logging.getLogger('ispyb-logistics').error('Could not get valid instrument from dewar {}'.format(dewarBarCode))

    return results

def get_lc_from_dewar(dewarBarCode):
    """
    Get the local contact name for a session associated with a dewar
    """
    results = {
            'barcode': dewarBarCode,
            'lc1': '',
            'email': '',
            }


    records = Dewar.query.join(BLSession).\
        filter(BLSession.sessionId == Dewar.firstExperimentId).\
        filter(Dewar.barCode == dewarBarCode).\
        limit(1).\
        values(Dewar.barCode,
               BLSession.beamLineOperator)

    try:
        firstRecord = next(records)

        logging.getLogger('ispyb-logistics').debug('get_lc_from_dewar first: {}'.format(firstRecord))

        lc1 = firstRecord.beamLineOperator.split(',')[0]
        lc1_title = lc1.split()[0]
        lc1_given_name = lc1.split()[1]
        lc1_family_name = '-'.join(lc1.split()[2:])
        lc1_email = lc1_given_name + '.' +lc1_family_name + email_domain
        results = {
            'barcode': firstRecord.barCode,
            'lc1': lc1,
            'email': lc1_email,
            }
    except:
        logging.getLogger('ispyb-logistics').error('Could not get valid local contact from dewar {}'.format(dewarBarCode))

    return results


def update_comments(dewarId, comments):
    """
    Redirect this request to SynchWeb to trigger e-mail alerts etc

    """
    # Test if this is actually a facility code
    return webservice.update_comments(dewarId, comments)

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

def is_arriving_at_ebic(location, previous_location):
    """
    Utility method to check if the location is EBIC-IN-*
    in which case we need to email LC
    Also check location has changed
    """
    if location == previous_location:
        return False

    result = False

    expr = re.compile(r'EBIC-IN-\d', re.IGNORECASE)
    match = expr.match(location)
    if match:
        result = True

    return result

def is_leaving_ebic(location):
    """
    Utility method to check if the location is EBIC-TO-STORES
    in which case we need to email LC
    """
    result = False

    expr = re.compile(r'EBIC-TO-STORES', re.IGNORECASE)
    match = expr.match(location)
    if match:
        result = True

    return result

