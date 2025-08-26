#
# Configuration for the Zone4 Storage Area
#
rack_prefix = 'TRAY-'

# 16 normal trays with A-F
num_trays = 16
positions = 'A B C D E F'.split()

rack_locations = []

# Build a list of trays numbers (As string)
trays = ["{}".format(i) for i in range(1,num_trays+1)]

# Build the list of TRAY-01A, TRAY-01B, TRAY-01C...
for tray in trays:
  rack_locations.extend(''.join([rack_prefix, tray, pos]) for pos in positions)

# Extend with Tray 17 A-P
positions.extend('G H I J K L M N O P'.split())

rack_locations.extend(''.join([rack_prefix+str(num_trays + 1), pos]) for pos in positions)

beamline_locations = ['I03',
                      'I04',
                      'I04-1',
                      'I19',
                      'I19-STORAGE',
                      'I23',
                      'I24',
                      'I02-1',
                      'I02-2',
                      'USER-COLLECTION',
                      'STORES-OUT',
                      'ZONE4-TO-STORES',
                      'ZONE4-CAGE',
                      'EBIC',
                      'LN2TOPUP',
                      ]
