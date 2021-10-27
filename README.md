# TokinBot
A bot for buying and selling cryptocurrencies on Robinhood, written in Python 3.


## Running the Bots
From a terminal window enter:

  Python3 bots.py


## Running for the first time

You will be asked for your Robinhood username and password. This is so that the script can log into your Robinhood account to make purchases and sales.

You will also be asked for a 2FA key. You can find the 2FA key on the robinhood website in the Account section.



### From the Robinhood website, select the following:

Account > Settings > Security And Privacy > Authenticator App

Then enable Two-Factor Authentication. Do Not scan the code. Instead, click the link below the code that says "can't scan it". The code presented is your 2FA key.

###### To Do:
Add cancelation logic in case purchase orders take to long to fulfill.

Purchase size logic would benefit from being reworked.

Possibly add logic to make small purchases when prices rise for a few days in a row. This could introduce quite a bit more risk, so would need to be thoroughly tested.
