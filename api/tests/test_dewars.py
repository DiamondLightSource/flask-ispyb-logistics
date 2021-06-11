import os
import sys
import logging
import logging.handlers

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import desc, func

import unittest
from flask import Flask
from flask_testing import TestCase

# We are not a package and the intent is to run this from the parent dir
sys.path.append('../')

from api.ispyb_api import init_app
from api.ispyb_api import db
from api.ispyb_api import controller
from api.ispyb_api.models import Dewar, DewarTransportHistory
from api.ispyb_api.models import Shipping, LabContact, Person, Laboratory

from api.dewars.zone6 import rack_locations

class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True

        os.environ['ISPYB_CONFIG_FILE'] = 'tests/test.cfg'
        os.environ['ISPYB_CONFIG_SECTION'] = 'ispyb_dev'

        init_app(app)

        self.barcodes = ['mx1005-0008799'] #sw19782-13-i03-0025656', 'SW19782-17-I24-0026897']

        return app

    def setUp(self):
        print("Setup")

    def tearDown(self):
        print("TearDown")
        db.session.remove()

    def test_find_dewars_by_barcode(self):
        for barcode in self.barcodes:
            result = controller.get_dewar_by_barcode(barcode)
            print(result)

    def test_find_dewars_by_location(self):
        """
        This method will find a dewar based on its location.
        """
        locations = ['RACK-X1', 'RACK-D1', 'RACK-D2']
        results = {}

        logging.getLogger('ispyb-logistics').debug("find_dewars_by_location {}".format(','.join(locations)))

        try: 
            # Query for dewars with transporthistory locations in the list
            # Use case insensitive search for storageLocation
            # Get the timestamp and location from the transport history 
            # The Dewar storageLocation does not always match the transport history
            dewars = DewarTransportHistory.query.join(Dewar).filter(func.lower(Dewar.storageLocation).in_(locations)).\
                filter(Dewar.dewarId == DewarTransportHistory.dewarId).\
                order_by(desc(DewarTransportHistory.arrivalDate)).\
                values(Dewar.dewarId, Dewar.barCode, Dewar.storageLocation, DewarTransportHistory.DewarTransportHistoryId, DewarTransportHistory.arrivalDate)

            for dewar in dewars:
                if dewar.storageLocation in results:
                    logging.getLogger('ispyb-logistics'),debug("Ignoring duplicate entry for dewar {} to location {} at time {}".format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
                else:
                    logging.getLogger('ispyb-logistics'),debug("Adding dewar {} to {} at time {}".format(dewar.barCode, dewar.storageLocation, dewar.arrivalDate))
                    results[dewar.storageLocation] = [dewar.barCode, dewar.arrivalDate]
    
        except NoResultFound:
            logging.getLogger('ispyb-logistics').error("Error retrieving dewars")

        print(results)

    def test_find_shipping_return_address(self):
        # Get the return lab address for this dewar.
        # Dewar=>Shipping=>LabContact=>Laboratory
        barcode = self.barcodes[0]
        results = None
        try:
            results = Dewar.query.join(Shipping, Dewar.shippingId == Shipping.shippingId).\
                join(LabContact, Shipping.returnLabContactId == LabContact.labContactId).\
                join(Person, LabContact.personId == Person.personId).\
                join(Laboratory, Person.laboratoryId == Laboratory.laboratoryId).\
                filter(Dewar.barCode == barcode).\
                order_by(desc(Dewar.dewarId)).\
                values(
                    Dewar.dewarId, 
                    Person.givenName,
                    Person.familyName,
                    Laboratory.address,
                    Laboratory.city,
                    Laboratory.country
                    )
        except NoResultFound:
            logging.getLogger('ispyb-logistics').error('Database API Exception - no route to database host?')

        for r in results:
            print(r)

if __name__ == "__main__":
    logger = logging.getLogger('ispyb-logistics')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    unittest.main()
