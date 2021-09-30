#!/usr/bin/env python3

import io
import json
import os
import sys
import time

CHAN_RATE = 400
CHAN_MIN_VALUE = 100000
CHAN_MAX_VALUE = 150000000
CHAN_OPEN_FEE = 500
OUR_NODE = '02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9'
OUR_ADDR = 'lndroutekytme3xds6cmbxaniretdgox2hk4cpu4k27jnub3gkfeuhqd.onion:9735'
CL_PROXY = '139.59.142.221:9735'

print('Hello! Welcome to LND ⚡ Routing!')
print('This script will help you request an incoming channel from us.')
print('')

local_pubkey = ''

lncli_exists = os.popen('which lncli').read().strip() != ''

if lncli_exists:

	local_pubkey = json.loads(os.popen('lncli getinfo').read().strip())['identity_pubkey']

	print('We found lncli. Would you like to check for updated fees and limits? This will send 3 sats,')
	print('and 1 will be returned in the response. This is to prevent fee siphoning from our node.')
	print('Receiving an update response also verifies your ability to receive refunds in case of failed channel opening.')
	print('')
	while True:
		update = input('Y: yes, N: no, C: check for response again without sending request (y/N/c): ').strip().upper()
		if update == 'N' or update == '':
			break
		if update == 'Y' or update == 'C':
			break
		print('Please enter Y, N, or C.')
	print('')

	if update == 'Y':
		print('Sending an update request. Please wait...')
		os.system('lncli sendpayment --keysend --dest ' + OUR_NODE + ' --amt 3 --data 1667785070=05,34349339=' + local_pubkey)
		time.sleep(5)

	if update == 'Y' or update == 'C':
		timeout = time.time() + 60
		params = ''

		while time.time() < timeout:
			invoices = json.loads(os.popen('lncli listinvoices').read().strip())['invoices']

			for invoice in invoices:
				if invoice['state'] == 'SETTLED' and int(invoice['settle_date']) > (time.time() - 600):
					for htlc in invoice['htlcs']:
						if '1667785071' in htlc['custom_records'] and '34349339' in htlc['custom_records']:
							if htlc['custom_records']['34349339'] == OUR_NODE and len(htlc['custom_records']['1667785071']) == 64:
								params = htlc['custom_records']['1667785071']
			if params != '':
				break

			time.sleep(5)

		if params != '':
			CHAN_RATE      = int(params[00:16], 16)
			CHAN_MIN_VALUE = int(params[16:32], 16)
			CHAN_MAX_VALUE = int(params[32:48], 16)
			CHAN_OPEN_FEE  = int(params[48:64], 16)

			print('')
			print('Got new parameters:')
			print('       Channel price: (chan_size * ' + str(1/CHAN_RATE) + ') + ' + str(CHAN_OPEN_FEE) + ' sats')
			print('Minimum channel size: ' + str(CHAN_MIN_VALUE) + ' sats')
			print('Maximum channel size: ' + str(CHAN_MAX_VALUE) + ' sats')
			print('')
		else:
			print('')
			print('Did not get parameter response before timeout. Your node must accept keysends, be routable, and appear in the graph in order to receive the response. (At least 1 public channel over a day old.) Channel opening will still function, but you must connect to us as a peer first.')
			print('Continuing without update. Press CTRL+C to cancel and restart if you would like to wait longer.')
			print('')


while True:
	node_pubkey = input('Enter the target node\'s public key or press ENTER for default (' + local_pubkey + '): ').strip()
	if node_pubkey == '' and len(local_pubkey) == 66:
		node_pubkey = local_pubkey
		break
	if len(node_pubkey) != 66:
		print('Invalid pubkey.')
		continue
	try:
		bytes.fromhex(node_pubkey)
	except ValueError:
		print('Invalid pubkey.')
		continue
	break

print('')

'''
if lncli_exists and node_pubkey == local_pubkey:
	existing_channels = os.popen('lncli listchannels').read()
	if OUR_NODE in existing_channels:
		print('You already have a channel open, please close it first.')
		sys.exit()
'''

while True:
	try:
		chan_val = int(input('Enter the desired channel size in satoshis: ').strip())
	except ValueError:
		print('Please enter a number.')
		continue
	if chan_val < CHAN_MIN_VALUE:
		print('Entered value less than minimum (' + str(CHAN_MIN_VALUE) + ').')
		continue
	if chan_val > CHAN_MAX_VALUE:
		print('Entered value greater than maximum (' + str(CHAN_MAX_VALUE) + ').')
		continue
	break
print('')

while True:
	pub_chan = input('Should this channel be public? (Y/n): ').strip().upper()
	if pub_chan == 'Y' or pub_chan == '':
		break
	if pub_chan == 'N':
		break
	print('Please enter Y or N.')
print('')

while True:
	send_msg = input('Would you like to send us a message? (y/N): ').strip().upper()
	if send_msg == 'N' or send_msg == '':
		break
	if send_msg == 'Y':
		break
	print('Please enter Y or N.')
print('')

if send_msg == 'Y':
	message = input('Enter your message: ').strip().encode('utf-8').hex()
	print('')

fee_prop = int(chan_val / CHAN_RATE)
fee = fee_prop + CHAN_OPEN_FEE

if pub_chan == 'Y':
	request_code = '01'
else:
	request_code = '02'

lncli1 = 'lncli sendpayment --keysend --amt ' + str(fee) + ' '
lncli2 = '    --dest ' + OUR_NODE + ' '
lncli3 = '    --data 1667785070=' + request_code + ',34349339=' + node_pubkey
if send_msg == 'Y':
	lncli3 = lncli3 + ',34349334=' + message

print('')
print('Requesting a ' + str(fee_prop * CHAN_RATE) + 'sat channel to ' + node_pubkey + ' for a fee of ' + str(fee) + ' satoshis.')
print('')
print('lncli connect ' + OUR_NODE + '@' + OUR_ADDR)
print('')
print(lncli1 + '\\')
print(lncli2 + '\\')
print(lncli3)
print('')

if lncli_exists:
	while True:
		do_it = input('Would you like us to do this for you? (y/N): ').upper()
		if do_it == 'N' or do_it == '':
			break
		if do_it == 'Y':
			break
		print('Please enter Y or N.')
	print('')

	if do_it == 'Y':
		print('Connecting to our node at ' + OUR_ADDR + '...')
		for i in range(3):
			connected = os.popen('lncli connect ' + OUR_NODE + '@' + OUR_ADDR + ' 2>&1').read().strip()
			if 'already connected' in connected:
				os.system(lncli1 + lncli2 + lncli3)
				break
		else:
			print('Could not connect to onion address. Trying clearnet proxy at ' + CL_PROXY + '...')
			for i in range(3):
				connected = os.popen('lncli connect ' + OUR_NODE + '@' + CL_PROXY + ' 2>&1').read().strip()
				if 'already connected' in connected:
					os.system(lncli1 + lncli2 + lncli3)
					break
			else:
				input('Could not connect to our node. Our node can attempt connecting to yours, but it must appear in the graph for channel opening and refunds to succeed. Press ENTER to continue or CTRL+C to abort.')
				os.system(lncli1 + lncli2 + lncli3)

