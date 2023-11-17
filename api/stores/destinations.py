# Storing list of instruments with their destinations here
class EBIC:
    destination = 'eBIC'
    proposal_codes = ['EM', 'BI']
    instruments = ['M01', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10', 'M11', 'M12', 'M13', 'M14']

class ZONE1:
    destination = 'Zone 1 Compound'
    proposal_codes = []
    instruments = ['M02']

class MX:
    destination = 'Zone 4 Store'
    proposal_codes = ['MX', 'LB', 'AU']
    instruments = ['I03', 'I04', 'I04-1', 'I19', 'I23', 'I24']

class I14:
    destination = 'I14'
    proposal_codes = ['SP']
    instruments = ['I14']

class I19:
    destination = 'I19'
    proposal_codes = ['CY']
    instruments = ['I19']

class SCM:
    destination = 'Lab 14'
    proposal_codes = []
    instruments = ['B21']




ALLDESTINATIONS = [I14, ZONE1, EBIC, SCM, I19, MX]  # order is important

def get_destination_from_barcode(barcode):
    barcode_prefix = barcode.upper()[0:2]
    destination = 'Unknown'
    for dest in ALLDESTINATIONS:
        if barcode_prefix in dest.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in dest.instruments):
            destination = dest.destination
            break

    return destination


def get_destination_from_instrument(instrument):
    destination = 'Unknown'
    for dest in ALLDESTINATIONS:
        if instrument.upper() in dest.instruments:
            destination = dest.destination
            break

    return destination


#
# Test logic to determine destination from barcode
#
if __name__ == "__main__":
    barcodes = [
        'cm1234-i13-1001', 
        'mx1234-b21-1001',
        'mx1234-i03-1001',
        'cm1234-m01-1001',
        'cm1234-m02-1001',
        'au1234-1001',
        'em1234-1001',
        'cm1234-i14-1001',
        'sp1234-1001',
    ]

    for barcode in barcodes:
        destination = get_destination_from_barcode(barcode)
        print("{} => {}".format(barcode, destination))

    instruments = [
        'i03',
        'm01',
        'm02',
        'i14',
        'b21',
    ]

    for instrument in instruments:
        destination = get_destination_from_instrument(instrument)
        print("{} => {}".format(instrument, destination))
