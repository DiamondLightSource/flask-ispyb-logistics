# Storing list of instruments with their destinations here
class EBIC:
    destination = 'eBIC'
    proposal_codes = ['EM', 'BI']
    instruments = ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10', 'M11', 'M12']

class MX:
    destination = 'Zone 4 Store'
    proposal_codes = ['MX']
    instruments = ['I02-2', 'I03', 'I04', 'I04-1', 'I19', 'I23', 'I24']

class I14:
    destination = 'I14'
    proposal_codes = ['SP']
    instruments = ['I14']

#
# Test logic to determine destination from barcode
#
if __name__ == "__main__":
    barcodes = [
        'cm1234-i13-1001', 
        'cm1234-i03-1001', 
        'mx1234-i03-1001',
        'cm1234-m03-1001',
        'em1234-i03-1001',
        'cm1234-i14-1001',
        'sp1234-i14-1001',
    ]

    for barcode in barcodes:

        barcode_prefix = barcode.upper()[0:2]

        if barcode_prefix in I14.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in I14.instruments):
            destination = I14.destination
        elif barcode_prefix in EBIC.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in EBIC.instruments):
            destination = EBIC.destination
        elif barcode_prefix in MX.proposal_codes or any('-{}'.format(b) in barcode.upper() for b in MX.instruments):
            destination = MX.destination
        else:
            destination = 'Unknown'

        print("{} => {}".format(barcode, destination))