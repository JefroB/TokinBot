#########################################################################################################
##                                                                                                     ##
##                                           TOKIN' BOT                                                ##
##                                                                                                     ##
##                                     Written By: J.Bornhoeft                                         ##
##                                                                                                     ##
##                       A Bot to Buy and sell cryptocurrencies on Robinhood                           ##
##                                                                                                     ##
#########################################################################################################
import robin_stocks.robinhood as r
from globals import globals as g
from datafiles import read_order_file, read_crypto_positions_file
from os.path import exists

def get_open_order_by_id(id):
	if id is None:
		numberOfOpenOrders = 0
	else:		
		g.sleep(15)
		open_order = r.get_crypto_order_info(id)
		if open_order is None:
			numberOfOpenOrders = 0
		else:
			if open_order['state'] == 'filled' or open_order['state'] == 'canceled':
				numberOfOpenOrders = 0
			else:
				numberOfOpenOrders = 1
				print(numberOfOpenOrders, 'open order.')
				print(open_order['type'], 'OPEN ORDER PRICE:', open_order['price'])
				print('')
				print(open_order)
				print('')
	return numberOfOpenOrders


# this function needs work
def get_all_open_order_by_symbol(symbol):
	#
	# We only want 1 open sell order for any symbol at any time, so the order ID is written to a file.
	# If the file doesn't exist, we assume no open sell order exists.
	# If the file does exist, we call the get_open_order_id function to check the real number of
	# open sell orders matching the id from the file at robinhood (either 1 or 0).
	#
	filename = './sell_orders/' + symbol + '.txt'
	file_exists = exists(filename)
	if file_exists == True:
		id = read_order_file(symbol)
		numberOfOpenOrders = get_open_order_by_id(id)
	else:
		numberOfOpenOrders = 0
	
	if numberOfOpenOrders == 0:
		print('No Open Orders')
	print('')
	return numberOfOpenOrders	


def get_open_selling_positions_by_symbol(symbol):
	g.sleep(15)
	crypto_positions = read_crypto_positions_file()
	numberOfOpenPositions = 0
	i = 0
	while i < len(crypto_positions):
		if symbol == crypto_positions[i]['currency']['code'] and float(crypto_positions[i]['quantity_held_for_sell']) > 0:
			print('')
			print(crypto_positions[i]['quantity_held_for_sell'] + ' ' + crypto_positions[i]['currency']['code'])
			print('')
			numberOfOpenPositions = 1
		i += 1
	return numberOfOpenPositions	


def get_recent_order_id():
	open_order = r.get_all_open_crypto_orders()
	id = '0'
	if not open_order:
		id = open_order[0]['id']
	return id

