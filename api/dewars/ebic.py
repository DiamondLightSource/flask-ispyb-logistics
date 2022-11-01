#
# Configuration for the Zone4 Storage Area
#
# # Build list of rack locations e.g. EBIC-IN-[1..20]
rack_locations = ['EBIC-IN-{}'.format(i) for i in range(1,28)]

beamlines = ['m01',
             'm02',
             'm03',
             'm04',
             'm05',
             'm06',
             'm07',
            ]

beamline_prefix = 'MICROSCOPE'

beamline_locations = ['{}-{}'.format(beamline_prefix, x.upper()) for x in beamlines]

# Add the common locations on for the web ui
beamline_locations.extend(['USER-COLLECTION',
                           'STORES-OUT',
                           'ZONE-4-STORE',
                           'ZONE-6-STORE',
                           'EBIC-TO-STORES',
                           'LN2TOPUP',
                           ])

