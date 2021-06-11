import re
import logging
import itertools
import datetime

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc, func
from sqlalchemy.orm import aliased

from . import db
from . import webservice
from .models import Container, ContainerHistory, Dewar, Shipping

# What age do we ignore container history entries
CONTAINER_FILTER_DAYS_LIMIT = 30

def set_container_location(barcode, location):
    """
    Redirect this request to SynchWeb to trigger e-mail alerts etc

    This might be a facility code (if the label is unreadable)
    So first check if this is a facility code, then use the actual barcode
    """
    # Test if this is actually a facility code
    return webservice.set_container_location(barcode, location)

def set_container_location_from_id(id, location):
    """
    Redirect this request to SynchWeb to trigger e-mail alerts etc

    This might be a facility code (if the label is unreadable)
    So first check if this is a facility code, then use the actual barcode
    """
    return webservice.set_container_location_from_id(id, location)

def find_containers_by_location(locations):
    """
    This method will find the most recent container stored in each location.
    It matches the Container.storageLocation with ContainerHistory.storageLocation
    """
    logging.getLogger('ispyb-logistics').debug("find_containers_by_location {}".format(','.join(locations)))

    results = {}

    filter_after = datetime.datetime.today() - datetime.timedelta(days = CONTAINER_FILTER_DAYS_LIMIT)

    try:
        # Query for containers with containerhistory locations in the list
        # Use case insensitive search for storageLocation
        # Get the timestamp and location from the transport history
        # Order so we get the most recent first...
        # The Dewar storageLocation does not always match the transport history
        containers = Container.query.join(ContainerHistory).\
            filter(func.lower(ContainerHistory.location).in_(locations)).\
            filter(Container.containerId == ContainerHistory.containerId).\
            filter(func.lower(Container.beamlineLocation) == func.lower(ContainerHistory.location)).\
            filter(ContainerHistory.blTimeStamp >= filter_after).\
            group_by(Container.containerId,ContainerHistory.location).\
            order_by(desc(ContainerHistory.containerHistoryId)).\
            values(Container.containerId,
                   Container.barcode,
                   Container.code,
                   ContainerHistory.blTimeStamp,
                   ContainerHistory.location,
                   ContainerHistory.status,
                   )

        for container in containers:
            payload = {
                'id': container.containerId,
                'code': container.code,
                'barcode': container.barcode,
                'arrivalDate': container.blTimeStamp.isoformat(),
                'status': container.status,
                'location': container.location
            }
            # If we already have an entry, it means there is a more recent change for a dewar in this location
            # Note we store the data in upper case - SynchWeb uses lower case while the UI requests data in upper case...
            if container.location.upper() in results:
                logging.getLogger('ispyb-logistics').debug('Appending entry for container {} location {} at {}'.format(container.barcode, container.location, container.blTimeStamp))
                results[container.location.upper()].append(payload)
            else:
                logging.getLogger('ispyb-logistics').debug('Found entry for this container {} in {} at {}'.format(container.barcode, container.location, container.blTimeStamp))

                results[container.location.upper()] = []
                results[container.location.upper()].append(payload)
    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error retrieving dewars")
    except DBAPIError:
        logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')
        results = None

    return results

def find_container_by_barcode(barcode):
    """
    This method will find a container based on its barcode.
    Code is set for registered containers but barcode isn't.
    New containers will have a name which == code, so we are using code here

    It enforces only one result and will throw an error if there is not one.
    """
    logging.getLogger('ispyb-logistics').info("find_container_by_barcode {}".format(barcode))
    result = {}

    try:
        records = Container.query.join(Dewar).join(Shipping).\
            filter(Dewar.dewarId == Container.dewarId).\
            filter(Shipping.shippingId == Dewar.shippingId).\
            filter(Container.code == barcode).\
            order_by(desc(Container.containerId)).\
            values(Shipping.shippingName,
                   Container.containerId,
                   Container.code,
                   Container.storageTemperature,
                   Container.beamlineLocation.label('location'),
                   )

        container = next(records)

        result['shippingName'] = container.shippingName
        result['id'] = container.containerId
        result['code'] = container.code
        result['storageTemperature'] = container.storageTemperature
        result['location'] = container.location
        
    except NoResultFound:
        logging.getLogger('ispyb-logistics').error("Error container barcode {} does not exist in ISPyB".format(barcode))

    return result

