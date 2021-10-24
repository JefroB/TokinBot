#########################################################################################################
##                                                                                                     ##
##                                           TOKIN' BOT                                                ##
##                                                                                                     ##
##                                     Written By: J.Bornhoeft                                         ##
##                                                                                                     ##
##                       A Bot to Buy and sell cryptocurrencies on Robinhood                           ##
##                                                                                                     ##
#########################################################################################################
from datafiles import create_strategy, write_json_file
from globals import globals as g
from keys import generate_key_file, encrypt_file
from art import ascii, relax
import os

def strategy_questionaire(symbol):
    filename = './strategies/' + symbol + '.json'

    file_exists = os.path.exists(filename)
    if file_exists == True:
        try:
            recreate_answer = str(input('Would you like to create a new ' + symbol + ' strategy?'))
            if recreate_answer == 'y':
                file_exists = False
            else:
                print('Using previous strategy for ' + symbol + '.')
        except ValueError:
                print("Invalid")

    if file_exists == False:
        try:
            max = input('What is the maximum dollar amount of ' + symbol + ' that you wold like Tokin\' Bot to purchase?')
            if max != None:
                print('the maximum dollar amount to spend on ' + symbol + ' is: $' + str(max))
            else:
                print('Skipping ' + symbol)      
        except ValueError:
            print("Invalid")
        try:
            min = input('What is the minimum dollar amount of ' + symbol + ' that you wold like Tokin\' Bot to purchase?')
            if min != None:
                print('the minimum dollar amount to spend on ' + symbol + ' is: $' + str(min))
            else:
                print('Skipping ' + symbol)      
        except ValueError:
            print("Invalid")

        create_strategy(symbol, float(min), float(max))


def select_coins(symbols, runcount):
	if runcount <= 1:
		filename = './strategies/coins.json'
		coins = []
		
		file_exists = os.path.exists(filename)
		if file_exists == True:
			try:
				recreate_answer = str(input('Would you like to choose which cryptos Tokin\' Bot will manage?'))
				if recreate_answer == 'y':
					file_exists = False
				else:
					print('Using previous settings.')
			except ValueError:
				print("Invalid")

		if file_exists == False:
			for symbol in symbols:
				try:
					answer = str(input('Would you like Tokin\' Bot to buy and sell ' + symbol + '?'))
					if answer == 'y':
						print('Adding ' + symbol + ' to the list of managed cryptos.')
						coins.append(symbol)
					else:
						print('Skipping ' + symbol)      
				except ValueError:
					print("Invalid")

			coins_for_json = dict()
			coins_for_json['coins'] = coins
			write_json_file(filename, coins_for_json)

	
def generate_auth():
	file_exists = os.path.exists('./breakfast/hashbrowns.txt')
	if file_exists == False:
		generate_key_file()
		username = str(input("Enter Your Robinhood Username: "))
		encrypt_file(username, './breakfast/toast.txt')
		password1 = '1'
		while True:
			try:
				password1 = str(input("Enter Your Robinhood Password: "))
				password2 = str(input("Enter Your Robinhood Password Again: ")) 
				if password1 == password2:
					print("The passwords your entered match")
					break;
				else:
					print("The passwords your entered do not match")      
			except ValueError:
				print("Invalid")
				continue
		encrypt_file(password1, './breakfast/eggs.txt')
		
		code = str(input("Enter Your Robinhood 2FA Auth Key: "))
		encrypt_file(code, './breakfast/sausage.txt')
		print('Auth files encrypted')


def startup():
    g.cls()
    g.init()
    ascii()
    print(g.colored('Startin\' Tokin\' Bots...', 'red'))
    g.sleep(4)
    g.cls()
    print('')
    print('')
    print(g.colored('                                    This will take a little bit. Smoke \'em if ya got \'em...', 'white'))
    relax()
    g.sleep(4)
    g.cls()