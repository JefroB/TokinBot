import robin_stocks.robinhood as r
from pyotp import TOTP as otp
from checkpricing import go_shopping, price_direction_over_last_5min, get_target_buy_and_sell_prices, current_price
from openorders import get_open_selling_positions_by_symbol, get_open_order_by_id
from datafiles import create_order_file, export_reports, build_data_files, transactions_file, get_strategy, get_crypto_positions, read_coins_file
from keys import decrypt_file
from globals import globals as g
from art import ascii, header_art, high_rent


def login():
	eat_this = './breakfast/sausage.txt'
	grains = decrypt_file('./breakfast/toast.txt')
	dairy = decrypt_file('./breakfast/eggs.txt')
	key = decrypt_file(eat_this)
	totp = otp(key).now()
	r.authentication.login(grains, dairy, store_session=True, mfa_code=totp)


def logout():
	r.logout()


def do_it_all(symbol):
	header_art(symbol)
	build_data_files(symbol)
	params = get_strategy(symbol)

	if get_open_selling_positions_by_symbol(symbol) == 1:
		print(g.colored('You\'ve got an open position broseph! Can\'t do it.', 'red'))
	else:
		# If the price isn't going up in the last few mins it might be crashing. Just stop here.
		# Idaeally, we want to buy just after the price goes down, but just as (or right after) it starts going up.
		cur_price = current_price(symbol)
		if 	price_direction_over_last_5min(symbol, cur_price) == 'up':
			print('let\'s go shopping!')
			print('...checking market conditions.')
			purchase = go_shopping(symbol)
			choose_purchase_amt(symbol, purchase, params)

		else:
			print(g.colored('The price is down over the last 5 min, let\'s wait it out.', 'cyan'))
			g.sleep(15)


def choose_purchase_amt(symbol, purchase, params):
	if purchase == 'big buy':
		purchase_descision(symbol, params['big_buy_amt'])
	elif purchase == 'med buy':
		purchase_descision(symbol, params['med_buy_amt'])
	elif purchase == 'small buy':
		purchase_descision(symbol, params['small_buy_amt'])
	else:
		print('Goodbye')
	


# Is the current price over the target price?
#
# THIS NEEDS TO LOG DATA TO A CSV 
#
def purchase_descision(symbol, dollarAmt):
	target_buy_and_sell_prices = get_target_buy_and_sell_prices(symbol)
	current_price = g.Decimal(r.crypto.get_crypto_quote(symbol)['ask_price'])
	current_price_text = str(current_price)
	print(g.colored('The Current Price is: $' + current_price_text, 'yellow'))

	if current_price < target_buy_and_sell_prices[0]:
		order_crypto(symbol, dollarAmt, target_buy_and_sell_prices)
	else:
		# the current price is above out target, 
		# show the high rent screen
		#g.cls()
		high_rent()
		g.sleep(15)


def order_crypto(symbol, dollarAmt, target_buy_and_sell_prices):
		# convert dollar amount to float for JSON
		amountInDollars = float(dollarAmt)

		# place buy order
		r.orders.order_buy_crypto_by_price(symbol, amountInDollars, timeInForce='gtc')

		# get the bought price. We should probably see if the cypto is actually owned
		bought_price = g.Decimal(r.orders.get_all_crypto_orders(info=None)[0]['price']).quantize(g.Decimal('1.000000'))

		#
		# limit price is 80% of daily fluctuation + bought_price
		# This is the target sale price
		# We are targeting less than the average daily price fluxuation to achieve around one or more sales per day.
		#
		percent_of_average_flux = g.Decimal('0.333333') # 33.3333% or 1/3
		limitPrice = float( g.Decimal(bought_price + (g.Decimal(target_buy_and_sell_prices[1]).quantize(g.Decimal('1.000000')) * percent_of_average_flux)).quantize(g.Decimal('1.000000')))

		limit_price_text = str(limitPrice)
		bought_price_text = str(bought_price) 
		print('limit price is ' + limit_price_text)
		print('bought price is ' + bought_price_text)

		order_info =  r.orders.get_all_crypto_orders(info=None)[0]
		buy_order_id = order_info['id']
		quantity = order_info['quantity']
		
		#
		# This is to deal with a 'bug' where sometimes the order to buy is not yet complete
		#
		if order_info['state'] != 'confirmed':
			sell_order_info = check_slow_order(symbol, quantity, limitPrice, buy_order_id)
		else:
			# Place Sell Order
			sell_order_info = submit_limit_sell_order(symbol, quantity, limitPrice)
			g.sleep(5)

		# now we need to check if sell order was recieved
		sell_order_info = r.orders.get_all_crypto_orders(info=None)[0]
		sell_order_id = sell_order_info['id']
		print(symbol, sell_order_id)
		create_order_file(symbol, sell_order_id)
		
		csv_data =  str(symbol) +','+ str(target_buy_and_sell_prices[0]) +','+ str(amountInDollars) +','+ str(bought_price) +','+ str(buy_order_id) +','+ str(quantity) +','+ str(limitPrice) +','+ str(sell_order_id) + ','+ str(target_buy_and_sell_prices[1])
		print(csv_data)
		transactions_file(symbol, csv_data)


def submit_limit_sell_order(symbol, quantity, limitPrice):
	print('submitting sell order for ' + symbol + ' at ' + str(limitPrice))
	if limitPrice > 1:
		sell_order_info = r.orders.order_sell_crypto_limit(symbol, quantity, round(limitPrice, 2), timeInForce='gtc')
	else:
		sell_order_info = r.orders.order_sell_crypto_limit(symbol, quantity, limitPrice, timeInForce='gtc')
	g.sleep(35)
	print(r.orders.get_all_crypto_orders(info=None)[0])
	g.sleep(35)
	return sell_order_info


def get_available_crypto_symbols():
	cryptos = r.crypto.get_crypto_currency_pairs(info=None)
	number_of_cryptos = len(cryptos)
	i = 0
	while i < number_of_cryptos:
		if cryptos[i]['tradability'] == 'tradeable':
			print(g.colored(cryptos[i]['symbol'] + ' ' + cryptos[i]['tradability'], 'green'))
		i += 1
	return cryptos


def try_to_buy_coins():
	login()
	get_crypto_positions()
	export_reports()

	coins_json = read_coins_file()
	coins = coins_json['coins']
	for e in coins:
		g.cls()
		ascii()
		do_it_all(e)

	logout()


#
# This can be improved using a different function from the robin_stocks library
# Take a look at get_open_order_by_id for where to make improvements
#
def check_slow_order(symbol, quantity, limitPrice, buy_order_id):
	num_of_open_orders = get_open_order_by_id(buy_order_id)
	if num_of_open_orders >= 1:
		i = 1
		#while i < 10 and num_of_open_orders >= 1:
		while num_of_open_orders >= 1:
			g.sleep(35)
			print('waiting on an open order')
			num_of_open_orders = get_open_order_by_id(buy_order_id)
			if i == 9 and num_of_open_orders >= 1:
#
#
#					add cancel here
#
#
				print('fuck.... Cancel it.')
			i += 1

		#
		# Sell Order
		#
		sell_order_info = submit_limit_sell_order(symbol, quantity, limitPrice)
		g.sleep(5) 

	else:
		#
		# Sell Order
		#
		sell_order_info = submit_limit_sell_order(symbol, quantity, limitPrice)
		g.sleep(5)
		
	return sell_order_info
