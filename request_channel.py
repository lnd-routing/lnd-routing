#!/usr/bin/env python3

import io
import json
import os

CHAN_RATE = 100
CHAN_MIN_VALUE = 50000
CHAN_MAX_VALUE = 100000000
CHAN_OPEN_FEE = 500
OUR_NODE = '02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9'
OUR_ADDR = 'hgjdgzq7h6e32anpkiveobx4coihxg4buzcevsxqr6lcj35stzszicad.onion:9735'

lncli_exists = os.popen('which lncll').read().strip() != ''

if lncli_exists:
	local_pubkey = json.loads(os.popen('lncli getinfo').read().strip())['identity_pubkey']
else:
	local_pubkey = ''

while True:
	node_pubkey = input('Enter your node\'s public key (' + local_pubkey + '): ')
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

while True:
	try:
		chan_val = int(input('Enter the desired channel size in satoshis: '))
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
	send_msg = input('Would you like to send us a message? (y/N): ').upper()
	if send_msg == '' or send_msg == 'N':
		break
	if send_msg == 'Y':
		break
	print('Please enter Y or N.')
print('')

if send_msg == 'Y':
	message = input('Enter your message: ').encode('utf-8').hex()
	print('')

fee_prop = int(chan_val / CHAN_RATE)
fee = fee_prop + CHAN_OPEN_FEE


lncli1 = 'lncli sendpayment --keysend --amt ' + str(fee) + ' '
lncli2 = '    --dest ' + OUR_NODE + ' '
lncli3 = '    --data 1667785070=01,34349339=' + node_pubkey
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
		if do_it == '' or do_it == 'N':
			break
		if do_it == 'Y':
			break
		print('Please enter Y or N.')
	print('')

	if do_it == 'Y':
		os.system('lncli connect ' + OUR_NODE + '@' + OUR_ADDR)
		os.system(lncli1 + lncli2 + lncli3)
