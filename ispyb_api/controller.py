from sqlalchemy.orm.exc import NoResultFound

from models import Dewar, Shipping, Proposal
import webservice


def set_location(barcode, location, awb=None):
    """
    Redirect this request to SynchWeb
    """
    return webservice.set_location(barcode, location, awb)

def get_dewar_by_facilitycode(fc):
    """
    This method will find a dewar based on its facilitycode.
    """
    result = None

    print "FIND METHOD: FacilityCode = ", fc

    d = Dewar.query.filter_by(FACILITYCODE = fc).first()

    if d:
        result = {'barcode': d.barCode,  'storageLocation': d.storageLocation}
    else:
        print("Could not find dewar with FacilityCode {}".format(fc))

    return result

def get_dewar_by_barcode(barcode):
    """
    This method will find a dewar based on its barcode.

    It enforces only one result and will throw an error if there is not one.
    """
    result = {}

    try: 
        d = Dewar.query.filter_by(barCode = barcode).one()

        result['dewarId'] = d.dewarId
        result['barCode'] = d.barCode
        result['storageLocation'] = d.storageLocation
        result['facilityCode'] = d.FACILITYCODE

    except NoResultFound:
        print("Error this barcode does not exist in ISPyB")

    return result

def find_dewars_by_location(locations):
    """
    This method will find a dewar based on its location.
    """
    print("find_dewars_by_location {}".format(','.join(locations)))
    results = {}

    try: 
        dewars = Dewar.query.filter(Dewar.storageLocation.in_(locations)).\
        values(Dewar.dewarId, Dewar.barCode, Dewar.FACILITYCODE, Dewar.storageLocation)

        for dewar in dewars:
            results[dewar.storageLocation] = [dewar.barCode, ""]

    except NoResultFound:
        print("Error retrieving dewars")

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