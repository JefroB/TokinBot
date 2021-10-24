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
import os
import sys
import json
import datetime
import time


def get_crypto_historicals(symbol, return_int, span_length):
	#g.sleep(15)
	history =  r.crypto.get_crypto_historicals(symbol, interval=return_int, span=span_length, bounds='24_7', info=None)
	return history


def str_to_class(str):
    return getattr(sys.modules[__name__], str)


def create_order_file(symbol, id):
	filename = './sell_orders/' + symbol + '.txt'
	write_json_file(filename, id)


def read_order_file(symbol):
	filename = './sell_orders/' + symbol + '.txt'
	id = read_json_file(filename)
	return id


def export_reports():
	print('Exporting Reports...')
	now = datetime.datetime.now()
	date = now.strftime('%b-%d-%Y')

	crypto_report = './reports/crypto/crypto_orders_' + date +'.csv'
	if crypto_report == False:
		r.export.export_completed_crypto_orders('./reports/crypto/')

	stock_report = './reports/stocks/stock_orders_' + date +'.csv'
	if stock_report == False:
		r.export.export_completed_stock_orders('./reports/stocks/')


def eat_breakfast():
	breakfast = './breakfast/hashbrowns.txt'
	full_belly = read_json_file(breakfast)
	return full_belly
	

def build_data_file(symbol, span, length):
	filename = './data/' + symbol + '-'+ span + '.json'
	print('Gathering data...')

	# The Daily data is only needed once a day, so check the file creation date for that file
	if span == 'day':
		replace_file = is_file_older_than_x_days(filename)
	else:
		replace_file = True

	# if the daily file is over 24 hours old recreate it. Always recreate the 5 min file.
	if replace_file == True:
		data = get_crypto_historicals(symbol, span, length)
		sorted_data = sorted(data, key=lambda d: d['begins_at'], reverse=True)

		record_count = len(sorted_data)
		if record_count == 0:
			print(g.colored('Something bad happened while fetching the ' + span + ' data for ' + symbol, 'red'))

		write_json_file(filename, sorted_data)


def is_file_older_than_x_days(filepath, days=1):
    file_time = g.os.path.getmtime(filepath) 
    # Check against 24 hours 
    return ((time.time() - file_time) / 3600 > 24*days)
	

def transactions_file (symbol, new_line):
	filename = './transactions/' + symbol + '.csv'
	f = open(filename, "a")
	f.write(new_line)
	f.close()


def read_data_file(symbol, span):
	filename = './data/' + symbol + '-'+ span +'.json'
	file_data = read_json_file(filename)
	return file_data
	

def build_data_files(symbol):
	build_data_file(symbol, '5minute', 'week')
	build_data_file(symbol, 'day', 'year')


def create_strategy(symbol, min, max):
	med = (((max - min) / 2) + min)
	params = dict()
	params['big_buy_amt'] = max
	params['med_buy_amt'] = med
	params['small_buy_amt'] = min
	filename = './strategies/' + symbol + '.json'
	write_json_file(filename, params)


def get_strategy(symbol):
    filename = './strategies/' + symbol + '.json'
    file_data = read_json_file(filename)
    return file_data


def get_crypto_positions():
	positions = r.get_crypto_positions()
	filename = './data/crypto_positions.json'
	write_json_file(filename, positions)


def read_crypto_positions_file():
	filename = './data/crypto_positions.json'
	file_data = read_json_file(filename)
	return file_data


def read_coins_file():
	filename = './strategies/coins.json'
	file_data = read_json_file(filename)
	return file_data


def write_json_file(filename, data):
	jsonstr = json.dumps(data)
	f = open(filename,"w+")
	f.write(jsonstr)
	f.close()

def read_json_file(filename):
	f = open(filename, "r")
	if f.mode == 'r':
		json_data =f.read()
		file_data = json.loads(json_data)
	f.close()
	return file_data
