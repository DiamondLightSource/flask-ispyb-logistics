#
# Configuration for the Lab 14 Storage Area
#
rack_prefix = 'TRAY'

# 16 normal trays with A-F
num_trays = 16
positions = 'A B C D E F'.split()

rack_locations = []

# Build a list of trays numbers (As string)
trays = ["{}".format(i) for i in range(1,num_trays+1)]

# Build the list of TRAY-01A, TRAY-01B, TRAY-01C...
for tray in trays:
  rack_locations.extend(''.join(['TRAY-', tray, pos]) for pos in positions)

beamline_locations = ['I22',
                      'B21',
                      'USER-COLLECTION',
                      'STORES-OUT',
                      ]