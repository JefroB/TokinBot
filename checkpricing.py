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
from datafiles import read_data_file
from globals import globals as g

##
## get_crypto_historicals (function) - used to get cypto history
##
## symbol (str) � The crypto ticker.
## return_int (str) � The time between data points. Can be �15second�, �5minute�, �10minute�, �hour�, �day�, or �week�.
## span_length (str) � The entire time frame to collect data points. Can be �hour�, �day�, �week�, �month�, �3month�, �year�, or �5year�.
##
def get_crypto_historicals(symbol, return_int, span_length):
	#
	# We can, and have been locked out for hitting this API too often.
	# Anything that uses this needs optimization.
	#
	#g.sleep(21)
	history =  r.crypto.get_crypto_historicals(symbol, interval=return_int, span=span_length, bounds='24_7', info=None)
	return history


def get_last_price_by_5_min_span(symbol, row):
	data = read_data_file(symbol, '5minute')
	price = g.Decimal(data[row]['open_price']).quantize(g.Decimal('1.000000'))
	return price
	
# We use the open price, becase the current day's data is not complete
def get_daily_open_price(symbol, row):
	data = read_data_file(symbol, 'day')
	price = g.Decimal(data[row]['open_price']).quantize(g.Decimal('1.000000'))
	return price
	

def get_record_from_daily_data(symbol, row):
	data = read_data_file(symbol, 'day')
	record = data[row]
	return record


def average_price_over_last_30_min(symbol):
	g.sleep(5)
	prices = [get_last_price_by_5_min_span(symbol, 4), get_last_price_by_5_min_span(symbol, 5), get_last_price_by_5_min_span(symbol, 6), get_last_price_by_5_min_span(symbol, 7), get_last_price_by_5_min_span(symbol, 8)]
	total = g.Decimal(prices[0]) + g.Decimal(prices[1]) + g.Decimal(prices[2]) + g.Decimal(prices[3]) + g.Decimal(prices[4])
	average = str(total / 5)
	print(g.colored(' Average ' + symbol + ' Price over the last 30 mins: ' + average, 'yellow'))
	return average


def check_market_conditions(symbol):
	cur_price = current_price(symbol)
	current_conditions = []

	# Check if Up over last Year
	if get_price_direction_over_last_year(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over last 3 Months
	if get_price_direction_over_last_3month(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over last Month
	if get_price_direction_over_last_month(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over last Week
	if get_price_direction_over_last_week(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over last Day
	if price_direction_over_last_day(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over last hour
	if price_direction_over_last_hour(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)	

	# Check if Up over 30 min
	if price_direction_over_last_30min(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over 15 min
	if price_direction_over_last_15min(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over 10 min
	if price_direction_over_last_10min(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)

	# Check if Up over 5 min
	if price_direction_over_last_5min(symbol, cur_price) == 'up':
		current_conditions.append(1)
	else:
		current_conditions.append(0)
	print('Stat building complete. Thanks for waiting.')

	return current_conditions


def get_market_condition_score_unweighted(symbol):
	current_conditions = check_market_conditions(symbol)
	number_of_data_points = len(current_conditions)
	i = 0
	score = 0
	while i < number_of_data_points:
		score = score + current_conditions[i]
		i += 1
	score_text = str(score)
	print('-----------------------------------------------')
	print(g.colored(symbol + ' unweighted market score is: ' + score_text + ' out of 10', 'yellow'))
	print('')

	# recent history only
	r = 5
	recent_score = 0
	while r < number_of_data_points:
		recent_score = recent_score + current_conditions[r]
		r += 1
	recent_score_text = str(recent_score)
	print('')
	print(g.colored(symbol + ' recent market score is: ' + recent_score_text + ' out of 5', 'yellow'))
	print('')
	return score, recent_score
	
	
def get_direction(symbol, span, open_price, close_price):
	if open_price > close_price:
		direction = 'down'
		color = 'red'
	else:
		direction = 'up'
		color = 'green'
	print(g.colored(symbol + ' price is going ' + direction + ' over the last ' + span + '.', color))
	return direction


def get_price_direction_over_last_year(symbol, cur_price):
	open_price = get_daily_open_price(symbol,364)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, 'year', open_price, cur_price)
	return direction



def get_price_direction_over_last_3month(symbol, cur_price):
	open_price = get_daily_open_price(symbol, 89)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, '3 months', open_price, cur_price)
	return direction


def get_price_direction_over_last_month(symbol, cur_price):
	open_price = get_daily_open_price(symbol, 29)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, 'month', open_price, cur_price)
	return direction


def get_price_direction_over_last_week(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 2015)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, 'week', open_price, cur_price)
	return direction
	

def price_direction_over_last_day(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 287)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, 'day', open_price, cur_price)
	return direction


def price_direction_over_last_hour(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 11)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, 'hour', open_price, cur_price)
	return direction


def price_direction_over_last_30min(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 5)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, '30 minutes', open_price, cur_price)
	return direction


def price_direction_over_last_15min(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 2)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, '15 minutes', open_price, cur_price)
	return direction


def price_direction_over_last_10min(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 1)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, '10 minutes',  open_price, cur_price)
	return direction


def price_direction_over_last_5min(symbol, cur_price):
	open_price = get_last_price_by_5_min_span(symbol, 0)
	print(str(open_price) +' '+ str(cur_price))
	direction = get_direction(symbol, '5 minutes', open_price, cur_price)
	return direction


def current_price(symbol):
	g.sleep(15)
	price = g.Decimal(r.crypto.get_crypto_quote(symbol)['ask_price']).quantize(g.Decimal('1.000000'))
	print('Current Price of', symbol, 'is:', price)
	return price


def check_price_difference(symbol):
	target_price = average_price_over_last_30_min(symbol)
	difference = g.Decimal(current_price(symbol)).quantize(g.Decimal('1.000')) -  g.Decimal(target_price).quantize(g.Decimal('1.000000'))
	print('Recent price difference:', difference)
	return difference


def get_average_fluctuation(symbol):
	print('Calcluating daily price fluxuations...')
	flux = get_daily_highs_and_lows(symbol)
	average_flux = get_daily_flux(flux)
	return average_flux


def get_daily_highs_and_lows(symbol):
	records = [1,2,3,4,5,6,7]
	hist = []
	for r in records:
		hist.append(get_record_from_daily_data(symbol, r))
		print(get_record_from_daily_data(symbol, r))	
		
	flux = []
	i = 0
	while i < 6:
		high = g.Decimal(hist[i]['high_price']).quantize(g.Decimal('1.000000'))
		low = g.Decimal(hist[i]['low_price']).quantize(g.Decimal('1.000000'))
		daily_flux = high - low
		flux.append(daily_flux)
		print(daily_flux)
		i += 1
		
	# sort the list of daily fluctuations 
	# and remove the move volatile day
	flux.sort()
	flux.pop()
	
	return flux


def get_daily_flux(flux):
	daily_fluxuation = 0
	i = 0
	while i < 5:
		daily_fluxuation = daily_fluxuation + flux[i]
		i += 1
	average_flux =  g.Decimal(daily_fluxuation / 5).quantize(g.Decimal('1.000000'))

	average_flux_text = str(average_flux)
	print('average price fluctuation is: ' + average_flux_text)
	return average_flux


def get_target_buy_and_sell_prices(symbol):
	records = [1,2,3,4,5,6,7]
	hist = []
	daily_medians = []
	for r in records:
		hist.append(get_record_from_daily_data(symbol, r))
		high_price = g.Decimal(hist[r - 1]['high_price']).quantize(g.Decimal('1.00000'))
		low_price = g.Decimal(hist[r - 1]['high_price']).quantize(g.Decimal('1.00000'))
		median_price = (high_price + low_price) / 2
		daily_medians.append(median_price)
	
	median_prices = 0
	for m in daily_medians:
		median_prices = median_prices + m
	actual_medain_price = median_prices / 7
	
	average_flux = get_average_fluctuation(symbol)
	percentage_of_average_flux = g.Decimal(0.60)
	drop_amount = (average_flux) * percentage_of_average_flux
	today = get_record_from_daily_data(symbol, 0)
	
	#if actual_medain_price > g.Decimal(today['open_price']):
	#		starting_price = today['open_price']
	#else:
	#	starting_price = actual_medain_price
	starting_price = actual_medain_price
	
	target_buy_price = g.Decimal(g.Decimal(starting_price) - drop_amount).quantize(g.Decimal('1.000000'))
	buy_price_text = str(target_buy_price)
	print(g.colored('The target buy price is: $' + buy_price_text, 'green'))
	return target_buy_price, average_flux

#
# This is used to determine the dollar amount purchased and likely could be better
# It would be nice to consider the volume of trading as well as the current grading system
#
def go_shopping(symbol):
	scores = get_market_condition_score_unweighted(symbol)
	unweighted_score = scores[0]
	recent_score = scores[1]
	if unweighted_score >= 8:
		if recent_score < 5:
			purchase_size = 'med buy'
		else:
			purchase_size = 'big buy'
	elif unweighted_score < 8 and unweighted_score >= 4:
		if recent_score < 5:
			purchase_size = 'small buy'
		else:
			purchase_size = 'med buy'
	elif unweighted_score < 4 and unweighted_score >= 2:
		if recent_score < 5:
			purchase_size = 'no buy'
		else:
			purchase_size = 'small buy'
	else:
		purchase_size = 'no buy'
	print(purchase_size)
	g.sleep(15)

	return purchase_size
