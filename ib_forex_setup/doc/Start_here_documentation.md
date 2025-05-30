## An end-to-end setup to trade forex algorithmically

#### This is your “Start here” document to set up your system for trading forex algorithmically.
###### QuantInsti Webpage: https://www.quantinsti.com/

**Version 1.0.1**
**Last Updated**: 2025-05-28

-----

## Disclaimer

#### This file is documentation only and should not be used for live trading without appropriate backtesting and tweaking of the strategy parameters.

## Licensed under the Apache License, Version 2.0 (the "License"). 
- Copyright 2025 QuantInsti Quantitative Learnings Pvt Ltd. 
- You may not use this file except in compliance with the License. 
- You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
- Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

## Table of contents
1. [Introduction](#introduction)
2. [Crucial Attributes](#crucial_attributes)
3. [Setup Notes](#setup_notes)
4. [Interactive Brokers setup requirements](#ib_requirements)
5. [Setup of variables](#variables_setup)

<a id='introduction'></a>
## Introduction 
We are happy to introduce a working version of our Python-based setup to trade forex algorithmically. It is meant for forex trading with the Interactive Brokers API. This script allows you to execute transactions in the forex market using a customizable strategy, and swap out forex assets as needed. 

The script-based application aims to teach you how to use a ready-made IB-API-based trading setup and how it works during each trading period. We refer to our labor of love as a Python-based setup, trading app, or similar such names. We hope it’s self-evident that they all refer to the same thing!

<a id='crucial_attributes'></a>
## Crucial attributes:
- forex trading: Our script functions and is optimized for this asset class in a streamlined manner because we created it with forex trading in mind. You can execute trades confidently because we’ve created it considering the nuances of the forex markets. 
- Strategy customization: Our script empowers you to modify trading strategies according to your preferences and market conditions. You can control your trading approach by adjusting risk parameters or refining entry and exit criteria.
- Flexible asset selection: You can modify your trading strategies to profit from any forex pair by having the flexibility to switch up your forex assets. You can use this trading application on as many forex pairs as IB allows.
- Integration with Interactive Brokers API: Our script utilizes the Interactive Brokers API to allow you to execute trades quickly and connect you to real-time forex market data. This integration ensures reliable access to market data and execution capabilities.
- Effective operation: Devoid of graphical user interfaces, we use only scripts if you want to quickly learn the intricacies of the trading setup code. You can make trades quickly and concentrate on the main file variables of the trading app.

<a id='setup_notes'></a>
## Setup notes
1. If you want to use the same strategy to check how the setup works, you should only need to modify the “main.py” file . In case you want to modify the strategy at your convenience, please also modify the “strategy_file.py” file (both files are located in the "samples" folder). Only forex contracts should be traded with this trading app.
2. If you run the trading setup for the first time, you'll see that you'll be downloading historical minute data. It will take like 3 to 5 days to complete the downloading (it will download from 2005 to 2024). This only happens at the very first time. Once you have the historical minute data up to date, you'll have the trading setup running.
3. The forex market closes from 5 pm to 6 pm Eastern time and the stop-loss and take-profit targets get discarded at 5 pm EST. Each day the setup will close all the existing positions half an hour before 5 pm EST. 
4. The setup will not leave any open positions on weekends. 
5. The strategy is based on bagging with a random forest algorithm. It creates long and short signals. To learn more about it, refer to the MLT-04 lecture.
6. The trading setup is designed to retrieve historical data from up to 10 previous days. If your historical data has missing data for more than 10 days, you’ll need to run the setup to download historical data and update the dataframe.
7. In case you want to get the live equity curve of the strategy, once you start trading, please go to the “database.xlsx” Excel file, sheet “cash_balance”, column “value”. Plot that column to see the equity curve graphically.
8. In case you want to make more changes to the setup so it can be better customized per your needs, please modify all the other relevant files as needed.

<a id='ib_requirements'></a>
## Interactive Brokers setup requirements

1. Installation of the **offline stable** version of the TWS. Save the TWS file in “path_to/Jts/tws_platform"
2. Installation of the **stable** version of the IB API. Save the IB API files in "path_to/Jts/tws_api"
3. Log in with your account credentials in the IB web platform and then go to Settings. Next, in the “Account Configuration” section, click on “Paper Trading Account”. Finally, click on the “Yes” button against the question “Share real-time market data subscriptions with paper trading account?” and click on “Save”. Wait at least 2 hours to let IB make the paper account have market data subscriptions.
4. In the TWS or IB Gateway platform, do the following: Go to File, Global configuration, API, and in Settings:
    1. Check “ActiveX and Socket Clients”
    2. Uncheck the “Read-Only API”
    3. In the “send instrument-specific attributes for dual-mode API client in” box, select “operator timezone”.
    4. Click on the “Reset API order ID sequence” whenever you need to restart paper or live trading.
5. In the TWS or IB Gateway platform, do the following: Go to File, Global configuration, Configuration and in “Lock and Exit”:
    - In the “Set Auto Logoff Timer” section, choose your local time to auto-log off or auto-restart the platform. Due to the IB platform specifications, in case you select auto-restart, it must restart at the specific hour you select. Be careful with this. When selecting auto restart, sometimes it doesn’t work properly, so you might need to log in to the platform again manually. 
6. In Configuration, Export trade Reports, check the “Export trade reports periodically”.
7. In the same section from above, in the “Export filename”, type: “\path_to\Jts\setup\samples\data\reports\report.txt”. This file will give you a trade report of all the trading positions you took while trading.
8. In the same section from above, in the “Export directory”, type: “\path_to\Jts\setup\samples\data\reports”. This folder will be used to save the trade report from above.
9. In the same section above, specify the interval at which you would like the reports to be generated.
10. Depending on your initial equity and trading frequency, you will have different equity curves throughout time. If you first want to try paper trading, you should set the initial equity value. To do this, please go to https://www.interactivebrokers.co.uk/sso/Login and do the following:
    1. Select “Paper”, instead of “Live”
    2. Login with your username and password
    3. Go to “Settings”
    4. Go to “Account Settings”
    5. In “Configuration”, click on the nut button of the “Paper Trading Account Reset”
    6. In the “Select Reset Amount” box, click on “Other Amount”. In the “Amount” box, write a specific amount you want to use as an initial equity value. Read the below instructions and click on Continue.
11. In case you want to reset the paper trading account to default settings, do the following:
    1. Drop all the created files saved in the "data" folder and sub-folders.
    2. Go to the TWS platform, go to the “File” tab, click on “Global Configuration”, click on “API settings”, and click on the “Reset API order ID sequence” button. Finally, click on “Apply” and “Ok”. Then you can paper trade once again from the start. In case you have live traded, please close any existing position on any asset before you restart live trading with the app.
12. To profit from forex leverage, you need to **ask IB to have a margin account for forex**. If you don’t do it, you will not be able to trade at all your capacity.

<a id='variables_setup'></a>
## Setup of variables
Inside the “main” file, you can change the following variables per your trading requirements. Each variable is explained and some extra information is added.

- **account**: The account name of your IB account. This account name starts with U followed by a number for a live trading account and starts with DU followed by a number for a paper trading account. Learn more in the TBP-01 lecture.
- **timezone**: Set the timezone of your country of residence. Please select the appropriate timezone as per the available Python time zones.
- **port**: The port number as per the live or paper trading account. Learn more in the TBP-01 lecture.
- **account_currency**: The base currency that your IB account has. You set the base currency while creating your IB account. It can be USD, EUR, INR, etc.
- **symbol**: The forex symbol to be traded. Choose as per the IB available forex assets to be traded. 
- **data_frequency**: The frequency used for trading. Please set this variable to ‘24h’ if you want to trade daily. The setup is not designed to trade with a frequency lower than daily (2-day, 3-day, etc.). Be careful while deciding the data_frequency because the signal creation might take longer than your chosen trading frequency. To check how much time it takes to run the strategy, you should check for each period the “epat_trading_app_database” file, sheet “app_time_spent”, column name “seconds”, and the unique value. 
- **local_restart_hour**: The local timezone hour you previously selected to log off or auto-restart your IB TWS. If you log off or auto-restart at 11 pm in the TWS platform, please set this variable to 23, and so on.
- **historical_data_address**: The string of the historical data file name and address. The data file is the resampled data per the frequency you set above.
- **base_df_address**: The string of the dataframe used to fit the machine learning model. Set the file name and address at your convenience.
- **train_span**: Set the train data number of observations to be used to fit the machine learning model. Please check the historical_data_address file to specify a number equal to or lower than the maximum data observations available in the historical dataframe file.
- **test_span_days**: To optimize the strategy, specify how many days you want to use as a validation dataset. The higher the trading frequency, the higher this number should be. For a daily frequency, set 22 days as a monthly validation dataset.
- **host**: Set the host for the trading app. Learn more in the TBP-01 lecture.
- **client_id**: Set the client ID for the trading app. Learn more in the TBP-01 lecture.
- **seed**: Set the seed to create a list of random seeds for the machine learning strategy. Each seed provides a unique machine-learning model to be used for backtesting it. The best model is chosen based on the machine learning model that gives the best Sharpe ratio of its strategy returns.
- **smtp_username**: Your Gmail to be used from which you’ll send the trading information per the above trading data frequency.
- **to_email**: The email (it can be any email service: Gmail, Outlook, etc.) to send the trading information per the above trading data frequency.
- **password**: The app password that was obtained from Google Gmail. You need to allow the app password in Google: https://support.google.com/mail/answer/185833?hl=en. Once you access the link, click on the link “Create and manage your app passwords”. Then, type your email and password and you’ll be directed to the “App passwords” webpage. There, you type an app name, it can be any name, and then you’ll be given a 12-letter-long password. Copy that password and paste it into this variable.

In the same "main" file, you can add optional variables per your trading requirements. In this case we optionally added the following:
- **leverage**: Set the fixed leverage you will use at your trading convenience. If you want to create a dynamic leverage position, please change the strategy_file file. You can set this with values from 0 (no position) to any positive number. A high value needs to be evaluated as per the leverage limits IB sets for each forex asset.
