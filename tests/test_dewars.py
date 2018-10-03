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

import ispyb_api
from ispyb_api import db
from ispyb_api import controller
from ispyb_api.models import Dewar, DewarTransportHistory
from dewars.zone6 import rack_locations

class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True

        os.environ['ISPYB_CONFIG_FILE'] = 'test.cfg'
        os.environ['ISPYB_CONFIG_SECTION'] = 'ispyb_dev'

        ispyb_api.init_app(app)

        self.barcodes = ['sw19782-13-i03-0025656', 'SW19782-17-I24-0026897']

        return app

    def setUp(self):
        print("Setup")

    def tearDown(self):
        print("TearDown")
        db.session.remove()

    def test_find_dewars_by_barcode(self):
        for barcode in self.barcodes:
            result = controller.get_dewar_by_barcode(barcode)
            print result

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

        return results

if __name__ == "__main__":
    logger = logging.getLogger('ispyb-logistics')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    unittest.main()
