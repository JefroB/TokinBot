#########################################################################################################
##                                                                                                     ##
##                                           TOKIN' BOT                                                ##
##                                                                                                     ##
##                                     Written By: J.Bornhoeft                                         ##
##                                                                                                     ##
##                       A Bot to Buy and sell cryptocurrencies on Robinhood                           ##
##                                                                                                     ##
##  This file was added to test out new functions, and changes to old functions, before making a mess  ##
##  out of working code. It is just a playground.                                                      ##
##                                                                                                     ##
#########################################################################################################
import robin_stocks.robinhood as r
from pyotp import TOTP as otp
from checkpricing import go_shopping, price_direction_over_last_day, price_direction_over_last_5min, get_crypto_historicals, get_target_buy_and_sell_prices, average_price_over_last_30_min, get_record_from_daily_data
from openorders import get_all_open_order_by_symbol, get_recent_order_id, get_open_selling_positions_by_symbol, get_open_order_by_id
from datafiles import create_order_file, export_reports, build_data_files, read_coins_file, create_strategy
from keys import decrypt_file
from coinbot import login, logout, order_crypto
from globals import globals as g
from art import ascii, header_art, high_rent
import json
import time
import os
from datetime import datetime


