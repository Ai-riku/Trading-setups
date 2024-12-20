# For data manipulation
import pickle 
import numpy as np
import pandas as pd
from hmmlearn import hmm
from datetime import datetime
from sklearn.utils import check_random_state
import trading_functions as tf
import featuretools as ft
from featuretools.primitives import Month, Weekday, Hour
from ta import add_all_ta_features
from statsmodels.tsa.stattools import adfuller
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.calibration import CalibratedClassifierCV as calibration

import warnings
warnings.filterwarnings("ignore")

def create_classifier_model(seed):
    """ Function to create a bagging classifier model """
    
    # Create the model object
    model = calibration(BaggingClassifier(RFC(n_estimators=5, max_features=1.0, class_weight = "balanced_subsample",\
                                              n_jobs=-2, random_state=seed),
                                          n_estimators=50, random_state=seed, n_jobs=-2),
                        method='isotonic', n_jobs=-2)
    return model

def set_stop_loss_price(signal, last_value, risk_management_target, stop_loss_multiplier):
    """ Function to create the stop-loss price """
            
    # If the signal tells you to go long
    if signal > 0:
        # The stop loss price will be below the long position value
        order_price = round(last_value*(1-risk_management_target*stop_loss_multiplier),5)
    # If the signal tells you to short-sell the asset
    elif signal < 0:
        # The stop loss price will be above the short position value
        order_price = round(last_value*(1+risk_management_target*stop_loss_multiplier),5)
        
    return order_price

def set_take_profit_price(signal, last_value, risk_management_target, take_profit_multiplier):
    """ Function to create the take-profit price """
            
    # If the signal tells you to go long
    if signal > 0:
        # The stop loss price will be below the long position value
        order_price = round(last_value*(1+risk_management_target*take_profit_multiplier),5)
    # If the signal tells you to short-sell the asset
    elif signal < 0:
        # The stop loss price will be above the short position value
        order_price = round(last_value*(1-risk_management_target*take_profit_multiplier),5)
        
    return order_price

def prepare_base_df(df, max_window, test_span, train_span=None, scalable_features=None):
    """ Function to prepare the data to be used for model fitting """
        
    ###############################################################################
    # Section 1: Creating the first model prediction feature
    ###############################################################################
    # Compute the close-to-close log returns
    df['cc_returns'] = np.log(df.Close/df.Close.shift(1))
    # Compute the prediction feature for the first model
    df['y'] = np.where(df['cc_returns'].shift(-1)>0,1,0)
    df['y'] = np.where(df['cc_returns'].shift(-1)<0,-1,df['y'])
    # Drop the rows which have the prediction feature a label with very few observations
    df = tf.dropLabels(df)
    
    # Use the last number of observations
    if train_span is not None:
        df = df.iloc[-train_span:]

    ###############################################################################
    # Section 2: Creating the datetime input features
    ###############################################################################
    # Set the name for the dates dataframe index
    for_features_index = 'index1'
    # Create a column based on the index datetime
    df[for_features_index] = df.index
    
    # Create an entityset to form the dates-based features
    es = ft.EntitySet('My EntitySet')
    es.add_dataframe(
        dataframe_name = 'main_data_table',
        index = 'index',
        dataframe = df[['Close', for_features_index]])#,
        # time_index = 'index1')#, 
        # make_index=True)
        
    # Set the frequency to be used to get the dates time series
    time_features = [Month, Weekday, Hour]
    #time_features = [Minute, Hour, Weekday, Month]
    
    # Create the time series based on the time frequencies' features from above
    fm, features = ft.dfs(
        entityset = es,
        target_dataframe_name = 'main_data_table',
        trans_primitives = time_features)
    
    # Set the fm index as the df.index is
    fm.set_index(df.index, inplace=True, drop=True)
    
    # A function to obtain the fm columns names
    def get_var_name(variable):
         for name, value in globals().items():
            if value is variable:
                return name
            
    # Set the time features names in a list
    time_features_columns = [get_var_name(el).upper()+ '('+for_features_index+')' for el in time_features]
    
    # Obtain the dummies from the months' time series
    months_dummies = pd.get_dummies(fm[time_features_columns[0]])
    # Rename the month's columns
    months_dummies.columns = ['month_'+ str(month) for month in months_dummies.columns.to_list()]
    # Obtain the dummies from the days' time series
    days_dummies = pd.get_dummies(fm[time_features_columns[1]])
    # Rename the days columns
    days_dummies.columns = ['day_'+ str(day) for day in days_dummies.columns.to_list()]
    # Drop the Saturday's column
    days_dummies.drop('day_5', axis=1, inplace=True)
    # Obtain the dummies from the hours' time series
    hours_dummies = pd.get_dummies(fm[time_features_columns[2]])
    # Rename the hour's columns
    hours_dummies.columns = ['hour_'+ str(hour) for hour in hours_dummies.columns.to_list()]
    
    # Save the datetime features in a single dataframe
    datetime_features = pd.concat([months_dummies, days_dummies, hours_dummies],axis=1)
    
    ###############################################################################
    # Section 3: Creating the technical indicators features
    ###############################################################################
    # Create a Volume column with zeros
    df['Volume'] = 0.0
    
    # Set the list of window sizes        
    if max_window<=15:
        windows = list(range(3,max_window))
    elif max_window>=16:
        windows = list(range(3,11))+list(range(15,(max_window+1),10))
    
    # Create the technical indicators dataframe
    technical_features_df = pd.DataFrame(index=df.index)
    
    # Obtain the long-memory stationary OHLC data based on the optimal "d" previously estimated
    df[['Open_dif','High_dif','Low_dif','Close_dif']] = df[['Open','High','Low','Close']].pct_change()
        
    ohlc_lags_list = ['Open_dif','High_dif','Low_dif','Close_dif']
    for lag in list(range(1,10)):
        df[[f'Open_dif_{lag}',f'High_dif_{lag}',f'Low_dif_{lag}',f'Close_dif_{lag}']] = df[['Open_dif','High_dif','Low_dif','Close_dif']].shift(lag)
        ohlc_lags_list.extend([f'Open_dif_{lag}',f'High_dif_{lag}',f'Low_dif_{lag}',f'Close_dif_{lag}'])
    
    # Drop Nan values
    df.dropna(inplace=True)
    
    # Get all the possible technical indicators for each window size
    for window in windows:
        # Obtain the technical indicators
        technical_features = (
            add_all_ta_features(
                df[['Open','High','Low','Close','Volume']].copy(), \
                    open="Open", high="High", low="Low", close="Close", volume="Volume"
            )
            .ffill()
        )
        
        # Drop the OHLCV columns
        technical_features.drop(['Open','High','Low','Close','Volume'], axis=1, inplace=True)
        # Save the names of the volume-based features as a list
        volume_indicators = technical_features.filter(like='volume', axis=1).columns.tolist()
        # Drop the volume-based features
        technical_features.drop(volume_indicators, axis=1, inplace=True)
        
        # Save the names of the volume-based features as a list
        volume_pvo_indicators = technical_features.filter(like='pvo', axis=1).columns.tolist()
        # Drop the volume-based features
        technical_features.drop(volume_pvo_indicators, axis=1, inplace=True)
        
        # Modify the dataframe columns to distinguish them from other features with different window sizes
        technical_features.columns = [f'{column}_{window}' for column in technical_features.columns.tolist()]
        # Concatenate these window-size-based technical indicators to the bigger dataframe
        technical_features_df.loc[technical_features.index, technical_features.columns.tolist()] = technical_features
        
    # Create a loop to make the technical indicators stationary
    for indicator in technical_features_df.columns:
        # If all observations are NaN values
        if technical_features_df[indicator].isna().all():
            # Drop the feature from the dataframe
            technical_features_df.drop(indicator, axis=1, inplace=True)  
            continue
        # If all observations are Infinite
        elif np.isinf(technical_features_df[indicator].values).all():
            # Drop the feature from the dataframe
            technical_features_df.drop(indicator, axis=1, inplace=True)  
            continue
        else:
            try:
                # Get the p-value of the adfuller applied to the technical indicator
                pvalue = adfuller(technical_features_df[indicator].iloc[:-test_span].dropna(), regression='c', autolag='AIC')[1]
                # If the p-value is higher than 0.05
                if pvalue > 0.05:
                    # Use the percentage returns of the technical indicator as the input feature
                    technical_features_df[indicator] = technical_features_df[indicator].pct_change()
                # If no p-value was obtained from the adfuller
                elif np.isnan(pvalue):
                    # Drop the feature from the dataframe
                    technical_features_df.drop(indicator, axis=1, inplace=True)
            except:
                # Drop the feature from the dataframe
                technical_features_df.drop(indicator, axis=1, inplace=True)
    
    # Creating more features
    ma_signal_names = [f'ma_signal_{i}' for i in windows]
    std_names = [f'std_{i}' for i in windows]
    std_mean_names = [f'std_mean_{i}' for i in windows]
    std_signal_names = [f'std_signal_{i1}_{i2}' for i1 in windows for i2 in windows]    
    df[ma_signal_names] = np.array([np.where(df['Close']>df['Close'].rolling(i).mean().values,1.0,-1.0) for i in windows]).T
    df[std_names] = np.array([df['Close'].rolling(i).std().values for i in windows]).T
    df[std_mean_names] = np.array([df[f'std_{i}'].rolling(i).mean() for i in windows]).T    
    df[std_signal_names] = np.array([np.where(df[f'std_{i1}']<df[f'std_mean_{i2}'],1.0,-1) for i1 in windows for i2 in windows]).T
    
    ###############################################################################
    # Section 4: Concatenating the necessary dataframes into a single dataframe
    ###############################################################################
    # Set the scalable features list
    if scalable_features is None:
        scalable_features = technical_features_df.columns.tolist() + \
            df[ohlc_lags_list].columns.tolist()
        
    # Create the base dataframe to be used for the ML model
    base_df = pd.concat([technical_features_df, df[ohlc_lags_list], datetime_features],axis=1)
    
    # Create the states' column to save the HMM-based regimes
    base_df['states'] = 0.0
    
    # Save the names of the final features as a list
    final_input_features = base_df.columns.tolist()
    
    # Create the dataframe to be used for estimating the model
    base_df = pd.concat([base_df, \
                         df[['y','cc_returns','Open','High','Low','Close','high_first']],\
                         df[ma_signal_names+std_signal_names]],axis=1) 
    
    # Save the high_first boolean values as integer numbers
    base_df['high_first_signal'] = np.where(base_df['high_first']==True,1.0,0.0)
    
    # Drop the high_first boolean-type column
    base_df.drop('high_first', axis=1, inplace=True)
        
    # Add the relevant features to the final features
    final_input_features.extend(ma_signal_names)
    final_input_features.extend(std_signal_names)
    final_input_features.append('high_first_signal')
    
    # Forward fill the NaN values
    base_df.ffill(inplace=True)  
    
    # Drop the NaN values
    base_df.dropna(inplace=True) 
    
    ###############################################################################
    # Section 5: Make the input features rolling-zscore-based
    ###############################################################################

    # Z-score the input features
    base_df, scalable_features = tf.rolling_zscore_function(base_df, scalable_features, 30) 
        
    # Drop the Inf values
    base_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    base_df.ffill(inplace=True) 
    
    return base_df, final_input_features, scalable_features

def get_signal(logging, market_open_time, base_df, final_input_features, purged_window_size, embargo_period): 
    ''' Function to get the signal'''
    
    print('Getting the current signal...')
    logging.info('Getting the current signal...')
        
    """ Change code from here """
    ###############################################################################
    # Section 1: Create the month and day strings to be used for calling the model objects
    ###############################################################################

    # Set the month and day strings to call the models
    month_string = str(market_open_time.month) if market_open_time.month>=10 else '0'+str(market_open_time.month)
    day_string = str(market_open_time.day-1) if (market_open_time.day-1)>=10 else '0'+str(market_open_time.day-1)

    ###############################################################################
    # Section 2: Split the data into train and test dataframes for the X and y features
    ###############################################################################

    # Create the input and prediction features
    X, y = tf.create_Xy(base_df, final_input_features, 'y')
    
    # Split the data
    X_train, X_test, y_train, _ = tf.train_test_split(X, y, 1, purged_window_size, embargo_period)
    
    ###############################################################################
    # Section 3: Create the HMM-based input feature
    ###############################################################################

    # Create the R indicator
    r_values = tf.directional_change_events(base_df.loc[X_train.index,['Close']], theta=0.00002, columns='R').dropna().values.reshape(-1,1)
    
    # Call the HMM model
    hmm_model = pickle.load(open(f'data/models/hmm_model_{market_open_time.year}_{month_string}_{day_string}.pickle', 'rb'))
        
    X_train['states'].iloc[-len(r_values):] = hmm_model.predict(r_values)
    
    # Forecast the next period state
    transmat_cdf = np.cumsum(hmm_model.transmat_, axis=1)
    random_state = check_random_state(hmm_model.random_state)
    X_test['states'].iloc[0] = (transmat_cdf[int(X_train['states'].iloc[-1])] > random_state.rand()).argmax()
    
    ###############################################################################
    # Section 4: Create the signal
    ###############################################################################
    # Call the random-forest first model object
    model_object = pickle.load(open(f'data/models/model_object_{market_open_time.year}_{month_string}_{day_string}.pickle', 'rb'))
    
    # Save the model test signal predictions
    signal = base_df.loc[X_test.index,'signal'] = float(model_object.predict(X_test[model_object.feature_names_in_.tolist()].astype("float32"))[0])
    
    """ Change code up to here """
    
    print('The current signal was successfully created...')
    logging.info('The current signal was successfully created...')
    
    return signal

def strategy_parameter_optimization(market_open_time, seed, random_seeds, data_frequency, max_window, file_address, base_df_address, purged_window_size, embargo_period, train_span, test_span=None):

    # Set the month and day strings to save the model objects
    month_string = str(market_open_time.month) if market_open_time.month>=10 else '0'+str(market_open_time.month)
    day_string = str(market_open_time.day-1) if (market_open_time.day-1)>=10 else '0'+str(market_open_time.day-1)

    """ Change code from here """
    ###############################################################################
    # Section 1: Prepare the base_df dataframe
    ###############################################################################
    start_time = datetime.now()
    print('='*100)
    print('='*100)
    print(f"- Preparing the base_df dataframe starts at {start_time}")
    
    # Get the trading periods per day
    periods_per_day = tf.get_periods_per_day(data_frequency)
    # Set the number of rows to be used for the test data
    if test_span is None:
        test_span = 5*periods_per_day
    
    # Import the data
    df = pd.read_csv(file_address, index_col = 0)
    # Parse the index as datetime
    df.index = pd.to_datetime(df.index)
    # Get the midpoint of the OHLC data
    df = tf.get_mid_series(df)
    # Resample the data as the frequency string
    
    # Get the hour string from the market opening time
    hour_string = str(market_open_time.hour) if (market_open_time.hour)>=10 else '0'+str(market_open_time.hour)
    # Get the minute string from the market opening time
    minute_string = str(market_open_time.minute) if (market_open_time.minute)>=10 else '0'+str(market_open_time.minute)
    # Resample the data
    df2 = tf.resample_df(df,frequency=data_frequency,start=f'{hour_string}h{minute_string}min')
    
    # Prepare the dataframe to be used for fitting the model
    base_df, final_input_features, scalable_features = prepare_base_df(df2, max_window, test_span, train_span)
    
    start_time = datetime.now()
    print('='*100)
    print('='*100)
    print(f"- Backtesting starts at {start_time}")
    
    ###############################################################################
    # Section 2: Split the data into train and test dataframes for the X and y features
    ###############################################################################
    # Create the input and prediction features
    X, y = tf.create_Xy(base_df, final_input_features, 'y')
    
    # Split the data
    X_train, X_test, y_train, _ = tf.train_test_split(X, y, test_span, purged_window_size, embargo_period)
        
    ###############################################################################
    # Section 3: Create the HMM-based input feature
    ###############################################################################
    # Create the R indicator
    r_values = tf.directional_change_events(base_df.loc[X_train.index,['Close']], theta=0.00002, columns='R').values.reshape(-1,1)
    train_r_values = r_values[:-test_span]
    train_r_values = train_r_values[~np.isnan(train_r_values)].reshape(-1,1)
    test_r_values = r_values[-test_span:].reshape(-1,1)
    
    # Create an HMM object with two hidden states
    hmm_model = hmm.GaussianHMM(n_components = 2, covariance_type = "diag", n_iter = 100, random_state = seed)
    
    # Estimate the HMM model
    hmm_model.fit(train_r_values)
    
    # Use the Viterbi algorithm to find the fitted hidden states
    X_train['states'].iloc[(len(X_train)-len(train_r_values)):] = hmm_model.predict(train_r_values)
    
    # Compute the next state hidden state for the test data
    for i in range(len(train_r_values),(len(train_r_values)+len(test_r_values))):
        transmat_cdf = np.cumsum(hmm_model.transmat_, axis=1)
        random_state = check_random_state(hmm_model.random_state)
        if i == len(train_r_values):
            X_test['states'].iloc[(i-len(train_r_values))] = \
                (transmat_cdf[int(X_train['states'].iloc[-1])] > random_state.rand()).argmax()
        else:
            X_test['states'].iloc[(i-len(train_r_values))] = \
                (transmat_cdf[int(X_test['states'].iloc[(i-1-len(train_r_values))])] > random_state.rand()).argmax()
    
    ###############################################################################
    # Section 4: Do feature importance with the Boruta-Shap algorithm
    ###############################################################################
    # Set the date of train split to estimate the Boruta-Shap algorithm
    date_loc_split = X_train.index[int(len(X_train.index)*0.8)]
    
    # Select the best features based on the Boruta Shap algorithm
    print('Get the best features with the Boruta-Shap algorithm')
    selected_features = tf.library_boruta_shap(X_train, y_train.iloc[:,:], seed, 25, date_loc_split)
    
    ###############################################################################
    # Section 5: Estimate the models based on the list of seeds
    ###############################################################################
    # Set the start date of the backtesting seed loop
    loop_start_time = datetime.now()
    print('='*100)
    print(f"- Backtesting loop starts at {loop_start_time}")

    # A dictionary to save the model objects created per each seed
    model_objects = {}
    
    # A dictionary to save the test-data Sharpe ratios of each model
    models_sharpe = dict()

    # Annualize factor for the Sharpe ratio
    annualize_factor = 252*periods_per_day

    for i in range(len(random_seeds)):    
        print(f"\t- model number {i+1} with seed {random_seeds[i]} estimation starts at {datetime.now()}")

    	# Create an random forest algo object
        model_objects[random_seeds[i]] = create_classifier_model(random_seeds[i]) 
        # Fit the model with the train data
        model_objects[random_seeds[i]].fit(X_train[selected_features].astype("float32"), y_train.astype("int32").values.ravel())
                
    	# Save the model train signal predictions
        base_df.loc[X_train.index,'signal'] = \
            model_objects[random_seeds[i]].predict(X_train[selected_features].astype("float32"))
            
    	# Save the model test signal predictions
        base_df.loc[X_test.index,'signal'] = \
            model_objects[random_seeds[i]].predict(X_test[selected_features].astype("float32"))
            
        # Compute the model's cumulative returns
        base_df.loc[X_train.index,'rets'] = base_df.loc[X_train.index,'cc_returns'] * \
            base_df.loc[X_train.index,'signal'].shift(1)
                                
        # Compute the model's cumulative returns
        base_df.loc[X_test.index,'rets'] = base_df.loc[X_test.index,'cc_returns'] * \
            base_df.loc[X_test.index,'signal'].shift(1)
                                
        # Compute the model's test data Sharpe ratio
        models_sharpe[random_seeds[i]] = np.round(base_df.loc[X_test.index,'rets'].mean() / \
                                                  base_df.loc[X_test.index,'rets'].std() * \
                                                  np.sqrt(annualize_factor),3)
                  
        print(f"\t\t- model number {i+1} with seed {random_seeds[i]} estimation ends at {datetime.now()}")
    
    loop_end_time = datetime.now()
    print('='*100)
    print(f"- Backtesting loop ends at {loop_end_time}")
    print(f"- Backtesting lasted {loop_end_time-start_time}")
      
    ###############################################################################
    # Section 6: Optimize the strategy based on the list of seeds
    ###############################################################################
    # Get the optimal model seed to trade the next month 
    optimal_seed = max(models_sharpe, key=models_sharpe.get)
            
    # Saving the base_df dataframe
    base_df.to_csv('data/'+base_df_address)
    
    ###############################################################################
    # Section 7: Save all the model objects used while optimizating the strategy
    ###############################################################################
    # Save the HMM model
    with open(f'data/models/hmm_model_{market_open_time.year}_{month_string}_{day_string}.pickle', 'wb') as handle:
        pickle.dump(hmm_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Save the model object
    with open(f'data/models/model_object_{market_open_time.year}_{month_string}_{day_string}.pickle', 'wb') as handle:
        pickle.dump(model_objects[optimal_seed], handle, protocol=pickle.HIGHEST_PROTOCOL)

    """ Change code up to here """
    
    # Save all the final and scalable features' names in a dataframe
    features_df = pd.DataFrame(data=final_input_features, columns=['final_features'], index=range(len(final_input_features)))
    features_df['scalable_features'] = np.nan
    features_df.loc[:(len(scalable_features)-1),'scalable_features'] = pd.Series(scalable_features)
    features_df.to_excel('data/optimal_features_df.xlsx')
        

    
