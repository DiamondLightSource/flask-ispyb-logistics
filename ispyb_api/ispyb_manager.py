import os
import glob
from datetime import datetime

import ispyb.factory

config_file = os.environ['ISPYB_CONFIG_FILE']


class ISPyBManager(object):
    """
    This is used by dewars and ebic to get proposals and dewars
    Rather than duplicate the functions, wrapped in a class to 
    specialise the methods for the locations e.g. RACK vs EBIC-RACK 

    If ebic beamlines are m01, m02, m03...
    If other (mx) beamlines are i01, i02, i03...

    beamline_prefix is 'BEAMLINE' or 'MICROSCOPE'

    rack_prefix = 'RACK' or 'EBIC_RACK'
    """

    def __init__(self, beamlines=[], beamline_prefix='BEAMLINES', rack_prefix='RACK'):
        self.rack_prefix = rack_prefix
        self.beamline_prefix = beamline_prefix
        self.beamlines = beamlines

    def checkDewars(self, data):
        """
        Not really a 'check'.
        This is an update / synch operation between the json file and ISPyB
        getDewars is the method that gets dewars for the active proposals (i.e. this year with a filesystem reference)
        """
        dewars = self.getDewars()

        for key in data.keys():
            if not key.startswith(self.rack_prefix):
                continue
            try:
                barcode = data[key][0]
            except:
                continue
            if barcode != "":
                for dewar in dewars:
                    if dewar['barCode'] is not None and dewar['barCode'].upper() == barcode.upper():
                        location = dewar['storageLocation']
                        status = dewar['status']
                        if (location is not None and location != key and location != key + '-FROM-BL') or (status != 'at DLS' and status != 'at facility'):
                            data[key] = ['', 0]
        return data

    def getProposals(self, proposals=[]):
        """
        Get All proposals in this year that are on filesystem

        This is only required to help find a dewar and update its location
        """
        year = datetime.strftime(datetime.now(), '%Y')

        for beamline in self.beamlines:
            for visit in glob.glob('/dls/' + beamline + '/data/' + year + '/*'):
                proposals.append(visit.split('/')[-1].split('-')[0])

        return set(proposals)

    def getDewars(self, proposals=[]):
        """
        Get Dewar status from ISPyB for all current proposals
        """
        proposals = self.getProposals(proposals)

        dewars = []

        with ispyb.open(config_file) as conn:
            shipping = ispyb.factory.create_data_area(
                ispyb.factory.DataAreaType.SHIPPING, conn)

            for proposal in proposals:
                try:
                    mx = proposal[0:2]
                    number = int(proposal[2:])
                    dewars.extend(
                        shipping.retrieve_dewars_for_proposal_code_number(mx, number))
                except:  # except ispyb.exception.ISPyBNoResultException:
                    print("ISPyB - no dewars found for proposal {}".format(proposal))
        return dewars

    def setLocation(self, barcode, location, awb=None):
        """
        Update the location of this dewar in ISPyB
        """
        # new proposals dont have a data dir yet, so force it to be included
        proposal = barcode.lower().split('-')[0]
        dewars = self.getDewars([proposal])

        print("Set Location, proposal = {}".format(proposal))
        print("Set Location, dewar = {}".format(dewars))
        # Looks like we can split this into a loop to find the dewar,
        # Then if found, carry out the logic to update ispyb
        matching_dewar = None

        for dewar in dewars:
            if dewar['barCode'] is not None and dewar['barCode'].upper() == barcode.upper():
                matching_dewar = dewar
                break;

        if matching_dewar is not None:
            with ispyb.open(config_file) as conn:
                shipping = ispyb.factory.create_data_area(
                    ispyb.factory.DataAreaType.SHIPPING, conn)

                params = shipping.get_dewar_params()
                params['id'] = matching_dewar['id']
                params['type'] = matching_dewar['type']
                params['status'] = 'at facility'

                #
                # This needs to be looked at - beamline locations are similar to the beamlines passed in
                # but are in a different form M01 instead of MICROSCOPE-M01
                #  If EBIC strip off MICROSCOPE, if mx strip off BEAMLINE to get list...?
                #
                # -FROM-BL used to denote that the dewar has been used at a beamline...
                if (matching_dewar['storageLocation'] is not None and (matching_dewar['storageLocation'].upper().startswith(self.beamline_prefix) or matching_dewar['storageLocation'].upper() in [x.upper() for x in self.beamlines])) or (matching_dewar['status'] is not None and matching_dewar['status'].lower() == 'processing'):
                    params['storagelocation'] = location + '-FROM-BL'
                else:
                    params['storagelocation'] = location

                if awb is not None and len(awb) > 5:
                    params['trackingnumberfromsynchrotron'] = awb

                dewarid = shipping.upsert_dewar(list(params.values()))
        else:
            dewarid = None

        return dewarid
