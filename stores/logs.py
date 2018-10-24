import json
import collections

# The maximum number of dewars recorded in the web page
max_stores_dewars = 10


def writeJsonFile(filename, data):
    """
    Dump the provided data to a json file
    """
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=0, sort_keys=True)
    except IOError:
        print("Error writing to json file %s" % filename)


def readJsonFile(filename):
    """
    Extract json data from the filename
    """
    try:
        with open(filename, 'r') as jsonfile:
            data = json.load(jsonfile)
            return data
    except IOError:
        print("Error reading json file: %s - using blank list" % filename)
        return []


def writeStoresFile(filename, data):
    """
    Dump the last 10 (max_stores_dewars) dewars processed to a json file

    Parameters:
    data - a collections.deque representing the dewar list
    """
    if len(data) is not max_stores_dewars:  # Warn for now, could raise as an error?
        print("Warning: dewar list for stores log file not of correct length (expected %d) " %
              max_stores_dewars)

    json_data = []

    for item in data:
        json_data.append(item)

    writeJsonFile(filename, json_data)


def readStoresFile(filename):
    """
    Read the dewar list and return a deque collection
    """
    json_data = readJsonFile(filename)

    dewar_list = collections.deque({}, max_stores_dewars)

    for item in json_data:
        dewar_list.append(item)

    return dewar_list


def _test_stores():
    import time

    test_stores_file = 'test_stores.json'

    data = collections.deque({}, max_stores_dewars)

    for i in range(max_stores_dewars):
        data.appendleft({'barcode': 'DLS-MX-12345',
                         'date': time.strftime('%a %d %b, %H:%M:%S'),
                         'inout': 'RACK-A%d' % i,
                         'destination': 'STORES-OUT',
                         'awb': '1234567890'})

    writeStoresFile(test_stores_file, data)

    # Test we can get back what we wrote
    print("Stores File Test:")
    print readStoresFile(test_stores_file)


def _test_json():
    data = {'BEAMLINE-I03': ['DLS-MX-12345', 'DLS-MX-23456', 'DLS-MX-34567'],
            'BEAMLINE-I04': ['MX12345-13-I04-00223344']}
    jsonfile = 'tmp_file.json'

    # First test should fail
    result = readJsonFile(jsonfile)
    if result:
        print(result)
    # Dump contents
    writeJsonFile(jsonfile, data)


if __name__ == '__main__':
    _test_json()

    _test_stores()
