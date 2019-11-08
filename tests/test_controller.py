import os
import sys
import logging
import logging.handlers

import unittest
from flask import Flask
from flask_testing import TestCase
import json

# Run this from the parent dir
# Run with python -m tests/test_controller

import ispyb_api
from ispyb_api import db
from ispyb_api import models
from ispyb_api import controller
from dewars.zone6 import rack_locations
from dewars.zone4 import rack_locations as zone4_locations

class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True

        os.environ['ISPYB_CONFIG_FILE'] = 'tests/test.cfg'
        os.environ['ISPYB_CONFIG_SECTION'] = 'ispyb_dev'

        self.logger = logging.getLogger('ispyb-logistics')

        ispyb_api.init_app(app)

        return app

    def setUp(self):
        print("Setup")
        self.facilitycode = 'DLS-MX-0001'
        self.locations = ['RACK-A1', 'RACK-A2', 'RACK-A3']

    def tearDown(self):
        print("TearDown")
        db.session.remove()

    def test_get_dewar_by_facilitycode(self):
        self.logger.debug("Test Get Dewars for facilitycode {}".format(self.facilitycode))
        result = controller.get_dewar_by_facilitycode(self.facilitycode)
        self.logger.debug(result)
        self.assertIsNotNone(result)

    def test_get_dewars_by_locations(self):
        self.logger.debug("Test Get Dewars for locations {}".format(','.join(self.locations)))
        result = controller.find_dewars_by_location(self.locations)
        self.assertIsNotNone(result)

    def test_get_dewar_history_by_locations(self):
        self.logger.debug("Test Get Dewar History for locations {}".format(','.join(zone4_locations)))
        result = controller.find_dewar_history_for_locations(zone4_locations, max_entries=-1, match_locations = False)
        self.logger.debug(json.dumps(result, indent=4, sort_keys=True))
        self.assertIsNotNone(result)

    def test_get_dewar_history_by_locations(self):
        self.logger.debug("Test Get Dewar History for locations {}".format(','.join(zone4_locations)))
        result = controller.find_recent_storage_history(zone4_locations)
        self.logger.debug(json.dumps(result, indent=4, sort_keys=True))
        self.assertIsNotNone(result)


if __name__ == "__main__":
    logger = logging.getLogger('ispyb-logistics')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    unittest.main()