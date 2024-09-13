# An end-to-end setup to trade forex algorithmically

#### This document details the strategy we’ve used to trade forex.
###### QuantInsti Webpage: https://www.quantinsti.com/

# DISCLAIMER

#### This file is documentation only and should not be used for live trading without appropriate backtesting and tweaking of the strategy parameters.

## Licensed under the Apache License, Version 2.0 (the "License").
- Copyright 2024 QuantInsti Quantitative Learnings Pvt Ltd.
- You may not use this file except in compliance with the License.
- You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
- Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

## Table of contents
1. [Introduction](#introduction)
2. [Notes](#notes)
3. [Function: create_classifier_model](#create_classifier_model)
4. [Function: set_stop_loss_price](#set_stop_loss_price)
5. [Function: set_take_profit_price](#set_take_profit_price)
6. [Function: prepare_base_df](#prepare_base_df)
7. [Function: get_signal](#get_signal)
8. [Function: strategy_parameter_optimization](#strategy_parameter_optimization)


<a id='introduction'></a>
## Introduction
We are happy to introduce our working setup to trade forex algorithmically with the Interactive Brokers API.

We refer to our labor of love as a Python-based setup, trading app, or similar names. We hope it’s self-evident that they all refer to the same thing!

This script allows you to execute transactions in the forex market using a customizable strategy and swap out forex assets as needed. The script-based application aims to teach you the basics of using a ready-made IB-API-based trading app and how it works during each trading period.

This documentation explains the basics of implementing a strategy in the trading app. You will learn the steps followed in the strategy and the variables used. You can make major changes following the functions’ outputs. However, if you want to make changes beyond the functions’ outputs, we suggest you revise the entire script’s code to modify it according to your trading needs.

<a id='notes'></a>
## Notes

- The file name is “strategy_file.py”. Do not change the file name. The functions can be changed with respect to inputs, outputs, and definitions.
- The first function (create_classifier_model) can be changed completely at your discretion, the remaining ones can only be changed in their respective definitions. The inputs and outputs of these remaining functions cannot be modified.
- Each function will be explained based on:
    - Available modifications
    - Explanation
    - Parameters
    - Output

<a id='create_classifier_model'></a>
## Function: create_classifier_model
```python
create_classifier_model(seed)
```

### Available modifications
1. Definition: Modifiable
2. Input: Modifiable
3. Output: Modifiable

### Explanation:
- This function outputs the machine-learning model object.
- The model employs a random forest algorithm with bagging.
- The only changeable parameter is the seed.
- If you want to vary more parameters or change the model, please modify the function at your discretion.
- The optimization of the strategy consists of testing many models and finding the one that performs the best. This is done in the function ```strategy_parameter_optimization``` in the same strategy file. Each model will vary only on a seed basis.

### Parameters
- **seed**
    - Explanation: This is the seed used for the model building.
    - Variable type: ```int```

### Output
- **model**:
    - Explanation: The function should output the model object. If you want the function to output something else or change the output, please modify this file and the others so that they run properly.
    - Variable type: ```object```

<a id='set_stop_loss_price'></a>
## Function: set_stop_loss_price
```python
set_stop_loss_price(signal, last_value, risk_management_target, stop_loss_multiplier)
```

### Available modifications
1. Definition: Modifiable
2. Input: Not modifiable
3. Output: Not modifiable

### Explanation:
- This function sets the price target for the stop-loss order in the trading setup.
- This function is modifiable in such a way that it can be used for long and short signals, that's why there's an if-else condition to apply for both cases.
- The stop loss is created such that it is a percentage return (risk_management_target*stop_loss_multiplier) lower (higher) than the last forex price value for the long (short) signal.

### Parameters
- **signal**
    - Explanation: The signal for the market order obtained from the ```get_signal``` function.
    - Variable type: ```float```
- **last_value**
    - Explanation: The forex asset's latest price that is available in the market. This value is obtained within the trading app. To make the function work, keep this input. This price is used as the price from which we can obtain the take profit target price.
    - Variable type: ```float```
- **risk_management_target**
    - Explanation: Explained in the Start-here documentation guide.
    - Variable type: ```float```
- **stop_loss_multiplier**
    - Explanation: Explained in the Start-here documentation guide.
    - Variable type: ```float```

#### Output
- **order_price**:
    - Explanation: The target price of the stop-loss order.  
    - Variable type: ```float```

<a id='set_take_profit_price'></a>
## Function: set_take_profit_price
```python
set_stop_loss_price(signal, last_value, risk_management_target, take_profit_multiplier)
```
### Available modifications
1. Definition: Modifiable
2. Input: Not modifiable
3. Output: Not modifiable
### Explanation:
- This function sets the price target for the take-profit order in the trading setup.
- This function is modifiable in such a way that it can be used for long and short signals, that's why there's an if-else condition to apply for both cases.
- The stop loss is created such that it is a percentage return (risk_management_target*take_profit_multiplier) higher (lower) than the last forex price value for the long (short) signal.
### Parameters
- **signal**
    - Explanation: The signal for the market order obtained from the ```get_signal``` function.
    - Variable type: ```float```
- **last_value**
    - Explanation: The forex asset's latest price that is available in the market. This value is obtained within the trading app. To make the function work, keep this input. This price is used as the price from which we can obtain the take profit target price.
    - Variable type: ```float```
- **risk_management_target**
    - Explanation: Explained in the Start-here documentation guide.
    - Variable type: ```float```
- **take_profit_multiplier**
    - Explanation: Explained in the Start-here documentation guide.
    - Variable type: ```float```
### Output
- **order_price**:
    - Explanation: The target price of the take-profit order.  
    - Variable type: ```float```

<a id='prepare_base_df'></a>
## Function: prepare_base_df
```python
prepare_base_df(df2, max_window, test_span, train_span=None, scalable_features=None)
```

### Available modifications
1. Definition: Modifiable
2. Input: Not modifiable
3. Output: Not modifiable

### Explanation:
This function creates a dataframe to be used later to create the ```X``` and ```y``` dataframes for the ML model. It consists of 5 sections:
1. **Creating the first model prediction feature**
    - Creates the prediction feature based on the next-day price-return sign.
    - Drop the zero signals
    - Subset the dataframe based on the most recent "train_span" observations.
2. **Creating the datetime input features**
    - Create the fm dataframe that will contain the time-frequency values based on the datetime index of the dataframe.
    - Create dummies columns based on the months, days' numbers, and hours that are obtained through the fm dataframe.
3. **Creating the technical indicators features**
    - Create the "windows" list that will contain all the available window sizes to be used for the creation of technical indicators.
    - Create the percentage returns of the OHLC data and their respective lags.
    - Use a for loop that will iterate through the "windows" list. It will create a group of technical indicators based on each window. The loop will:
        - Create the technical indicators based on the iteration window
        - Drop the OHLCV of the created TI-based dataframe
        - Drop all the Volume-based indicators since we don't have that in forex.
        - Drop the columns with NaN values.
        - Change the current TI-based dataframe columns' names to incorporate the window size string.
        - Add the TA-based dataframe values to the whole "technical_features_df" dataframe. This dataframe will contain the technical indicators created with all the window sizes.
    - Check for stationarity for all the technical indicators. If the TI is stationary, we use it as an input feature. If it's not, we use its percentage returns as an input feature.
    - Create more features using signals based on moving averages and standard deviations of the Close prices.
4. **Concatenating the necessary dataframes into a single dataframe**
    - Create a list of features that can be transformed into a rolling zscore. Name them as "scalable_features"
    - Create the "base_df" datagrame that will be used in another function to create the X and y features.
5. **Make the input features rolling-zscore-based**. It uses a function called "rolling_zscore_function" where inputs are:
    - The dataframe to be used for transforming its respective columns into rolling zscores (base_df in this case)
    - The column names to be transformed into rolling zscores (scalable_features in this case)
    - The window size to create the rolling zscores.

### Parameters
- **df**
    - Explanation: The historical OHLC data as per the data frequency defined in the main file (the variable is ```data_frequency```).
    - Variable type: ```pandas.DataFrame```
- **test_span**
    - Explanation: The test span to be used for splitting the ```df``` into train and test data. For the optimization of the strategy, this value will be equal to the ```test_span_days``` defined in the main file. For the trading setup, it will be equal to 1, since we need to set the train span until the previous trading period.
    - Variable type: ```int```
- **train_span**
    - Explanation: The span to be used to select the most recent observations for the train dataframe. This is a string provided in the main file (The variable name is ```train_span```). This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```
- **scalable_features**
    - Explanation: A list of strings, where each string will be the name of the columns in the ```base_df```dataframe to be transformed into rolling zscores. We use this list as input for the function because in the trading setup it will be called. For the optimization of the strategy, this variable is not called, the list will be actually created inside this function.
    - Variable type: ```list```

### Output
- **base_df**:
    - Explanation: The dataframe to be used to create the X and y features in another function.
    - Variable type: ```pandas.DataFrame```
- **final_input_features**:
    - Explanation: The list of strings that will be column names of the ```base_df```dataframe that will be used for the X dataframe in another function.
    - Variable type: ```list```
- **scalable_features**:
    - Explanation: The list of strings that will be column names of the ```base_df```dataframe that will be used for transforming them into rolling zscores.
    - Variable type: ```list```    

<a id='get_signal'></a>
## Function: get_signal
```python
get_signal(market_open_time, base_df, final_input_features, purged_window_size, embargo_period, logging)
```
### Available modifications
1. Definition: Modifiable
2. Input: Not modifiable
3. Output: Not modifiable
### Explanation:
This function creates the long and short signal to be used in inside the trading setup. It consists of 4 sections:
1. **Create the month and day strings to be used for calling the model objects**
2. **Split the data into train and test dataframes for the X and y features**
    - Create the the X and y dataframes using a function called ```create_Xy```. The function uses 3 inputs:
        - The dataframe to be used for splitting it as input and prediction features.
        - The list of column name strings to be used to create the input features.
        - The prediction feature name string to be used to create the prediction feature.
    - Split the X and y dataframes into train and test dataframes. It uses a function called ```train_test_split```. It outputs 4 variables (X_train, X_test, y_train, y_test). The function uses 5 inputs:
        - The X dataframe
        - The y dataframe
        - An integer to be used as a span for the test data.
        - The purged window size ```int``` value to eliminate the first observations based on this value. This variable is explained in the Start-here documentation guide.
        - The embargo period ```int``` value to eliminate the first observations based on this value. This variable is explained in the Start-here documentation guide.
3. **Create an input feature based on the Hidden Markov (HMM) model**
    - Create the Directional-Change R indicator.
    - Import the HMM model object created in the ```strategy_parameter_optimization``` function.
    - Apply a Hidden-Markov model to the above indicator.
    - Fill the X_train and X_test dataframes with the HMM-based in-sample and out-of-sample predictions, respectively.
4. **Create the signal**
    - Import the model object created in the ```strategy_parameter_optimization``` function.
    - Create the signal based on the X_test data using the model object from above.
### Parameters
- **market_open_time**
    - Explanation: It's the start datetime of the current week.
    - Variable type: ```datetime.datetime```
- **base_df**
    - Explanation: Provided in the ```prepare_base_df``` definition.
    - Variable type: ```pandas.DataFrame```
- **final_input_features**
    - Explanation: Provided in the ```prepare_base_df``` definition.
    - Variable type: ```list```
- **purged_window_size**
    - Explanation: This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```
- **embargo_period**
    - Explanation: This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```
- **logging**
    - Explanation: An object to be used for saving logging information.
    - Variable type: ```object```
### Output
- **signal**:
    - Explanation: The signal to be used in the trading setup to create the market order.
    - Variable type: ```float```

<a id='strategy_parameter_optimization'></a>
## Function: strategy_parameter_optimization
```python
strategy_parameter_optimization(market_open_time, seed, random_seeds, data_frequency, max_window, file_address, base_df_address, purged_window_size, embargo_period, train_span, test_span=None)
```

### Available modifications
1. Definition: Modifiable
2. Input: Not modifiable
3. Output: None

### Explanation:
This function does the optimization of the strategy based on the seed list provided in the main file. It will be called each weekend when the market closes. Take into account that the whole optimization should last less than 48 hours (2 days) so you can start trading in the next week's first datetime. It consists of 7 sections:
1. **Prepare the base_df dataframe**
    - Create the test span based on the trading frequency provided in the main file. The test span will be approximately 1 week. For example, in case you want to make the test span to be 1 month, please change the code line 391 as ```test_span = 22*periods_per_day```since a month has 22 days approximately. Otherwise, you can set this variable as per your specific number of observations by defining it in the main file (The variable to change is ```test_span_days```).
    - Create the ```df``` dataframe based on the historical minute data. This dataframe is then converted to OHLC data and resampled as per the trading frequency provided in the main file (the variable is ```data_frequency```)
2. **Split the data into train and test dataframes for the X and y features**
    - To create the X and y dataframes, it uses the ```create_Xy``` function explained previously in the ```get_signal``` function above.
    - Split the X and y dataframes into train and test dataframes. It uses a function called ```train_test_split``` explained previously in the ```get_signal``` function above. This time the test_span variable is not 1. It's actually the test_span defined in Section 1.
3. **Create the HMM-based input feature**
    - Create the Directional-Change R indicator.
    - Define an HMM model object and fit the model.
    - Provide in-sample and out-of-sample predictions for the X_train and X_test dataframes.
4. **Do feature importance with the Boruta-Shap algorithm**
    - Set the split observation such that 80% of the X_train dataframe will be used as the train dataframe for the Boruta-Shap algorithm and the remaining 20% of dataframe to select the best features based on the same algorithm.
    - Apply the Boruta-Shap algorithm and save the best features in the ```selected_features``` list.
5. **Estimate the models based on the list of seeds**
    - Create 2 dictionaries to save the ML-based model objects and their corresponding Sharpe ratio values.
    - Set an ```annualize_factor``` to compute the Sharpe ratio.
    - Use a loop to iterate through each seed to estimate an ML model based on it
        - Create the ML model object
        - Fit the model
        - Fill the X_train and X_test dataframes with the in-sample and out-of-sample signal values.
        - Fill the X_train and X_test dataframes with the in-sample and out-of-sample strategy returns.
        - Save in the Sharpe ratio value of the strategy.
6. **Optimize the strategy based on the list of seeds**
We choose the model seed that has the highest Sharpe ratio value.
7. **Save all the model objects used while optimizating the strategy**
We save the 2 objects created in this function. These objects will be used in the ```get_signal``` function. They're saved as pickle files.

### Parameters
- **market_open_time**
    - Explanation: It's the start datetime of the current week.
    - Variable type: ```datetime.datetime```
- **seed**
    - Explanation: This is a single seed value provided in the main file (The variable name is ```seed```).
    - Variable type: ```int```. This variable is explained in the start_here_document guide.
- **random_seeds**
    - Explanation: This is a list of integer seeds provided in the main file (The variable name is ```random_seeds```). This variable is explained in the start_here_document guide.
    - Variable type: ```list```
- **data_frequency**
    - Explanation: This is a string provided in the main file (The variable name is ```data_frequency```). This variable is explained in the start_here_document guide.
    - Variable type: ```string```
- **max_window**
    - Explanation: This is an integer provided in the main file (The variable name is ```max_window```). This variable is explained in the start_here_document guide.
    - Variable type: ```int```
- **file_address**
    - Explanation: This is a string that relates to the historical minute data CSV file downloaded before you start trading.
    - Variable type: ```string```
- **base_df_address**
    - Explanation: This is a string that is used to save the ```base_df```dataframe and it's provided in the main file. This variable is explained in the start_here_document guide.
    - Variable type: ```string```
- **purged_window_size**
    - Explanation: Provided in the ```prepare_base_df``` definition. This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```
- **embargo_period**
    - Explanation: Provided in the ```prepare_base_df``` definition. This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```
- **train_span**
    - Explanation: Provided in the ```prepare_base_df``` definition. This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```
- **test_span**
    - Explanation: Provided in the ```prepare_base_df``` definition. This variable is explained in the Start-here documentation guide.
    - Variable type: ```int```

### Output
The function doesn't have any output to be given.
