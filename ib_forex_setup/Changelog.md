
# Changelog

This document outlines the relevant modifications made between a version and its subsequent one.

## Licensed under the Apache License, Version 2.0 (the "License")
- Copyright 2025 QuantInsti Quantitative Learnings Pvt Ltd. 
- You may not use this file except in compliance with the License. 
- You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
- Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

## Changelog: IB Forex Setup Version 1.0.0 to 1.0.1

This document outlines the relevant modifications made between version 1.0.0 and version 1.0.1 of the IB Forex Setup.

### I. Major Structural and File Changes

* **Introduction of `user_config` Directory:**
    * Version 1.0.1 introduces a new top-level directory named `user_config` located at `all_trading_setups/ib_forex_setup_1_0_1/user_config/`.
    * This directory centralizes user-specific configurations and data, replacing the `samples` directory found in version 1.0.0 (which was located at `all_trading_setups/ib_forex_setup_1_0_0/samples/`).
    * **Contents of `user_config` in 1.0.1:**
        * `main.py`: User-configurable main script to run the trading setup.
        * `strategy.py`: User-definable strategy logic.
        * `__init__.py` (empty).
        * `data/`: A subdirectory for user-specific data, including:
            * `models/__init__.py` (empty)
            * `reports/__init__.py` (empty)
            * `log/__init__.py` (empty)
    * This change indicates a shift towards a more modular design where user-specific files are clearly separated from the core application logic.

* **Removal of `samples` Directory:**
    * The `all_trading_setups/ib_forex_setup_1_0_0/samples/` directory and its contents (including `main.py`, `strategy.py`, and `data` subfolder) have been removed in version 1.0.1. Its role is now fulfilled by the `user_config` directory.

* **Removal of `previous_versions` Directory:**
    * The directory `all_trading_setups/ib_forex_setup_1_0_0/previous_versions/`, which contained `version_1_0_0/changelog.py`, has been removed in version 1.0.1.

* **New Developer Documentation:**
    * Version 1.0.1 adds a new documentation file: `all_trading_setups/ib_forex_setup_1_0_1/doc/Developer_documentation.md`. This document provides guidelines for modifying the source code, rebuilding the package, and running the modified setup.

### II. Documentation Content Updates

* **`README.md`**:
    * The Quick start section in version 1.0.1 now instructs users to download the user_config folder instead of the samples folder.
    * The installation command for the package has been updated to reflect the new version: `pip install ib_forex_setup/dist/qi_forex_setup-1.0.1-py3-none-any.whl` (previously `...-1.0.0-...`).
    * References to paths for `main.py` and data folders have been updated to point to the new `user_config` directory structure.

* **`doc/Start_here_documentation.md`**:
    * Version updated from 1.0.0 to 1.0.1, and Last Updated date changed to 2025-05-28.
    * References to the `samples` folder have been updated to `user_config`.
    * The Setup of variables section in 1.0.1 now details variables expected in `user_config/main.py`. Notable changes include:
        * `leverage`: Now listed as an optional variable that can be set to `None`. In 1.0.0, `samples/main.py` had a fixed `leverage = 1`. The 1.0.1 `user_config/main.py` shows `leverage = None`.
        * `trail`: A new boolean variable introduced in 1.0.1s `user_config/main.py` to enable/disable trailing stop loss.
        * `random_seeds`: In 1.0.0 `samples/main.py`, this was generated as `list(np.random.randint(low = 1, high = 10000001, size = 1000000))[:3]` using `seed = 2024`. In 1.0.1s `user_config/main.py`, a single `seed = 2025` is defined (though `seed = 2024` is also present but commented out or overridden), and the `random_seeds` list itself is not directly defined in `user_config/main.py` but rather generated within `engine.py` based on the provided `seed`.
        * **Removed Variables from `main.py` configuration in 1.0.1 (previously in 1.0.0 `samples/main.py`):**
            * `max_window`
            * `purged_window_size`
            * `embargo_period`
            * `risk_management_target`
            * `stop_loss_multiplier`
            * `take_profit_multiplier`
            * These parameters appear to be managed differently or have fixed values within the core strategy/setup functions in 1.0.1.

* **`doc/Strategy_documentation.md`**:
    * Version updated from 1.0.0 to 1.0.1, and Last Updated date changed to 2025-05-28.
    * The documentation now reflects that certain functions (`get_signal`, `set_stop_loss_price`, `set_take_profit_price`) receive an `app` object as a primary means of accessing necessary data (like `base_df`, `signal`, `last_value`, `final_input_features`, `market_open_time`).
    * Mentions that `leverage` can be `None` in 1.0.1 if not set in `user_config/main.py`, implying the strategy or `app` object might handle its default or derivation.
    * The description of `set_stop_loss_price` and `set_take_profit_price` indicates they now use the `app` object for context (like `app.signal`, `app.last_value`) and internally defined risk parameters (0.3% target, 1x multiplier), whereas in 1.0.0 these risk parameters were passed directly to the functions.
    * The signature of `prepare_base_df` is simplified. While `historical_data` remains key, `train_span` is optional, and other parameters like `max_window`, `test_span`, `scalable_features` (from 1.0.0s `strategy.py`) are handled differently, likely internally or derived from the calling context in 1.0.1.
    * `strategy_parameter_optimization` in 1.0.1 has a more streamlined set of parameters, relying on context (e.g., `market_open_time` for model naming) and `main.py` variables. It now saves `optimal_features_df.xlsx` to `data/models/` within the `user_config` structure (if running from there, or relative to `src` if models are saved by the package) instead of a root `data/` directory.

* **`doc/The_trading_setup_references.md`**:
    * No significant content changes were observed between versions.

### III. Core Code Modifications (`src` directory files)

* **`src/ib_functions.py`**:
    * `stopOrder()` function in 1.0.1:
        * Added a `trail` boolean parameter.
        * If `trail` is `True`, `order.orderType` is set to `TRAIL` and `order.trailStopPrice` is set to `st_price`.
        * If `trail` is `False`, `order.orderType` remains `STP`.

* **`src/setup_for_download_data.py`**:
    * In the `app_for_download_data.__init__` method:
        * The condition for returning early when `update == true` has been slightly modified. In 1.0.1, if `len(self.saturdays)==1` and `self.saturdays[0] >= first_date`, the function returns. This specific combination was not explicitly present in 1.0.0.
    * In `update_historical_resampled_data` function (1.0.1):
        * A check is added to see if resampling was already done by comparing the last day of `historical_minute_data` with the last day of `historical_resampled_data`. If they are the same or the minute data is only one day ahead, it prints `Resampling was already done...` and skips the process. This check is more explicit than in 1.0.0.
        * Explicit print statements like `Resample of historical minute data as per the data frequency is in process...` and `...is completed...` have been added.

* **`src/trading_functions.py`**:
    * `get_capital_as_per_forex_base_currency()` in 1.0.1:
        * When fetching exchange rates from Yahoo Finance, the ticker construction for USD/contract_symbol and USD/account_currency is `fUSD{app.contract.symbol}=X` and `fUSD{app.account_currency}=X` respectively. It then specifically extracts the `EURUSD=X` column from the downloaded data for both. This hardcoded extraction might be an issue if the primary pair used by `yf.download` for multiple tickers is not always EURUSD or if the intended pair is not EURUSD. Version 1.0.0 directly used the result of individual `yf.download` calls for `fUSD{app.contract.symbol}=X` and `fUSD{app.account_currency}=X`.
    * `get_the_closest_periods()` in 1.0.1:
        * The logic for the `elif now_ < day_start_datetime:` condition has changed. If `periods[-2] == trading_day_end_datetime`, it sets `previous_period`, `current_period`, and `next_period` to `periods[-3]`, `trading_day_end_datetime`, and `day_start_datetime` respectively. This replaces the logic in `get_the_closest_periods_old()` from 1.0.0.
    * New utility functions added in 1.0.1:
        * `extract_variables(source_file)`: Reads a Python source file, parses it using `ast`, and extracts variable assignments, attempting to evaluate literal values.
        * `get_return_variable_names(filename, function_name)`: Uses `ast` to parse a Python file and find the names of variables returned by a specified function.

* **`src/setup.py` (class `trading_app`)**:
    * **`__init__` method:**
        * Parameters removed in 1.0.1: `leverage`, `risk_management_target`, `stop_loss_multiplier`, `take_profit_multiplier`, `purged_window_size`, `embargo_period`, `max_window`. These are now managed differently (e.g., via `user_config/main.py`, within `strategy.py`, or fixed internally).
        * New parameter `trail` (boolean) added in 1.0.1.
        * Loading of `optimal_features_df.xlsx`: In 1.0.1, it attempts to load from `data/models/optimal_features_df.xlsx` (relative to where the script is run, typically `user_config` or the packages data path). In 1.0.0, it loaded from `data/optimal_features_df.xlsx` (relative to `samples` or the packages data path).
        * The attributes `self.scalable_features` and `self.final_input_features` are loaded by parsing columns from `optimal_features_df.xlsx` in 1.0.1. Version 1.0.0 assigned them directly from the DataFrame columns.
    * Callback methods `orderStatus`, `execDetails`, and `position` in 1.0.1 now ensure relevant quantity/position values are converted to `float`.

* **`src/setup_functions.py`**:
    * `update_hist_data()`:
        * The `days_passed_number` calculation for `durationStr` in `reqHistoricalData` has a slight adjustment: `days_passed = f{days_passed_number if days_passed_number > 1 else (days_passed_number + 2)} D` (1.0.1) vs. `days_passed = f{days_passed_number if days_passed_number > 0 else (days_passed_number + 2)} D` (1.0.0).
        * Multithreading for `download_hist_data` is commented out in 1.0.1, and calls are made sequentially.
    * `cancel_previous_stop_loss_order()` and `cancel_previous_take_profit_order()` in 1.0.1 now use `app.cancelOrder(order_id, OrderCancel())` instead of `app.cancelOrder(order_id, "")`.
    * `send_stop_loss_order()`:
        * Uses `app.trail` to decide the stop order type (STP or TRAIL) via `ibf.stopOrder(..., app.trail)`.
        * Retrieves stop loss price using `stra.set_stop_loss_price(app)` (which takes the `app` object) instead of passing individual parameters like `app.signal`, `app.last_value`, etc.
    * `send_take_profit_order()`:
        * Retrieves take profit price using `stra.set_take_profit_price(app)` instead of passing individual parameters.
    * `send_orders()`:
        * Logic for determining `app.previous_leverage` and `app.previous_signal` from `app.cash_balance` is added.
        * Order sending conditions are restructured, primarily checking `if app.previous_leverage == app.leverage:`.
        * When adjusting positions due to leverage changes, if `new_quantity` implies a change in position direction, `app.signal` is adjusted accordingly.
        * The call to `send_orders_as_bracket` may include a `rm_quantity` parameter in some scenarios.
    * `strategy()`:
        * Uses `tf.extract_variables(main.py)` to get variables from `user_config/main.py`.
        * Uses `tf.get_return_variable_names(strategy.py, prepare_base_df)` and `tf.get_return_variable_names(strategy.py, get_signal)` to dynamically determine return variable names from `user_config/strategy.py`.
        * Passes parameters to `stra.prepare_base_df()` and `stra.get_signal()` more dynamically based on their signatures and available variables in the `app` object and from `main.py`.
        * Handles `leverage` assignment: if `leverage` is returned by `get_signal`, it is used. Otherwise, if `app.leverage` (from `trading_app` instance, potentially `None`) is used, or if `leverage` is in variables from `main.py`, that is prioritized.
    * `run_strategy_for_the_period()`: Multithreading for `run_strategy` and `connection_monitor` is commented out in 1.0.1.
    * `send_email()`: In 1.0.1, when retrieving order details for the email, it checks `app.trail` to determine if the stop order type is `TRAIL` or `STP`.

* **`src/engine.py`**:
    * `run_app()`:
        * When initializing `trading_app`, parameters like `leverage`, `risk_management_target`, etc., are no longer passed as they are removed from `trading_app.__init__`.
        * The `trail` parameter is added to the `trading_app` instantiation.
    * `run_trading_setup_loop()`: Similarly, parameters removed from `trading_app.__init__` are no longer passed. The `trail` parameter is added.
    * `main()`:
        * Uses `tf.extract_variables(main.py)` (from `user_config` context) to load variables.
        * Variables like `leverage`, `risk_management_target`, `max_window`, `purged_window_size`, `embargo_period`, `random_seeds` are no longer explicitly fetched from these variables to be passed to `trading_app` or `strategy_parameter_optimization`, as their handling has changed. `trail` is fetched.
        * When calling `stra.strategy_parameter_optimization`, the signature has changed. It now takes fewer direct arguments, inferring some from the `app` context or `variables` loaded from `main.py`. It uses a more dynamic way to pass arguments based on the functions signature.
        * Model and feature files (e.g., `stra_opt_...pickle`, `optimal_features_df.xlsx`) are now expected to be saved under a `data/models/` subfolder (relative to where the script is run, likely `user_config`).
        * The logic for checking if `stra_opt_...pickle` exists determines if `strategy_parameter_optimization` needs to be run.

* **`src/create_database.py`**:
    * No significant changes observed in the structure or columns of the created Excel database (`database.xlsx`) or `email_info.xlsx`.

### IV. Summary of Key Functional Changes

1.  **Configuration Management**: Major shift from a `samples` folder to a dedicated, user-managed `user_config` directory for `main.py`, `strategy.py`, and user-specific data/models/logs. This promotes better separation of user code and application code.
2.  **Parameter Handling & Decoupling**:
    * Many parameters previously defined in `samples/main.py` (1.0.0) and passed through `engine.py` to core `trading_app` and strategy functions (e.g., `leverage`, `risk_management_target`, `max_window`, `purged_window_size`, `embargo_period`) are no longer explicitly passed in this way in 1.0.1.
    * In 1.0.1, these parameters are either:
        * Read directly from `user_config/main.py` within `engine.py` or `setup_functions.py` using `tf.extract_variables`.
        * Handled internally within `user_config/strategy.py` (e.g., risk parameters in `set_stop_loss_price`).
        * Passed via the `app` object to strategy functions.
        * Some (like `max_window`) seem to be implicitly handled or have fixed values within the strategy logic.
3.  **Trailing Stop Loss**: Introduction of a `trail` boolean parameter (configurable in `user_config/main.py`) to enable trailing stop-loss orders.
4.  **Dynamic Function Argument Passing**: `src/engine.py` and `src/setup_functions.py` in 1.0.1 now use `inspect` and custom `ast` utilities (`tf.extract_variables`, `tf.get_return_variable_names`) to more dynamically call functions from `strategy.py` and pass parameters based on their signatures.
5.  **Code Structure & Readability**:
    * `setup_functions.py` (1.0.1) makes more direct calls to functions in `strategy.py` (from `user_config`), often passing the `app` object for context.
    * Multithreading in some parts of `setup_functions.py` (e.g., `update_hist_data`, `run_strategy_for_the_period`) has been commented out in 1.0.1, favoring sequential execution for those specific tasks.
6.  **Model/Data Storage Paths**: Optimization artifacts (trained models, feature lists like `optimal_features_df.xlsx`) are now consistently referred to be saved within a `data/models/` subdirectory. Given the `user_config` structure, this implies these would be within `user_config/data/models/`.
7.  **Strategy File Interface (`user_config/strategy.py` in 1.0.1 vs. `samples/strategy.py` in 1.0.0)**:
    * Functions like `set_stop_loss_price`, `set_take_profit_price`, and `get_signal` in 1.0.1s strategy template now primarily expect an `app` object as input, from which they derive necessary context (e.g., `app.signal`, `app.last_value`, `app.base_df`). This is a shift from 1.0.0 where these functions took more individual parameters.
    * `prepare_base_df` and `strategy_parameter_optimization` in 1.0.1 have revised signatures reflecting the new way parameters are sourced (often from `user_config/main.py` via the `engine` or directly within the strategy).
