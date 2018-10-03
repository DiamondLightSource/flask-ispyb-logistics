import sys
import logging

from ispyb_api import controller

facilitycodes = ['DLS-MX-0001', 'dls-mx-0001', 'DLS-EM-0000', 'AAA-AA-12345']
not_facilitycodes = ['dls-mx-1', 'DL-MX-1234', 'DLS-MX-AA00', 'aaa-a-1', 'cm123245-1-i01-12345']

tests = facilitycodes + not_facilitycodes

if __name__ == "__main__":
    logger = logging.getLogger('ispyb-logistics')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    for test in tests:
        controller.is_facility_code(test)
    