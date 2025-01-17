#
# Configuration for the I19 Storage Area
#

rack_locations = ['I19-STORAGE']
max_per_location = 8
suffixes = ["-{}".format(i) for i in range(1,max_per_location+1)]
beamline_locations = ['I19',
                      'I19-STORAGE',
                      'USER-COLLECTION',
                      'STORES-OUT',
                      'I19-TO-STORES',
                      'LN2TOPUP',
                      ]
