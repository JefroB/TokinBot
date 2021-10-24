#########################################################################################################
##                                                                                                     ##
##                                           TOKIN' BOT                                                ##
##                                                                                                     ##
##                                     Written By: J.Bornhoeft                                         ##
##                                                                                                     ##
##                       A Bot to Buy and sell cryptocurrencies on Robinhood                           ##
##                                                                                                     ##
#########################################################################################################
from colorama import init
from termcolor import colored
from decimal import Decimal
from time import sleep
import os
#import path from os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
