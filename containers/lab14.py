#
# Configuration for the Lab 14 Storage Area
#
prefixes = ['ULT', 'RT', 'RF']

positions = ["{}".format(i) for i in range(1,6)]

rack_locations = []

# Build the list of TRAY-01A, TRAY-01B, TRAY-01C...
for prefix in prefixes:
  rack_locations.extend(''.join([prefix, '-', pos]) for pos in positions)

beamline_locations = ['I22',
                      'B21',
                      ]

if __name__ == "__main__":
  print("Rack locations: {}".format(rack_locations))
  print("Beamline locations: {}".format(beamline_locations))