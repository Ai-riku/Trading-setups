# Import the engine file
from ib_forex_setup import engine

# Set all the variables you need for the trading app
###############################################################################
###############################################################################
""" Set the variables as per your trading specifications"""
# Set account name in case you do paper trading
account = 'DU1682711'
# Set the time zone
timezone = 'America/Lima'
# The app port
port = 7497
# The account base currency symbol
account_currency = 'USD'
# The asset symbol
symbol = 'EURUSD'
# The data frequency for trading
data_frequency = '5min'
# The auto-restart hour
local_restart_hour = 23
# The historical data file address
historical_data_address = 'historical_data.csv'
# The base_df file address
base_df_address = 'app_base_df.csv'
# The train span 
train_span = 3500
# Set the number of days to set the test data number of rows   
test_span_days = 1
# The app host
host='127.0.0.1'
# The client id
client_id=1
# Set the seed for the machine-learning model
seed = 2024  
# Set the trailing stop loss boolean
trail = True
# Set the seed you would like to use for your trading setup computations
seed = 2025
# The email that will be used to send the emails
smtp_username = 'jcgtanaka@gmail.com'
# The email to which the trading info will be sent. It can be the above or any other email
to_email = 'jcgtanaka@gmail.com'
# The app password that was obtained in Google. You need to allow app password in Google: 
# https://support.google.com/mail/answer/185833?hl=en
password = 'xreh bdtl tiug dmvn'
###############################################################################
""" Set the additional variables you would like to add for the strategy functions"""
# Example (uncomment the below code line to incorporate this variable in the trading setup)
# num_technical_indicators = 50
# Set the leverage of your position
leverage = None
# ...
###############################################################################
