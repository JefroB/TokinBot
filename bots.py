#########################################################################################################
##                                                                                                     ##
##                                           TOKIN' BOT                                                ##
##                                                                                                     ##
##                                     Written By: J.Bornhoeft                                         ##
##                                                                                                     ##
##                       A Bot to Buy and sell cryptocurrencies on Robinhood                           ##
##                                                                                                     ##
#########################################################################################################
from coinbot import try_to_buy_coins
from globals import globals as g
from art import ascii
from datafiles import read_coins_file
from ui import strategy_questionaire, generate_auth, startup, select_coins

runcount = 1

try:
	while True:
		
		generate_auth()
		ascii()

		# this should be replaced with a call to robinhood to get avilable cryptos. 
		# Perhaps only occasionally called, since new cryptos are not added often.
		coins = ['DOGE', 'BCH', 'ETC', 'LTC', 'ETH', 'BSV', 'BTC']
		print('runcount = ' + str(runcount))
		select_coins(coins, runcount)
		coins = read_coins_file()
		for e in coins['coins']:
			strategy_questionaire(e)

		startup()
		try_to_buy_coins()

		#minutes = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
		minutes = [1]
		for x in minutes:
			ascii()
			time = str(x)
			if x == 1:
				s = ''
			else:
				s = 's'
			print('Sleeping for ' + time + ' minute' + s)
			print('')
			g.sleep(60)
			g.cls()
		runcount += 1

except KeyboardInterrupt:
	pass

