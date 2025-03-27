# An end-to-end setup to trade forex algorithmically

#### This document details the strategy we've used to trade forex.
###### QuantInsti Webpage: https://www.quantinsti.com/

**Version 1.0**  

# Disclaimer

#### This file is documentation only and should not be used for live trading without appropriate backtesting and tweaking of the strategy parameters.

## Licensed under the Apache License, Version 2.0 (the "License").
- Copyright 2024 QuantInsti Quantitative Learnings Pvt Ltd.
- You may not use this file except in compliance with the License.
- You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
- Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

**Last Updated**: [Insert Date]  

## Table of Contents  
1. [Introduction](#introduction)  
2. [General Guidelines](#general-guidelines)
3. [Workflow of how the `strategy.py` is used by the trading setup](#workflow)
4. [Core Components](#core-components)  
   - 3.1 [Data Preparation](#data-preparation)  
   - 3.2 [Signal Generation](#signal-generation)  
   - 3.3 [Risk Management](#risk-management)  
   - 3.4 [Model Training & Optimization](#model-training--optimization)  
5. [Function Documentation](#function-documentation)  
   - 4.1 [`create_classifier_model(seed)`](#1-create_classifier_modelseed)  
   - 4.2 [`prepare_base_df(...)`](#2-prepare_base_dfbase_df-max_window-test_span-train_spannone)  
   - 4.3 [`get_signal(...)`](#3-get_signalbase_df-purged_window_size-embargo_period)  
   - 4.4 [`set_stop_loss_price()` & `set_take_profit_price()`](#4-set_stop_loss_price--set_take_profit_price)  
   - 4.5 [`strategy_parameter_optimization(...)`](#5-strategy_parameter_optimization)  
6. [Dependencies](#dependencies)  
7. [Detailed Function Modifications](#detailed-function-modifications)  

<a id='introduction'></a>
## Introduction  
The `strategy.py` file is the core algorithmic trading module responsible for generating trading signals, managing risk, and optimizing strategy parameters. It integrates machine learning models (e.g., Hidden Markov Models, Random Forests) with technical analysis to predict market direction and execute trades. Key features include:  
- **Feature Engineering**: Creates technical indicators, datetime features, and stationary transformations.  
- **Regime Detection**: Uses HMMs to identify market states (e.g., bullish/bearish).  
- **Risk Management**: Dynamically sets stop-loss and take-profit levels.  
- **Model Persistence**: Saves trained models for consistent signal generation.
- Important Notes:
   - You can modify almost anything in the functions' definitions. There are some things you cannot change. But don't worry. Once you understand the whole documentation, you can quickly tweak it to fit your trading needs.
   - If you want to add more inputs for the functions, you can set them in this same file or the `main.py` file. The only condition is that they must be put in either of these two files.

---

<a id='general-guidelines'></a>
## General Guidelines  
1. **Mandatory Inputs**:  
   - The `base_df` parameter (a feature-engineered DataFrame) **cannot be removed** from any function where it appears.  
   - Functions called by `setup_functions.py` (e.g., `get_signal`, `prepare_base_df`) must retain their only the `base_df` input to avoid runtime errors. You can add more inputs or remove the existing ones as you'd like.   

2. **Modifications**:  
   - You may add new (or remove) inputs/outputs to functions if they enhance your own strategy logic.  
   - Avoid removing parameters marked as "Required" in the [Function Documentation](#function-documentation).  

3. **Reproducibility**:  
   - Use `seed` parameters to ensure consistent model training. This can be either used or not. It's better to use it. In case you're not using an ML-based strategy, you can get rid of the seed in case you don't generate random numbers.
   - (Pre-)trained models are saved with date-specific filenames (e.g., `model_object_2023_10_05.pickle`).  

---

<a id='workflow'></a>
### Workflow of how the `strategy.py` is used by the trading setup

**Step-by-Step Process**:  

1. **Weekly Model Optimization**  
   - **Function**: `strategy_parameter_optimization()`  
   - **Frequency**: Called once per week.  
   - **Purpose**:  
     - Trains HMM and classifier models using historical data.  
     - Selects optimal features via Boruta-Shap.  
     - Saves updated models and metadata to `data/models/`.  

2. **Signal Generation**  
   - This process is repeated for each period while trading as per the frequency (`data_frequency`) you choose in the `main.py` file.
   - **Step 1**: **Prepare Feature-Engineered Data**  
     - **Function**: `prepare_base_df()`  
     - **Input**: Raw OHLC data.  
     - **Output**: Processed `base_df` with (stationary) technical indicators, datetime features.  
   - **Step 2**: **Generate Trading Signal**  
     - **Function**: `get_signal()`  
     - **Input**: `base_df` from `prepare_base_df()`.  
     - **Output**:  
       - `signal` (`-1`, or `1`).  
       - `leverage` (position sizing multiplier).

3. **Order Execution & Risk Management**  
   - This process is repeated for each period while trading as per the frequency (`data_frequency`) you choose in the `main.py` file.
   - These two functions are called inside the trading setup once you generate the signal with the `get_signal` function.
   - **Step 1**: **Send Market Order**  
     - Based on the `signal`, execute a market order (long/short).  
   - **Step 2**: **Set Stop-Loss**  
     - **Function**: `set_stop_loss_price()`  
     - **Input**: `signal`, entry price, risk parameters.  
     - **Output**: Stop-loss price (below entry for long, above entry for short).  
   - **Step 3**: **Set Take-Profit**  
     - **Function**: `set_take_profit_price()`  
     - **Input**: `signal`, entry price, risk parameters.  
     - **Output**: Take-profit price (above entry for long, below entry for short).  

---

### Key Workflow Notes:  
1. **Weekly vs. Daily Tasks**:  
   - **Weekly**: Retrain models to adapt to new market conditions.  
   - **As per the trading frequency**: Use pre-trained models to update the `base_df` dataframe, generate the signal, and send the risk management orders.  

2. **Dependencies**:  
   - `prepare_base_df()` **is** run before `get_signal()` (the latter depends on the engineered `base_df`).  
   - `set_stop_loss_price()` and `set_take_profit_price()` **are run after** the `signal` and entry price to calculate thresholds.  

3. **Execution Flow**:  
   ```  
   Weekly: strategy_parameter_optimization() → Each trading period: prepare_base_df() → get_signal() → Market Order → set_stop_loss_price()/set_take_profit_price()  
   ```  

--- 

### Simplified Summary Table  

| Step | Function                          | Frequency       | Inputs                          | Outputs                              |  
|------|-----------------------------------|-----------------|---------------------------------|--------------------------------------|  
| 1    | `strategy_parameter_optimization` | Weekly          | Historical data, seed           | Trained models, feature list         |  
| 2    | `prepare_base_df`                 | Each Trading Period | Raw OHLC data                   | Processed `base_df`, feature names   |  
| 3    | `get_signal`                      | Each Trading Period           | `base_df`, model artifacts      | `signal`, `leverage`                 |  
| 4    | `set_stop_loss_price`             | On-order        | `signal`, entry price, risk     | Stop-loss price                      |  
| 5    | `set_take_profit_price`           | On-order        | `signal`, entry price, risk     | Take-profit price                    |  

--- 

This workflow ensures the strategy adapts weekly to market changes while generating signals (as per your chosen trading frequency) with risk management.

<a id='core-components'></a>
## Core Components of the strategy file 

<a id='data-preparation'></a>
### Data Preparation  
- **Purpose**: Transforms raw OHLC data into a feature-rich DataFrame for model training.  
- **Key Functions**:  
  - `prepare_base_df()`: Generates technical indicators, enforces stationarity, and normalizes features.  
- **Output**: `base_df` (processed DataFrame) and `final_input_features` (list of feature names).  

<a id='signal-generation'></a>
### Signal Generation  
- **Purpose**: Predicts market direction using ML models and HMM regimes.  
- **Key Functions**:  
  - `get_signal()`: Loads pre-trained models and returns a trading signal (`-1`, `0`, `1`).  
- **Dependencies**:  
  - Pre-trained HMM and classifier models stored in `data/models/`.  

<a id='risk-management'></a>
### Risk Management  
- **Purpose**: Calculates stop-loss and take-profit prices to limit losses and lock gains.  
- **Key Functions**:  
  - `set_stop_loss_price()`: Sets stop-loss based on signal direction and volatility.  
  - `set_take_profit_price()`: Sets take-profit using risk multipliers.  

<a id='model-training--optimization'></a>
### Model Training & Optimization  
- **Purpose**: Trains models, selects features, and evaluates performance via backtesting.  
- **Key Functions**:  
  - `strategy_parameter_optimization()`: End-to-end pipeline for model training, feature selection, and artifact saving.  
  - `create_classifier_model()`: Configures the ensemble classifier.  

---

<a id='function-documentation'></a>
## Function Documentation  

<a id='1-create_classifier_modelseed'></a>
### 1. `create_classifier_model(seed)`  
- **Description**: Initializes a calibrated bagging classifier with Random Forest base estimators.  
- **Parameters**:  
  - `seed` (int): Random seed for reproducibility.  
- **Returns**:  
  - `CalibratedClassifierCV`: Model object with calibrated probabilities.  
- **Usage Notes**:  
  - Modify hyperparameters (e.g., `n_estimators`) to adjust model complexity.  

<a id='2-prepare_base_dfbase_df-max_window-test_span-train_spannone'></a>
### 2. `prepare_base_df(base_df, max_window, test_span, train_span=None)`  
- **Description**: Processes raw data into a feature-engineered DataFrame.  
- **Parameters**:  
  - `base_df` (DataFrame): Raw OHLC data.  
  - `max_window` (int): Maximum lookback window for technical indicators.  
  - `test_span` (int): Test set size to avoid look-ahead bias.  
- **Returns**:  
  - `base_df` (DataFrame): Processed data with features and targets.  
  - `final_input_features` (list): Feature names used for model training.  

<a id='3-get_signalbase_df-purged_window_size-embargo_period'></a>
### 3. `get_signal(base_df, purged_window_size, embargo_period, ...)`  
- **Description**: Generates trading signals using pre-trained models.  
- **Parameters**:  
  - `base_df` (DataFrame): Processed data from `prepare_base_df()`.  
  - `purged_window_size` (int): Periods to exclude around splits.  
  - `embargo_period` (int): Buffer to prevent data leakage.  
- **Returns**:  
  - `signal` (float): Trading signal (`-1`, `0`, `1`).  
  - `leverage` (float): Leverage multiplier for position sizing.  

<a id='4-set_stop_loss_price--set_take_profit_price'></a>
### 4. `set_stop_loss_price()` & `set_take_profit_price()`  
- **Description**: Calculate stop-loss/take-profit prices using risk parameters.  
- **Shared Parameters**:  
  - `base_df` (DataFrame): Processed data (for contextual features).  
  - `signal` (int/float): Directional signal (`+1`=long, `-1`=short).  
  - `last_value` (float): Entry price of the position.  
- **Returns**:  
  - `order_price` (float): Rounded stop-loss/take-profit price.  

<a id='5-strategy_parameter_optimization'></a>
### 5. `strategy_parameter_optimization()`  
- **Description**: Trains models, selects features, and saves artifacts.  
- **Key Parameters**:  
  - `historical_minute_data_address` (str): Path to raw OHLC data.  
  - `market_open_time` (datetime): Date for model filenames.  
- **Outputs**:  
  - Saves models to `data/models/` as `.pickle` files.  

---

<a id='dependencies'></a>
## Dependencies  
- **Libraries**: `hmmlearn`, `scikit-learn`, `pandas`, `numpy`, `featuretools`, `statsmodels`.  
- **Custom Modules**: `trading_functions.py` (helper functions).  

---

<a id='detailed-function-modifications'></a>
### Detailed Function Modifications

This guide explains each function in `strategy.py`, including its purpose, inputs/outputs, and how to safely modify them. All functions with `base_df` as an input **cannot remove it** (as per your requirement). Below is a breakdown:

---

#### **1. `create_classifier_model(seed)`**
**Purpose**:  
Creates a calibrated ensemble classifier (bagged random forests) for predicting market direction.

##### **Inputs**:
| Parameter | Type | Required? | Description |
|-----------|------|-----------|-------------|
| `seed` | `int` | Yes | Random seed for reproducibility. |

##### **Outputs**:
| Return Value | Type | Description |
|--------------|------|-------------|
| `model` | `CalibratedClassifierCV` | Classifier model with calibrated probabilities. |

##### **Modifications**:
- **Inputs**:
  - Can add new hyperparameters (e.g., `n_estimators`, `max_depth`).
  - **Do not remove `seed`** unless you handle randomness elsewhere.
- **Outputs**:
  - Must return a classifier object compatible with `sklearn` APIs.
  - Can return additional metadata (e.g., training logs) by modifying the return statement.

##### **Example Modification**:
```python
# Added n_estimators as a new input
def create_classifier_model(seed, n_estimators=50):
    model = calibration(BaggingClassifier(RFC(n_estimators=n_estimators, ...), ...)
    return model
```

---

#### **2. `set_stop_loss_price(base_df, ...)` & `set_take_profit_price(base_df, ...)`  
**Purpose**:  
Calculate stop-loss/take-profit prices based on signal direction and risk parameters.

##### **Inputs**:
| Parameter | Type | Required? | Description |
|-----------|------|-----------|-------------|
| `base_df` | `pd.DataFrame` | Yes | Feature-engineered data (used for context). |
| `signal` | `int/float` | Yes | Trading direction (`+1`=long, `-1`=short). |
| `last_value` | `float` | Yes | Entry price of the position. |
| `risk_management_target` | `float` | Yes | Base risk % (e.g., `0.01` = 1%). |
| `multiplier` | `float` | Yes | Scales the risk distance. |

##### **Outputs**:
| Return Value | Type | Description |
|--------------|------|-------------|
| `order_price` | `float` | Stop-loss/take-profit price (rounded). |

##### **Modifications**:
- **Inputs**:
  - **Do not remove `base_df`** (used in `setup_functions.py`).
  - Can add new parameters (e.g., volatility threshold).
- **Outputs**:
  - Must return a price value. Can add secondary returns (e.g., risk level).

##### **Example Modification**:
```python
# Added volatility_threshold to adjust SL dynamically
def set_stop_loss_price(base_df, signal, last_value, ..., volatility_threshold=2.0):
    if base_df["volatility"].iloc[-1] > volatility_threshold:
        stop_loss_multiplier *= 1.5  # Wider stop in volatile markets
    ...
    return order_price
```

---

#### **3. `prepare_base_df(base_df, max_window, test_span, train_span=None)`  
**Purpose**:  
Engineers features from raw OHLC data for model training/prediction.

##### **Inputs**:
| Parameter | Type | Required? | Description |
|-----------|------|-----------|-------------|
| `base_df` | `pd.DataFrame` | Yes | Raw OHLC data. |
| `max_window` | `int` | Yes | Max lookback window for technical indicators. |
| `test_span` | `int` | Yes | Test set size (avoids look-ahead bias). |
| `train_span` | `int` | Optional | Truncate training data to last `N` periods. |

##### **Outputs**:
| Return Value | Type | Description |
|--------------|------|-------------|
| `base_df` | `pd.DataFrame` | Processed data with features/targets. |
| `final_input_features` | `list` | Names of features used by the model. |

##### **Modifications**:
- **Inputs**:
  - **Do not remove `base_df`, `max_window`, or `test_span`** (critical for pipeline).
  - Can add new parameters (e.g., `feature_lags`).
- **Outputs**:
  - Must return the processed DataFrame and feature list.  
  - Can add tertiary returns (e.g., stationarity flags).

##### **Example Modification**:
```python
# Added feature_lags to control lagged features
def prepare_base_df(base_df, max_window, ..., feature_lags=5):
    for lag in range(1, feature_lags):
        ...
    return base_df, final_input_features
```

---

#### **4. `get_signal(base_df, purged_window_size, ...)`  
**Purpose**:  
Generates trading signals using pre-trained HMM and classifier models.

##### **Inputs**:
| Parameter | Type | Required? | Description |
|-----------|------|-----------|-------------|
| `base_df` | `pd.DataFrame` | Yes | Feature-engineered data from `prepare_base_df`. |
| `purged_window_size` | `int` | Yes | Periods to exclude around splits. |
| `embargo_period` | `int` | Yes | Buffer to prevent data leakage. |
| `market_open_time` | `datetime` | Yes | Timestamp to load date-specific models. |
| `final_input_features` | `list` | Yes | Features used for prediction. |
| `leverage` | `float` | Yes | Leverage multiplier for position sizing. |

##### **Outputs**:
| Return Value | Type | Description |
|--------------|------|-------------|
| `signal` | `float` | Trading signal (`-1`, `0`, `1`). |
| `leverage` | `float` | Leverage value (unchanged by default). |

##### **Modifications**:
- **Inputs**:
  - **Do not remove any parameters** (used in `setup_functions.py`).
  - Can add new inputs (e.g., `volatility_filter`).
- **Outputs**:
  - Must return `signal` and `leverage`.  
  - Can add auxiliary outputs (e.g., confidence score).

##### **Example Modification**:
```python
# Added model_confidence to return prediction probability
def get_signal(...):
    signal = model.predict(...)
    proba = model.predict_proba(...)
    return signal, leverage, proba
```

---

#### **5. `strategy_parameter_optimization(...)`  
**Purpose**:  
Backtests strategy, selects features, trains models, and saves artifacts.

##### **Inputs**:
| Parameter | Type | Required? | Description |
|-----------|------|-----------|-------------|
| `seed` | `int` | Yes | Random seed for reproducibility. |
| `data_frequency` | `str` | Yes | Resampling frequency (e.g., `"15min"`). |
| `max_window` | `int` | Yes | Max lookback window for indicators. |
| `base_df_address` | `str` | Yes | Path to save/load `base_df`. |
| `purged_window_size` | `int` | Yes | Periods to purge around splits. |
| `embargo_period` | `int` | Yes | Buffer after purging. |
| `train_span` | `int` | Optional | Training data truncation. |
| `test_span` | `int` | Yes | Test set size. |
| `historical_minute_data_address` | `str` | Yes | Path to raw OHLC data. |
| `market_open_time` | `datetime` | Yes | Date to format saved models. |

##### **Outputs**:
- Saves models to disk (`hmm_model_*.pickle`, `model_object_*.pickle`).  
- No explicit return value.

##### **Modifications**:
- **Inputs**:
  - **Do not remove any parameters** (orchestrates the full pipeline).
  - Can add new parameters (e.g., `sharpe_threshold`).
- **Outputs**:
  - Can add return values (e.g., backtest metrics).

---

### Critical Notes for Modifications:
1. **`base_df` is mandatory** in all functions where it appears. Removing it will break downstream code.
2. **Function signatures** used in `setup_functions.py` (e.g., `get_signal`, `prepare_base_df`) must retain their core inputs/outputs.
3. Test changes thoroughly—modifying input orders or return types may cause runtime errors.
4. To add new features, edit `prepare_base_df` (e.g., new technical indicators).
