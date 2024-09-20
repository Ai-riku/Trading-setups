# Import the necessary libraries
import numpy as np
from engine import main
  
###############################################################################
""" Set the variables as per your trading specifications"""
# Set account name in case you do paper trading
account = 'DU1234567'
# Set the time zone
timezone = 'America/Bogota'
# The app port
port = 7497
# The account base currency symbol
account_currency = 'USD'
# The asset symbol
symbol = 'EURUSD'
# The data frequency for trading
data_frequency = '10min'
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
# The maximum window to create the technical indicators
max_window = 6
# The app host
host='127.0.0.1'
# The client id
client_id=1
# Set the seed for the machine-learning model
seed = 2024
# Create 10 uniformly-distributed random numbers
np.random.seed(seed)
random_seeds = list(np.random.randint(low = 1, high = 10000001, size = 1000000))[:3]
# The purged window and embargo period values
purged_window_size = embargo_period = 1    
# Set the leverage
leverage = 1
# Set the risk management price return target
risk_management_target = 0.003
# Set the stop loss multiplier target
stop_loss_multiplier = 1
# Set the take profit multiplier target
take_profit_multiplier = 2
# The email that will be used to send the emails
smtp_username = 'your_email@gmail.com'
# The email to which the trading info will be sent. It can be the above or any other email
to_email = 'any_email@email_extension.com'
# The app password that was obtained in Google. You need to allow app password in Google: https://support.google.com/mail/answer/185833?hl=en
password = 'qwer yuio asdf hjkl'
###############################################################################

# Run the main file to run the app loop
main(account, timezone, port, account_currency, symbol, data_frequency, local_restart_hour, historical_data_address, base_df_address, train_span, test_span_days, 
     max_window, host, client_id, purged_window_size, embargo_period, seed, random_seeds, leverage, risk_management_target, stop_loss_multiplier, take_profit_multiplier, smtp_username, to_email, password)
