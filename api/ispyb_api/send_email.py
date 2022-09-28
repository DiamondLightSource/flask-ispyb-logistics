import os
import smtplib
from email.mime.text import MIMEText

ebic_industry_emails = os.environ.get('EMAIL_ADDRESSES_EBIC_INDUSTRY', '')
ebic_academic_emails = os.environ.get('EMAIL_ADDRESSES_EBIC_ACADEMIC', '')
email_domain = os.environ.get('EMAIL_DOMAIN', '@diamond.ac.uk')
smtp_server = os.environ.get('SMTP_SERVER', 'localhost')

def get_cc_addresses(barcode):
	if barcode[0:2].lower() == 'in' or barcode[0:2].lower() == 'sw':
		return ebic_industry_emails
	else:
		return ebic_academic_emails


def email_lc(barcode, lc_details):
	msg = MIMEText('Dear '+lc_details['lc1']+',\n\nA dewar with barcode '+barcode+' has arrived at the eBIC storage area.\n\nMany thanks.')
	msg['From'] = 'no-reply' + email_domain
	msg['Subject'] = 'Dewar arrived at eBIC storage area'
	msg['To'] = lc_details['email']
	msg['CC'] = get_cc_addresses(barcode)
	do_send_email(msg)


def email_stores(barcode):
	msg = MIMEText('Dear Goods Handling,\n\nA dewar with barcode '+barcode+' has returned to the eBIC storage area. Please arrange to collect it ready for shipment.\n\nMany thanks.')
	msg['From'] = 'no-reply' + email_domain
	msg['Subject'] = 'Dewar ready at eBIC storage area'
	msg['To'] = 'Goodshandling' + email_domain
	msg['CC'] = get_cc_addresses(barcode)
	do_send_email(msg)


def do_send_email(msg):
	s = smtplib.SMTP(smtp_server, 25)
	s.sendmail(msg['From'], msg['To'].split(',') + msg['CC'].split(','), msg.as_string())
	s.quit()

