#
# Configuration for the Zone4 Storage Area
#
rack_prefix = 'TRAY'

num_trays = 17
positions = ['A', 'B', 'C', 'D', 'E', 'F']

rack_locations = []

# Build a list of trays numbers (As string)
trays = ["{:02d}".format(i) for i in range(1,num_trays+1)]

# Build the list of TRAY-01A, TRAY-01B, TRAY-01C...
for tray in trays:
  rack_locations.extend(''.join(['TRAY-', tray, pos]) for pos in positions)

beamline_locations = ['I03',
                      'I04',
                      'I04-1',
                      'I19',
                      'I24',
                      'USER-COLLECTION',
                      'STORES-OUT',
                      'EBIC'
                      ]
