# --- Do not remove these libs ----------------------------------------------------------------------
import os
import sys
from scipy.interpolate import interp1d
import freqtrade.vendor.qtpylib.indicators as qtpylib
import logging
import numpy as np  # noqa
import pandas as pd  # noqa
import talib.abstract as ta
from datetime import datetime, timedelta
from freqtrade.exchange import timeframe_to_prev_date
from freqtrade.persistence import Trade
from freqtrade.strategy \
    import IStrategy, CategoricalParameter, IntParameter, merge_informative_pair, timeframe_to_minutes
from freqtrade.state import RunMode
from numpy import timedelta64
from pandas import DataFrame
import json
from typing import List  # stoploss search space
from freqtrade.optimize.space import Dimension, SKDecimal # stoploss search space

logger = logging.getLogger(__name__)


# ^ TA-Lib Autofill mostly broken in JetBrains Products,
# ta._ta_lib.<function_name> can temporarily be used while writing as a workaround
# Then change back to ta.<function_name> so IDE won't nag about accessing a protected member of TA-Lib
# ----------------------------------------------------------------------------------------------------
def init_vars(parameter_dictionary: dict, parameter_name: str, parameter_min_value: int, parameter_max_value: int,
              parameter_threshold: int, precision: float, overrideable: bool = True):
    """
    Function to automatically initialize MoniGoMani's HyperOptable parameter values for both HyperOpt Runs.

    :param parameter_dictionary: Buy or Sell params dictionary
    :param parameter_name: Name of the signal in the dictionary
    :param parameter_min_value: Minimal search space value to use during the 1st HyperOpt Run and override value for weak signals on the 2nd HyperOpt Run 
    :param parameter_max_value: Maximum search space value to use during the 1st HyperOpt Run and override value for weak signals on the 2nd HyperOpt Run 
    :param parameter_threshold: Threshold to use for overriding weak/strong signals and setting up refined search spaces after the 1st HyperOpt Run
    :param precision: Precision used while HyperOpting
    :param overrideable: Allow value to be overrideable or not (defaults to 'True')
    :return: Dictionary containing the search space values to use during the HyperOpt Runs
    """
    parameter_value = parameter_dictionary.get(parameter_name)

    # 1st HyperOpt Run: Use provided min/max values for the search spaces
    if parameter_value is None:
        min_value = parameter_min_value
        max_value = parameter_max_value
    # 2nd HyperOpt Run: Use refined search spaces where needed
    else:
        min_value = parameter_min_value if parameter_value <= (parameter_min_value + parameter_threshold) else \
            parameter_value - parameter_threshold
        max_value = parameter_max_value if parameter_value >= (parameter_max_value - parameter_threshold) else \
            parameter_value + parameter_threshold

    # 1st HyperOpt Run: Use middle of min/max values as default value
    if parameter_value is None:
        default_value = int((parameter_min_value + parameter_max_value) / 2)
    # 2nd HyperOpt Run: Use Overrides where needed for default value
    elif (max_value == parameter_max_value) and (overrideable is True):
        default_value = parameter_max_value
    elif min_value == parameter_min_value and (overrideable is True):
        default_value = parameter_min_value
    # 2nd HyperOpt Run: Use values found in Run 1 for the remaining default values
    else:
        default_value = parameter_value

    return_vars_dictionary = {
        "min_value": int(min_value * precision),
        "max_value": int(max_value * precision),
        "default_value": int(default_value * precision),
        # 1st HyperOpt Run: No overrides, 2nd HyperOpt Run: Apply Overrides where needed
        "opt_and_Load": False if (parameter_value is not None) and (overrideable is True) and
                                 (min_value == parameter_min_value or max_value == parameter_max_value) else True
    }

    return return_vars_dictionary


class MoniGoManiHyperStrategy(IStrategy):
    """
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.11.0 by Rikj000                        ###
    ##                          -----------------------------                         ##
    #               Isn't that what we all want? Our money to go many?                 #
    #          Well that's what this Freqtrade strategy hopes to do for you!           #
    ##       By giving you/HyperOpt a lot of signals to alter the weight from         ##
    ###           ------------------------------------------------------             ###
    ##        Big thank you to xmatthias and everyone who helped on MoniGoMani,       ##
    ##      Freqtrade Discord support was also really helpful so thank you too!       ##
    ###         -------------------------------------------------------              ###
    ##              Disclaimer: This strategy is under development.                   ##
    #      I do not recommend running it live until further development/testing.       #
    ##                      TEST IT BEFORE USING IT!                                  ##
    ###                                                              ▄▄█▀▀▀▀▀█▄▄     ###
    ##               -------------------------------------         ▄█▀  ▄ ▄    ▀█▄    ##
    ###   If you like my work, feel free to donate or use one of   █   ▀█▀▀▀▀▄   █   ###
    ##   my referral links, that would also greatly be appreciated █    █▄▄▄▄▀   █    ##
    #     ICONOMI: https://www.iconomi.com/register?ref=JdFzz      █    █    █   █     #
    ##  Binance: https://www.binance.com/en/register?ref=97611461  ▀█▄ ▀▀█▀█▀  ▄█▀    ##
    ###          BTC: 19LL2LCMZo4bHJgy15q1Z1bfe7mV4bfoWK             ▀▀█▄▄▄▄▄█▀▀     ###
    ####                                                                            ####
    ####################################################################################
    """

    ####################################################################################################################
    #                                           START OF CONFIG NAMES SECTION                                          #
    ####################################################################################################################
    mgm_config_name = 'mgm-config.json'
    mgm_config_hyperopt_name = 'mgm-config-hyperopt.json'
    ####################################################################################################################
    #                                            END OF CONFIG NAMES SECTION                                           #
    ####################################################################################################################

    # Load the MoniGoMani settings
    mgm_config_path = os.getcwd() + '/user_data/' + mgm_config_name
    if os.path.isfile(mgm_config_path) is True:
        # Load the 'mgm-config.json' file as an object and parse it as a dictionary
        file_object = open(mgm_config_path, )
        json_data = json.load(file_object)
        mgm_config = json_data['monigomani_settings']

    else:
        sys.exit(f'MoniGoManiHyperStrategy - ERROR - The main MoniGoMani configuration file ({mgm_config_name}) can\'t '
                 f'be found at: {mgm_config_path}... Please provide the correct file and/or alter "mgm_config_name" in '
                 f'"MoniGoManiHyperStrategy.py"')

    # Apply the loaded MoniGoMani Settings
    timeframe = mgm_config['timeframe']
    backtest_timeframe = mgm_config['backtest_timeframe']
    startup_candle_count = mgm_config['startup_candle_count']
    precision = mgm_config['precision']
    min_weighted_signal_value = mgm_config['min_weighted_signal_value']
    max_weighted_signal_value = mgm_config['max_weighted_signal_value']
    min_trend_total_signal_needed_value = mgm_config['min_trend_total_signal_needed_value']
    min_trend_total_signal_needed_candles_lookback_window_value = \
        mgm_config['min_trend_total_signal_needed_candles_lookback_window_value']
    max_trend_total_signal_needed_candles_lookback_window_value = \
        mgm_config['max_trend_total_signal_needed_candles_lookback_window_value']
    search_threshold_weighted_signal_values = mgm_config['search_threshold_weighted_signal_values']
    search_threshold_trend_total_signal_needed_candles_lookback_window_value = \
        mgm_config['search_threshold_trend_total_signal_needed_candles_lookback_window_value']
    number_of_weighted_signals = mgm_config['number_of_weighted_signals']
    roi_table_step_size = mgm_config['roi_table_step_size']
    stoploss_max_value = -0.35 if mgm_config['stoploss_max_value'] == None else mgm_config['stoploss_max_value']
    debuggable_weighted_signal_dataframe = mgm_config['debuggable_weighted_signal_dataframe']
    use_mgm_logging = mgm_config['use_mgm_logging']
    mgm_log_levels_enabled = mgm_config['mgm_log_levels_enabled']

    # Initialize empty buy/sell_params dictionaries and initial (trailing)stoploss values
    buy_params = {}
    sell_params = {}
    stoploss = -0.25
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    # If results from a previous HyperOpt Run are found then continue the next HyperOpt Run upon them
    mgm_config_hyperopt_path = os.getcwd() + '/user_data/' + mgm_config_hyperopt_name
    if os.path.isfile(mgm_config_hyperopt_path) is True:
        # Load the previous 'mgm-config-hyperopt.json' file as an object and parse it as a dictionary
        file_object = open(mgm_config_hyperopt_path, )
        mgm_config_hyperopt = json.load(file_object)

        # Convert the loaded 'mgm-config-hyperopt.json' data to the needed HyperOpt Results format
        for param in mgm_config_hyperopt['params']:
            param_value = mgm_config_hyperopt['params'][str(param)]
            if (isinstance(param_value, str) is True) and (str.isdigit(param_value) is True):
                param_value = int(param_value)

            if str(param).startswith('buy'):
                buy_params[str(param)] = param_value
            else:
                sell_params[str(param)] = param_value

        minimal_roi = mgm_config_hyperopt['minimal_roi']
        stoploss = mgm_config_hyperopt['stoploss']
        if isinstance(mgm_config_hyperopt['trailing_stop'], str) is True:
            trailing_stop = bool(mgm_config_hyperopt['trailing_stop'])
        else:
            trailing_stop = mgm_config_hyperopt['trailing_stop']
        trailing_stop_positive = mgm_config_hyperopt['trailing_stop_positive']
        trailing_stop_positive_offset = mgm_config_hyperopt['trailing_stop_positive_offset']
        if isinstance(mgm_config_hyperopt['trailing_only_offset_is_reached'], str) is True:
            trailing_only_offset_is_reached = bool(mgm_config_hyperopt['trailing_only_offset_is_reached'])
        else:
            trailing_only_offset_is_reached = mgm_config_hyperopt['trailing_only_offset_is_reached']

    ####################################################################################################################
    #                                 START OF HYPEROPT PARAMETERS CONFIGURATION SECTION                               #
    ####################################################################################################################

    # ---------------------------------------------------------------- #
    #                  Buy HyperOpt Space Parameters                   #
    # ---------------------------------------------------------------- #

    # React to Buy Signals when certain trends are detected (False would disable trading in said trend)
    buy___trades_when_downwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)
    buy___trades_when_sideways = \
        CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
    buy___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)

    # ---------------------------------------------------------------- #
    #                  Sell HyperOpt Space Parameters                  #
    # ---------------------------------------------------------------- #

    # React to Sell Signals when certain trends are detected (False would disable trading in said trend)
    sell___trades_when_downwards = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___trades_when_sideways = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)
    sell___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)

    # ---------------------------------------------------------------- #
    #             Sell Unclogger HyperOpt Space Parameters             #
    # ---------------------------------------------------------------- #

    sell___unclogger_enabled = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)

    param = init_vars(sell_params, "sell___unclogger_minimal_losing_trade_duration_minutes",
                      15, 60, search_threshold_weighted_signal_values, precision, False)
    sell___unclogger_minimal_losing_trade_duration_minutes = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell___unclogger_minimal_losing_trades_open",
                      1, 5, 1, precision, False)
    sell___unclogger_minimal_losing_trades_open = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell___unclogger_open_trades_losing_percentage_needed",
                      1, 60, search_threshold_weighted_signal_values, precision, False)
    sell___unclogger_open_trades_losing_percentage_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell___unclogger_trend_lookback_candles_window",
                      10, 60, search_threshold_weighted_signal_values, precision, False)
    sell___unclogger_trend_lookback_candles_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell___unclogger_trend_lookback_candles_window_percentage_needed",
                      10, 40, search_threshold_weighted_signal_values, precision, False)
    sell___unclogger_trend_lookback_candles_window_percentage_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    sell___unclogger_trend_lookback_window_uses_downwards_candles = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_sideways_candles = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_upwards_candles = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)

    ####################################################################################################################
    #                                   END OF HYPEROPT PARAMETERS CONFIGURATION SECTION                               #
    ####################################################################################################################

    # Below HyperOpt Space Parameters should preferably be tweaked using the 'monigomani_settings' section inside
    # 'mgm-config.json'. But they can still be manually tweaked if truly needed!

    # ---------------------------------------------------------------- #
    #                  Buy HyperOpt Space Parameters                   #
    # ---------------------------------------------------------------- #

    # Downwards Trend Buy
    # -------------------

    # Total Buy Signal Percentage needed for a signal to be positive
    param = init_vars(buy_params, "buy__downwards_trend_total_signal_needed", min_trend_total_signal_needed_value,
                      int(max_weighted_signal_value * number_of_weighted_signals),
                      search_threshold_weighted_signal_values, precision)
    buy__downwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy__downwards_trend_total_signal_needed_candles_lookback_window",
                      min_trend_total_signal_needed_candles_lookback_window_value,
                      max_trend_total_signal_needed_candles_lookback_window_value,
                      search_threshold_trend_total_signal_needed_candles_lookback_window_value, precision, False)
    buy__downwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Buy Signal Weight Influence Table
    param = init_vars(buy_params, "buy_downwards_trend_adx_strong_up_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_adx_strong_up_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_bollinger_bands_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_ema_long_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_ema_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_ema_short_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_ema_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_macd_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_rsi_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_sma_long_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_sma_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_sma_short_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_sma_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_vwap_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_downwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sideways Trend Buy
    # ------------------

    # Total Buy Signal Percentage needed for a signal to be positive
    param = init_vars(buy_params, "buy__sideways_trend_total_signal_needed",
                      min_trend_total_signal_needed_value, int(max_weighted_signal_value * number_of_weighted_signals),
                      search_threshold_weighted_signal_values, precision)
    buy__sideways_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy__sideways_trend_total_signal_needed_candles_lookback_window",
                      min_trend_total_signal_needed_candles_lookback_window_value,
                      max_trend_total_signal_needed_candles_lookback_window_value,
                      search_threshold_trend_total_signal_needed_candles_lookback_window_value, precision, False)
    buy__sideways_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Buy Signal Weight Influence Table
    param = init_vars(buy_params, "buy_sideways_trend_adx_strong_up_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_adx_strong_up_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_bollinger_bands_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_ema_long_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_ema_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_ema_short_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_ema_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_macd_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_rsi_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_sma_long_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_sma_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_sma_short_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_sma_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_vwap_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_sideways_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Upwards Trend Buy
    # -----------------

    # Total Buy Signal Percentage needed for a signal to be positive
    param = init_vars(buy_params, "buy__upwards_trend_total_signal_needed",
                      min_trend_total_signal_needed_value, int(max_weighted_signal_value * number_of_weighted_signals),
                      search_threshold_weighted_signal_values, precision)
    buy__upwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy__upwards_trend_total_signal_needed_candles_lookback_window",
                      min_trend_total_signal_needed_candles_lookback_window_value,
                      max_trend_total_signal_needed_candles_lookback_window_value,
                      search_threshold_trend_total_signal_needed_candles_lookback_window_value, precision, False)
    buy__upwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Buy Signal Weight Influence Table
    param = init_vars(buy_params, "buy_upwards_trend_adx_strong_up_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_adx_strong_up_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_bollinger_bands_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_ema_short_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_ema_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_ema_long_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_ema_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_macd_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_rsi_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_sma_long_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_sma_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_sma_short_golden_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_sma_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_vwap_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    buy_upwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # ---------------------------------------------------------------- #
    #                  Sell HyperOpt Space Parameters                  #
    # ---------------------------------------------------------------- #

    # Downwards Trend Sell
    # --------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    param = init_vars(sell_params, "sell__downwards_trend_total_signal_needed",
                      min_trend_total_signal_needed_value, int(max_weighted_signal_value * number_of_weighted_signals),
                      search_threshold_weighted_signal_values, precision)
    sell__downwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell__downwards_trend_total_signal_needed_candles_lookback_window",
                      min_trend_total_signal_needed_candles_lookback_window_value,
                      max_trend_total_signal_needed_candles_lookback_window_value,
                      search_threshold_trend_total_signal_needed_candles_lookback_window_value, precision, False)
    sell__downwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sell Signal Weight Influence Table
    param = init_vars(sell_params, "sell_downwards_trend_adx_strong_down_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_adx_strong_down_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_bollinger_bands_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_ema_long_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_ema_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_ema_short_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_ema_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_macd_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_rsi_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_sma_long_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_sma_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_sma_short_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_sma_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_vwap_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_downwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sideways Trend Sell
    # -------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    param = init_vars(sell_params, "sell__sideways_trend_total_signal_needed",
                      min_trend_total_signal_needed_value, int(max_weighted_signal_value * number_of_weighted_signals),
                      search_threshold_weighted_signal_values, precision)
    sell__sideways_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell__sideways_trend_total_signal_needed_candles_lookback_window",
                      min_trend_total_signal_needed_candles_lookback_window_value,
                      max_trend_total_signal_needed_candles_lookback_window_value,
                      search_threshold_trend_total_signal_needed_candles_lookback_window_value, precision, False)
    sell__sideways_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sell Signal Weight Influence Table
    param = init_vars(sell_params, "sell_sideways_trend_adx_strong_down_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_adx_strong_down_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_bollinger_bands_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_ema_long_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_ema_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_ema_short_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_ema_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_macd_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_rsi_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_sma_long_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_sma_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_sma_short_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_sma_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_vwap_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_sideways_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Upwards Trend Sell
    # ------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    param = init_vars(sell_params, "sell__upwards_trend_total_signal_needed",
                      min_trend_total_signal_needed_value, int(max_weighted_signal_value * number_of_weighted_signals),
                      search_threshold_weighted_signal_values, precision)
    sell__upwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell__upwards_trend_total_signal_needed_candles_lookback_window",
                      min_trend_total_signal_needed_candles_lookback_window_value,
                      max_trend_total_signal_needed_candles_lookback_window_value,
                      search_threshold_trend_total_signal_needed_candles_lookback_window_value, precision, False)
    sell__upwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sell Signal Weight Influence Table
    param = init_vars(sell_params, "sell_upwards_trend_adx_strong_down_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_adx_strong_down_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_bollinger_bands_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_ema_long_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_ema_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_ema_short_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_ema_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_macd_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_rsi_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_sma_long_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_sma_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_sma_short_death_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_sma_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_vwap_cross_weight", min_weighted_signal_value,
                      max_weighted_signal_value, search_threshold_weighted_signal_values, precision)
    sell_upwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Create dictionary to store custom information MoniGoMani will be using in RAM
    custom_info = {
        'open_trades': {}
    }

    # Initialize some parameters which will be automatically configured/used by MoniGoMani
    use_custom_stoploss = True  # Leave this enabled (Needed for open_trade custom_information_storage)
    is_dry_live_run_detected = True  # Class level runmode detection, Gets set automatically
    informative_timeframe = timeframe  # Gets set automatically
    timeframe_multiplier = None  # Gets set automatically

    # Plot configuration to show all signals used in MoniGoMani in FreqUI (Use load from Strategy in FreqUI)
    plot_config = {
        'main_plot': {
            # Main Plot Indicators (SMAs, EMAs, Bollinger Bands, VWAP)
            'sma9': {'color': '#2c05f6'},
            'sma50': {'color': '#19038a'},
            'sma200': {'color': '#0d043b'},
            'ema9': {'color': '#12e5a6'},
            'ema50': {'color': '#0a8963'},
            'ema200': {'color': '#074b36'},
            'bb_upperband': {'color': '#6f1a7b'},
            'bb_lowerband': {'color': '#6f1a7b'},
            'vwap': {'color': '#727272'}
        },
        'subplots': {
            # Subplots - Each dict defines one additional plot (MACD, ADX, Plus/Minus Direction, RSI)
            'MACD (Moving Average Convergence Divergence)': {
                'macd': {'color': '#19038a'},
                'macdsignal': {'color': '#ae231c'}
            },
            'ADX (Average Directional Index) + Plus & Minus Directions': {
                'adx': {'color': '#6f1a7b'},
                'plus_di': {'color': '#0ad628'},
                'minus_di': {'color': '#ae231c'}
            },
            'RSI (Relative Strength Index)': {
                'rsi': {'color': '#7fba3c'}
            }
        }
    }

    class HyperOpt:
        # Generate a Custom Long Continuous ROI-Table with less gaps in it
        @staticmethod
        def generate_roi_table(params):
            step = MoniGoManiHyperStrategy.roi_table_step_size
            minimal_roi = {0: params['roi_p1'] + params['roi_p2'] + params['roi_p3'],
                           params['roi_t3']: params['roi_p1'] + params['roi_p2'],
                           params['roi_t3'] + params['roi_t2']: params['roi_p1'],
                           params['roi_t3'] + params['roi_t2'] + params['roi_t1']: 0}

            max_value = max(map(int, minimal_roi.keys()))
            f = interp1d(
                list(map(int, minimal_roi.keys())),
                list(minimal_roi.values())
            )
            x = list(range(0, max_value, step))
            y = list(map(float, map(f, x)))
            if y[-1] != 0:
                x.append(x[-1] + step)
                y.append(0)
            return dict(zip(x, y))

        #define custom stoploss search space with configurable parameter max value
        @staticmethod
        def stoploss_space() -> List[Dimension]:
            """
            Stoploss Value to search
            Override it if you need some different range for the parameter in the
            'stoploss' optimization hyperspace.
            """
            return [
                SKDecimal(MoniGoManiHyperStrategy.stoploss_max_value, -0.02, decimals=3, name='stoploss'),
            ]
        
    def __init__(self, config: dict):
        """
        First method to be called once during the MoniGoMani class initialization process
        :param config::
        """

        super().__init__(config)
        initialization = 'Initialization'

        if RunMode(config.get('runmode', RunMode.OTHER)) in (RunMode.BACKTEST, RunMode.HYPEROPT):
            self.timeframe = self.backtest_timeframe
            self.mgm_logger('info', 'TimeFrame-Zoom', f'Auto updating to zoomed "backtest_timeframe": {self.timeframe}')

            self.is_dry_live_run_detected = False
            self.mgm_logger('info', initialization, f'Current run mode detected as: HyperOpting/BackTesting. '
                                                    f'Auto updated is_dry_live_run_detected to: False')

            self.mgm_logger('info', initialization, f'Calculating and storing "timeframe_multiplier" + Updating '
                                                    f'"startup_candle_count"')
            self.timeframe_multiplier = \
                int(timeframe_to_minutes(self.informative_timeframe) / timeframe_to_minutes(self.timeframe))
            if self.timeframe_multiplier < 1:
                raise SystemExit(f'MoniGoManiHyperStrategy - ERROR - TimeFrame-Zoom - "timeframe" must be bigger than '
                                 f'"backtest_timeframe"')
            self.startup_candle_count *= self.timeframe_multiplier

        else:
            if os.path.isfile(self.mgm_config_hyperopt_path) is False:
                sys.exit(f'MoniGoManiHyperStrategy - ERROR - The MoniGoMani HyperOpt Results configuration file '
                         f'({self.mgm_config_hyperopt_name}) can\'t be found at: {self.mgm_config_hyperopt_path}... '
                         f'Please Optimize your MoniGoMani before Dry/Live running! Once optimized provide the correct '
                         f'file and/or alter "mgm_config_hyperopt_name" in "MoniGoManiHyperStrategy.py"')

            self.is_dry_live_run_detected = True
            self.mgm_logger('info', initialization, f'Current run mode detected as: Dry/Live-Run. '
                                                    f'Auto updated is_dry_live_run_detected to: True')

    def informative_pairs(self):
        """
        Defines additional informative pair/interval combinations to be cached from the exchange, these will be used
        during TimeFrame-Zoom.
        :return:
        """
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds indicators based on Run-Mode & TimeFrame-Zoom:

        If Dry/Live-running or BackTesting/HyperOpting without TimeFrame-Zoom it just pulls 'timeframe' (1h candles) to
        compute indicators.

        If BackTesting/HyperOpting with TimeFrame-Zoom it pulls 'informative_pairs' (1h candles) to compute indicators,
        but then tests upon 'backtest_timeframe' (5m or 1m candles) to simulate price movement during that 'timeframe'
        (1h candle).

        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for MoniGoMani
        """
        timeframe_zoom = 'TimeFrame-Zoom'
        # Compute indicator data during Backtesting / Hyperopting when TimeFrame-Zooming
        if (self.is_dry_live_run_detected is False) and (self.informative_timeframe != self.backtest_timeframe):
            self.mgm_logger('info', timeframe_zoom, f'Backtesting/Hyperopting this strategy with a '
                                                    f'informative_timeframe ({self.informative_timeframe} candles) and '
                                                    f'a zoomed backtest_timeframe ({self.backtest_timeframe} candles)')

            # Warning! This method gets ALL downloaded data that you have (when in backtesting mode).
            # If you have many months or years downloaded for this pair, this will take a long time!
            informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)

            # Throw away older data that isn't needed.
            first_informative = dataframe["date"].min().floor("H")
            informative = informative[informative["date"] >= first_informative]

            # Populate indicators at a larger timeframe
            informative = self._populate_indicators(informative.copy(), metadata)

            # Merge indicators back in with, filling in missing values.
            dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe,
                                               ffill=True)

            # Rename columns, since merge_informative_pair adds `_<timeframe>` to the end of each name.
            # Skip over date etc..
            skip_columns = [(s + "_" + self.informative_timeframe) for s in
                            ['date', 'open', 'high', 'low', 'close', 'volume']]
            dataframe.rename(columns=lambda s: s.replace("_{}".format(self.informative_timeframe), "") if
            (not s in skip_columns) else s, inplace=True)

        # Compute indicator data normally during Dry & Live Running or when not using TimeFrame-Zoom
        else:
            self.mgm_logger('info', timeframe_zoom,
                            f'Dry/Live-running MoniGoMani with normal timeframe ({self.timeframe} candles)')
            # Just populate indicators.
            dataframe = self._populate_indicators(dataframe, metadata)

        return dataframe

    def _populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame.
        Should be called with 'informative_pair' (1h candles) during backtesting/hyperopting with TimeFrame-Zoom!

        Performance Note: For the best performance be frugal on the number of indicators you are using.
        Let uncomment only the indicator you are using in MoniGoMani or your hyperopt configuration,
        otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for MoniGoMani
        """

        # Momentum Indicators (timeperiod is expressed in candles)
        # -------------------

        # ADX - Average Directional Index (The Trend Strength Indicator)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)  # 14 timeperiods is usually used for ADX

        # +DM (Positive Directional Indicator) = current high - previous high
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        # -DM (Negative Directional Indicator) = previous low - current low
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)

        # RSI - Relative Strength Index (Under bought / Over sold & Over bought / Under sold indicator Indicator)
        dataframe['rsi'] = ta.RSI(dataframe)

        # MACD - Moving Average Convergence Divergence
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']  # MACD - Blue TradingView Line (Bullish if on top)
        dataframe['macdsignal'] = macd['macdsignal']  # Signal - Orange TradingView Line (Bearish if on top)

        # Overlap Studies
        # ---------------

        # SMA's & EMA's are trend following tools (Should not be used when line goes sideways)
        # SMA - Simple Moving Average (Moves slower compared to EMA, price trend over X periods)
        dataframe['sma9'] = ta.SMA(dataframe, timeperiod=9)
        dataframe['sma50'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['sma200'] = ta.SMA(dataframe, timeperiod=200)

        # EMA - Exponential Moving Average (Moves quicker compared to SMA, more weight added)
        # (For traders who trade intra-day and fast-moving markets, the EMA is more applicable)
        dataframe['ema9'] = ta.EMA(dataframe, timeperiod=9)  # timeperiod is expressed in candles
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_upperband'] = bollinger['upper']

        # Volume Indicators
        # -----------------

        # VWAP - Volume Weighted Average Price
        dataframe['vwap'] = qtpylib.vwap(dataframe)

        # Weighted Variables
        # ------------------

        # Initialize weighted buy/sell signal variables if they are needed (should be 0 = false by default)
        if self.debuggable_weighted_signal_dataframe:
            dataframe['adx_strong_up_weighted_buy_signal'] = dataframe['adx_strong_down_weighted_sell_signal'] = 0
            dataframe['bollinger_bands_weighted_buy_signal'] = dataframe['bollinger_bands_weighted_sell_signal'] = 0
            dataframe['ema_long_death_cross_weighted_sell_signal'] = 0
            dataframe['ema_long_golden_cross_weighted_buy_signal'] = 0
            dataframe['ema_short_death_cross_weighted_sell_signal'] = 0
            dataframe['ema_short_golden_cross_weighted_buy_signal'] = 0
            dataframe['macd_weighted_buy_signal'] = dataframe['macd_weighted_sell_signal'] = 0
            dataframe['rsi_weighted_buy_signal'] = dataframe['rsi_weighted_sell_signal'] = 0
            dataframe['sma_long_death_cross_weighted_sell_signal'] = 0
            dataframe['sma_long_golden_cross_weighted_buy_signal'] = 0
            dataframe['sma_short_death_cross_weighted_sell_signal'] = 0
            dataframe['sma_short_golden_cross_weighted_buy_signal'] = 0
            dataframe['vwap_cross_weighted_buy_signal'] = dataframe['vwap_cross_weighted_sell_signal'] = 0

        # Initialize total signal variables (should be 0 = false by default)
        dataframe['total_buy_signal_strength'] = dataframe['total_sell_signal_strength'] = 0

        # Trend Detection
        # ---------------

        # Detect if current trend going Downwards / Sideways / Upwards, strategy will respond accordingly
        dataframe.loc[(dataframe['adx'] > 22) & (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
        dataframe.loc[dataframe['adx'] <= 22, 'trend'] = 'sideways'
        dataframe.loc[(dataframe['adx'] > 22) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """

        # If a Weighted Buy Signal goes off => Bullish Indication, Set to true (=1) and multiply by weight percentage

        if self.debuggable_weighted_signal_dataframe:
            # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'adx_strong_up_weighted_buy_signal'] = \
                self.buy_downwards_trend_adx_strong_up_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'adx_strong_up_weighted_buy_signal'] = \
                self.buy_sideways_trend_adx_strong_up_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'adx_strong_up_weighted_buy_signal'] = \
                self.buy_upwards_trend_adx_strong_up_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['adx_strong_up_weighted_buy_signal']

            # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'bollinger_bands_weighted_buy_signal'] = \
                self.buy_downwards_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'bollinger_bands_weighted_buy_signal'] = \
                self.buy_sideways_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'bollinger_bands_weighted_buy_signal'] = \
                self.buy_upwards_trend_bollinger_bands_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['bollinger_bands_weighted_buy_signal']

            # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_golden_cross_weighted_buy_signal'] = \
                self.buy_downwards_trend_ema_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_golden_cross_weighted_buy_signal'] = \
                self.buy_sideways_trend_ema_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_golden_cross_weighted_buy_signal'] = \
                self.buy_upwards_trend_ema_long_golden_cross_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['ema_long_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_golden_cross_weighted_buy_signal'] = \
                self.buy_downwards_trend_ema_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_golden_cross_weighted_buy_signal'] = \
                self.buy_sideways_trend_ema_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_golden_cross_weighted_buy_signal'] = \
                self.buy_upwards_trend_ema_short_golden_cross_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['ema_short_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: MACD above Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'macd_weighted_buy_signal'] = self.buy_downwards_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] > dataframe['macdsignal']),
                          'macd_weighted_buy_signal'] = self.buy_sideways_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'macd_weighted_buy_signal'] = self.buy_upwards_trend_macd_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['macd_weighted_buy_signal']

            # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'rsi_weighted_buy_signal'] = self.buy_downwards_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'rsi_weighted_buy_signal'] = self.buy_sideways_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'rsi_weighted_buy_signal'] = self.buy_upwards_trend_rsi_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['rsi_weighted_buy_signal']

            # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_golden_cross_weighted_buy_signal'] = \
                self.buy_downwards_trend_sma_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_golden_cross_weighted_buy_signal'] = \
                self.buy_sideways_trend_sma_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_golden_cross_weighted_buy_signal'] = \
                self.buy_upwards_trend_sma_long_golden_cross_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['sma_long_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_golden_cross_weighted_buy_signal'] = \
                self.buy_downwards_trend_sma_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_golden_cross_weighted_buy_signal'] = \
                self.buy_sideways_trend_sma_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_golden_cross_weighted_buy_signal'] = \
                self.buy_upwards_trend_sma_short_golden_cross_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['sma_short_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_buy_signal'] = \
                self.buy_downwards_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_buy_signal'] = \
                self.buy_sideways_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_buy_signal'] = \
                self.buy_upwards_trend_vwap_cross_weight.value / self.precision
            dataframe['total_buy_signal_strength'] += dataframe['vwap_cross_weighted_buy_signal']

        else:
            # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += \
                self.buy_downwards_trend_adx_strong_up_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += \
                self.buy_sideways_trend_adx_strong_up_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += \
                self.buy_upwards_trend_adx_strong_up_weight.value / self.precision

            # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += \
                self.buy_downwards_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += \
                self.buy_sideways_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += \
                self.buy_upwards_trend_bollinger_bands_weight.value / self.precision

            # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += \
                self.buy_downwards_trend_ema_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += \
                self.buy_sideways_trend_ema_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += \
                self.buy_upwards_trend_ema_long_golden_cross_weight.value / self.precision

            # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += \
                self.buy_downwards_trend_ema_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += \
                self.buy_sideways_trend_ema_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += \
                self.buy_upwards_trend_ema_short_golden_cross_weight.value / self.precision

            # Weighted Buy Signal: MACD above Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += self.buy_downwards_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += self.buy_sideways_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += self.buy_upwards_trend_macd_weight.value / self.precision

            # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += self.buy_downwards_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += self.buy_sideways_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += self.buy_upwards_trend_rsi_weight.value / self.precision

            # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += \
                self.buy_downwards_trend_sma_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += \
                self.buy_sideways_trend_sma_long_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += \
                self.buy_upwards_trend_sma_long_golden_cross_weight.value / self.precision

            # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += \
                self.buy_downwards_trend_sma_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += \
                self.buy_sideways_trend_sma_short_golden_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += \
                self.buy_upwards_trend_sma_short_golden_cross_weight.value / self.precision

            # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += \
                self.buy_downwards_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += \
                self.buy_sideways_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += \
                self.buy_upwards_trend_vwap_cross_weight.value / self.precision

        # Check if buy signal should be sent depending on the current trend, using a lookback window to take signals
        # that fired during previous candles into consideration
        if (self.is_dry_live_run_detected is False) and (self.informative_timeframe != self.backtest_timeframe):
            # If TimeFrame-Zooming => Only use 'informative_timeframe' data
            dataframe.loc[
                (
                        (dataframe['trend'] == 'downwards') &
                        ((dataframe['total_buy_signal_strength']
                          .rolling(self.buy__downwards_trend_total_signal_needed_candles_lookback_window.value *
                                   self.timeframe_multiplier).sum() / self.timeframe_multiplier)
                         >= self.buy__downwards_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'sideways') &
                        ((dataframe['total_buy_signal_strength']
                          .rolling(self.buy__sideways_trend_total_signal_needed_candles_lookback_window.value *
                                   self.timeframe_multiplier).sum() / self.timeframe_multiplier)
                         >= self.buy__sideways_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'upwards') &
                        ((dataframe['total_buy_signal_strength']
                          .rolling(self.buy__upwards_trend_total_signal_needed_candles_lookback_window.value *
                                   self.timeframe_multiplier).sum() / self.timeframe_multiplier)
                         >= self.buy__upwards_trend_total_signal_needed.value / self.precision)
                ), 'buy'] = 1
        else:
            dataframe.loc[
                (
                        (dataframe['trend'] == 'downwards') &
                        (dataframe['total_buy_signal_strength']
                         .rolling(self.buy__downwards_trend_total_signal_needed_candles_lookback_window.value).sum()
                         >= self.buy__downwards_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'sideways') &
                        (dataframe['total_buy_signal_strength']
                         .rolling(self.buy__sideways_trend_total_signal_needed_candles_lookback_window.value).sum()
                         >= self.buy__sideways_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'upwards') &
                        (dataframe['total_buy_signal_strength']
                         .rolling(self.buy__upwards_trend_total_signal_needed_candles_lookback_window.value).sum()
                         >= self.buy__upwards_trend_total_signal_needed.value / self.precision)
                ), 'buy'] = 1

        # Override Buy Signal: When configured buy signals can be completely turned off for each kind of trend
        if not self.buy___trades_when_downwards.value / self.precision:
            dataframe.loc[dataframe['trend'] == 'downwards', 'buy'] = 0
        if not self.buy___trades_when_sideways.value / self.precision:
            dataframe.loc[dataframe['trend'] == 'sideways', 'buy'] = 0
        if not self.buy___trades_when_upwards.value / self.precision:
            dataframe.loc[dataframe['trend'] == 'upwards', 'buy'] = 0

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """

        # If a Weighted Sell Signal goes off => Bearish Indication, Set to true (=1) and multiply by weight percentage

        if self.debuggable_weighted_signal_dataframe:
            # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'adx_strong_down_weighted_sell_signal'] = \
                self.sell_downwards_trend_adx_strong_down_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'adx_strong_down_weighted_sell_signal'] = \
                self.sell_sideways_trend_adx_strong_down_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'adx_strong_down_weighted_sell_signal'] = \
                self.sell_upwards_trend_adx_strong_down_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['adx_strong_down_weighted_sell_signal']

            # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'bollinger_bands_weighted_sell_signal'] = \
                self.sell_downwards_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'bollinger_bands_weighted_sell_signal'] = \
                self.sell_sideways_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'bollinger_bands_weighted_sell_signal'] = \
                self.sell_upwards_trend_bollinger_bands_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['bollinger_bands_weighted_sell_signal']

            # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_death_cross_weighted_sell_signal'] = \
                self.sell_downwards_trend_ema_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_death_cross_weighted_sell_signal'] = \
                self.sell_sideways_trend_ema_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_death_cross_weighted_sell_signal'] = \
                self.sell_upwards_trend_ema_long_death_cross_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['ema_long_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_death_cross_weighted_sell_signal'] = \
                self.sell_downwards_trend_ema_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_death_cross_weighted_sell_signal'] = \
                self.sell_sideways_trend_ema_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_death_cross_weighted_sell_signal'] = \
                self.sell_upwards_trend_ema_short_death_cross_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['ema_short_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: MACD below Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'macd_weighted_sell_signal'] = self.sell_downwards_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] < dataframe['macdsignal']),
                          'macd_weighted_sell_signal'] = self.sell_sideways_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'macd_weighted_sell_signal'] = self.sell_upwards_trend_macd_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['macd_weighted_sell_signal']

            # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'rsi_weighted_sell_signal'] = self.sell_downwards_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'rsi_weighted_sell_signal'] = self.sell_sideways_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'rsi_weighted_sell_signal'] = self.sell_upwards_trend_rsi_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['rsi_weighted_sell_signal']

            # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_death_cross_weighted_sell_signal'] = \
                self.sell_downwards_trend_sma_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_death_cross_weighted_sell_signal'] = \
                self.sell_sideways_trend_sma_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_death_cross_weighted_sell_signal'] = \
                self.sell_upwards_trend_sma_long_death_cross_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['sma_long_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_death_cross_weighted_sell_signal'] = \
                self.sell_downwards_trend_sma_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_death_cross_weighted_sell_signal'] = \
                self.sell_sideways_trend_sma_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_death_cross_weighted_sell_signal'] = \
                self.sell_upwards_trend_sma_short_death_cross_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['sma_short_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: VWAP crosses below current price
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_sell_signal'] = \
                self.sell_downwards_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_sell_signal'] = \
                self.sell_sideways_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_sell_signal'] = \
                self.sell_upwards_trend_vwap_cross_weight.value / self.precision
            dataframe['total_sell_signal_strength'] += dataframe['vwap_cross_weighted_sell_signal']

        else:
            # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += \
                self.sell_downwards_trend_adx_strong_down_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += \
                self.sell_sideways_trend_adx_strong_down_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += \
                self.sell_upwards_trend_adx_strong_down_weight.value / self.precision

            # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                self.sell_downwards_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                self.sell_sideways_trend_bollinger_bands_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                self.sell_upwards_trend_bollinger_bands_weight.value / self.precision

            # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += \
                self.sell_downwards_trend_ema_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += \
                self.sell_sideways_trend_ema_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += \
                self.sell_upwards_trend_ema_long_death_cross_weight.value / self.precision

            # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += \
                self.sell_downwards_trend_ema_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += \
                self.sell_sideways_trend_ema_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += \
                self.sell_upwards_trend_ema_short_death_cross_weight.value / self.precision

            # Weighted Sell Signal: MACD below Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += self.sell_downwards_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += self.sell_sideways_trend_macd_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += self.sell_upwards_trend_macd_weight.value / self.precision

            # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += self.sell_downwards_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += self.sell_sideways_trend_rsi_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += self.sell_upwards_trend_rsi_weight.value / self.precision

            # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += \
                self.sell_downwards_trend_sma_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += \
                self.sell_sideways_trend_sma_long_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += \
                self.sell_upwards_trend_sma_long_death_cross_weight.value / self.precision

            # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += \
                self.sell_downwards_trend_sma_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += \
                self.sell_sideways_trend_sma_short_death_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += \
                self.sell_upwards_trend_sma_short_death_cross_weight.value / self.precision

            # Weighted Sell Signal: VWAP crosses below current price
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += \
                self.sell_downwards_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += \
                self.sell_sideways_trend_vwap_cross_weight.value / self.precision
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += \
                self.sell_upwards_trend_vwap_cross_weight.value / self.precision

        # Check if buy signal should be sent depending on the current trend, using a lookback window to take signals
        # that fired during previous candles into consideration
        if (self.is_dry_live_run_detected is False) and (self.informative_timeframe != self.backtest_timeframe):
            # If TimeFrame-Zooming => Only use 'informative_timeframe' data
            dataframe.loc[
                (
                        (dataframe['trend'] == 'downwards') &
                        ((dataframe['total_sell_signal_strength']
                          .rolling(self.sell__downwards_trend_total_signal_needed_candles_lookback_window.value *
                                   self.timeframe_multiplier).sum() / self.timeframe_multiplier)
                         >= self.sell__downwards_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'sideways') &
                        ((dataframe['total_sell_signal_strength']
                          .rolling(self.sell__sideways_trend_total_signal_needed_candles_lookback_window.value *
                                   self.timeframe_multiplier).sum() / self.timeframe_multiplier)
                         >= self.sell__sideways_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'upwards') &
                        ((dataframe['total_sell_signal_strength']
                          .rolling(self.sell__upwards_trend_total_signal_needed_candles_lookback_window.value *
                                   self.timeframe_multiplier).sum() / self.timeframe_multiplier)
                         >= self.sell__upwards_trend_total_signal_needed.value / self.precision)
                ), 'sell'] = 1
        else:
            dataframe.loc[
                (
                        (dataframe['trend'] == 'downwards') &
                        (dataframe['total_sell_signal_strength']
                         .rolling(self.sell__downwards_trend_total_signal_needed_candles_lookback_window.value).sum()
                         >= self.sell__downwards_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'sideways') &
                        (dataframe['total_sell_signal_strength']
                         .rolling(self.sell__sideways_trend_total_signal_needed_candles_lookback_window.value).sum()
                         >= self.sell__sideways_trend_total_signal_needed.value / self.precision)
                ) | (
                        (dataframe['trend'] == 'upwards') &
                        (dataframe['total_sell_signal_strength']
                         .rolling(self.sell__upwards_trend_total_signal_needed_candles_lookback_window.value).sum()
                         >= self.sell__upwards_trend_total_signal_needed.value / self.precision)
                ), 'sell'] = 1

        # Override Sell Signal: When configured sell signals can be completely turned off for each kind of trend
        if not self.sell___trades_when_downwards.value / self.precision:
            dataframe.loc[dataframe['trend'] == 'downwards', 'sell'] = 0
        if not self.sell___trades_when_sideways.value / self.precision:
            dataframe.loc[dataframe['trend'] == 'sideways', 'sell'] = 0
        if not self.sell___trades_when_upwards.value / self.precision:
            dataframe.loc[dataframe['trend'] == 'upwards', 'sell'] = 0

        return dataframe

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        """
        Open Trade Custom Information Storage & Garbage Collector
        ---------------------------------------------------------
        MoniGoMani (currently) only uses this function to store custom information from all open_trades at that given
        moment during BackTesting/HyperOpting or Dry/Live-Running
        Further it also does garbage collection to make sure no old closed trade data remains in custom_info

        The actual normal "custom_stoploss" usage for which this function is generally used isn't used by MGM (yet)!
        This custom_stoploss function should be able to work in tandem with Trailing stoploss!

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in ask_strategy.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return float: New stoploss value, relative to the current-rate
        """

        custom_information_storage = 'custom_stoploss - Custom Information Storage'
        garbage_collector = custom_information_storage + ' Garbage Collector'

        # Open Trade Custom Information Storage
        # -------------------------------------
        self.mgm_logger('debug', custom_information_storage, f'Fetching all currently open trades')

        # Fetch all open trade data during Dry & Live Running
        if self.is_dry_live_run_detected is True:
            self.mgm_logger('debug', custom_information_storage,
                            f'Fetching all currently open trades during Dry/Live Run')

            all_open_trades = Trade.get_trades([Trade.is_open.is_(True)]).order_by(Trade.open_date).all()
        # Fetch all open trade data during Back Testing & Hyper Opting
        else:
            self.mgm_logger('debug', custom_information_storage,
                            f'Fetching all currently open trades during BackTesting/HyperOpting')
            all_open_trades = trade.trades_open

        self.mgm_logger('debug', custom_information_storage,
                        f'Up-to-date open trades ({str(len(all_open_trades))}) fetched!')
        self.mgm_logger('debug', custom_information_storage,
                        f'all_open_trades contents: {repr(all_open_trades)}')

        # Store current pair's open_trade + it's current profit in custom_info
        for open_trade in all_open_trades:
            if str(open_trade.pair) == str(pair):
                if str(open_trade.pair) not in self.custom_info['open_trades']:
                    self.custom_info['open_trades'][str(open_trade.pair)] = {}
                self.custom_info['open_trades'][str(open_trade.pair)]['trade'] = str(open_trade)
                self.custom_info['open_trades'][str(open_trade.pair)]['current_profit'] = current_profit
                self.mgm_logger('info', custom_information_storage,
                                f'Storing trade + current profit/loss for pair ({str(pair)}) '
                                f'in custom_info')
                break

        # Custom Information Storage Garbage Collector
        # --------------------------------------------
        # Check if any old open_trade garbage needs to be removed
        if len(all_open_trades) < len(self.custom_info['open_trades']):
            garbage_trade_amount = len(self.custom_info['open_trades']) - len(all_open_trades)
            self.mgm_logger('info', garbage_collector, f'Old open trade garbage detected for '
                                                       f'{str(garbage_trade_amount)} trades, starting cleanup')

            for garbage_trade in range(garbage_trade_amount):
                for stored_trade in self.custom_info['open_trades']:
                    pair_still_open = False
                    for open_trade in all_open_trades:
                        if str(stored_trade) == str(open_trade.pair):
                            self.mgm_logger('debug', garbage_collector,
                                            f'Open trade found, no action needed for pair ({stored_trade}) '
                                            f'in custom_info')
                            pair_still_open = True
                            break

                    # Remove old open_trade garbage
                    if not pair_still_open:
                        self.mgm_logger('info', garbage_collector,
                                        f'No open trade found for pair ({stored_trade}), removing '
                                        f'from custom_info')
                        self.custom_info['open_trades'].pop(stored_trade)
                        self.mgm_logger('debug', garbage_collector,
                                        f'Successfully removed garbage_trade {str(garbage_trade)} '
                                        f'from custom_info!')
                        break

        # Print all stored open trade info in custom_storage
        self.mgm_logger('debug', custom_information_storage,
                        f'Open trades ({str(len(self.custom_info["open_trades"]))}) in custom_info updated '
                        f'successfully!')
        self.mgm_logger('debug', custom_information_storage,
                        f'custom_info["open_trades"] contents: {repr(self.custom_info["open_trades"])}')

        # Always return a value bigger than the initial stoploss to keep using the initial stoploss.
        # Since we (currently) only want to use this function for custom information storage!
        return -1

    def custom_sell(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        """
        Open Trade Unclogger:
        ---------------------
        Override Sell Signal: When enabled attempts to unclog the bot when it's stuck with losing trades & unable to
        trade more new trades.

        It will only unclog a losing trade when all of following checks have been full-filled:
        => Check if everything in custom_storage is up to date with all_open_trades
        => Check if there are enough losing trades open for unclogging to occur
        => Check if there is a losing trade open for the pair currently being ran through the MoniGoMani loop
        => Check if trade has been open for X minutes (long enough to give it a recovery chance)
        => Check if total open trades losing % is met
        => Check if open_trade's trend changed negatively during past X candles

        Please configurable/hyperoptable in the sell_params dictionary under the hyperopt results copy/paste section.
        Only used when sell_params['sell___unclogger_enabled'] is set to True.

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in ask_strategy.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return float: New stoploss value, relative to the current-rate
        """

        open_trade_unclogger = 'Open Trade Unclogger'
        custom_information_storage = 'custom_sell - Custom Information Storage'

        if self.sell___unclogger_enabled.value:
            try:
                # Open Trade Custom Information Storage
                # -------------------------------------
                # Fetch all open trade data during Dry & Live Running
                if self.is_dry_live_run_detected is True:
                    self.mgm_logger('debug', custom_information_storage,
                                    f'Fetching all currently open trades during Dry/Live Run')

                    all_open_trades = Trade.get_trades([Trade.is_open.is_(True)]).order_by(Trade.open_date).all()
                # Fetch all open trade data during Back Testing & Hyper Opting
                else:
                    self.mgm_logger('debug', custom_information_storage,
                                    f'Fetching all currently open trades during BackTesting/HyperOpting')
                    all_open_trades = trade.trades_open

                self.mgm_logger('debug', custom_information_storage,
                                f'Up-to-date open trades ({str(len(all_open_trades))}) fetched!')
                self.mgm_logger('debug', custom_information_storage,
                                f'all_open_trades contents: {repr(all_open_trades)}')

                # Check if everything in custom_storage is up to date with all_open_trades
                if len(all_open_trades) > len(self.custom_info['open_trades']):
                    self.mgm_logger('warning', custom_information_storage,
                                    f'Open trades ({str(len(self.custom_info["open_trades"]))}) in custom_storage do '
                                    f'not match yet with trades in live open trades ({str(len(all_open_trades))}) '
                                    f'aborting unclogger for now!')
                else:
                    # Open Trade Unclogger
                    # --------------------
                    self.mgm_logger('debug', open_trade_unclogger,
                                    f'Running trough all checks to see if unclogging is needed')

                    # Check if there are enough losing trades open for unclogging to occur
                    self.mgm_logger('debug', open_trade_unclogger,
                                    f'Fetching all currently losing_open_trades from custom information storage')
                    losing_open_trades = {}
                    for stored_trade in self.custom_info['open_trades']:
                        stored_current_profit = self.custom_info['open_trades'][stored_trade]['current_profit']
                        if stored_current_profit < 0:
                            if not str(pair) in losing_open_trades:
                                losing_open_trades[str(stored_trade)] = {}
                            losing_open_trades[str(stored_trade)] = stored_current_profit
                    self.mgm_logger('debug', open_trade_unclogger,
                                    f'Fetched losing_open_trades ({str(len(losing_open_trades))}) from custom '
                                    f'information storage!')

                    if len(losing_open_trades) < (self.sell___unclogger_minimal_losing_trades_open.value / self.precision):
                        self.mgm_logger('debug', open_trade_unclogger,
                                        f'No unclogging needed! Not enough losing trades currently open!')
                    else:
                        self.mgm_logger('debug', open_trade_unclogger,
                                        f'Enough losing trades detected! Proceeding to the next check!')

                        # Check if there is a losing trade open for the pair currently being ran through the MoniGoMani
                        if pair not in losing_open_trades:
                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'No unclogging needed! Currently checked pair ({pair}) is not making a '
                                            f'loss at this point in time!')
                        else:
                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'Currently checked pair ({pair}) is losing! Proceeding to the next check!')

                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'Trade open time: {str(trade.open_date_utc.replace(tzinfo=None))}')

                            minimal_open_time = current_time.replace(tzinfo=None) - timedelta(minutes=round(
                                self.sell___unclogger_minimal_losing_trade_duration_minutes.value / self.precision))

                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'Minimal open time: {str(minimal_open_time)}')

                            if trade.open_date_utc.replace(tzinfo=None) > minimal_open_time:
                                self.mgm_logger('debug', open_trade_unclogger,
                                                f'No unclogging needed! Currently checked pair ({pair}) has not been '
                                                f'open been open for long enough!')
                            else:
                                self.mgm_logger('debug', open_trade_unclogger,
                                                f'Trade has been open for long enough! Proceeding to the next check!')

                                # Check if total open trades losing % is met
                                percentage_open_trades_losing = \
                                    int((len(losing_open_trades) / len(all_open_trades)) * 100)
                                self.mgm_logger('debug', open_trade_unclogger,
                                                f'percentage_open_trades_losing: {str(percentage_open_trades_losing)}%')
                                if percentage_open_trades_losing < \
                                        round(self.sell___unclogger_open_trades_losing_percentage_needed.value /
                                              self.precision):
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'No unclogging needed! Percentage of open trades losing needed '
                                                    f'has not been satisfied!')
                                else:
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'Percentage of open trades losing needed has been satisfied! '
                                                    f'Proceeding to the next check!')

                                    # Fetch current dataframe for the pair currently being ran through MoniGoMani
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'Fetching currently needed "trend" dataframe data to check how '
                                                    f'pair ({pair}) has been doing in during the last '
                                                    f'{str(self.sell___unclogger_trend_lookback_candles_window.value / self.precision)}'
                                                    f' candles')

                                    # Fetch all needed 'trend' trade data
                                    stored_trend_dataframe = {}
                                    dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)

                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'Fetching all needed "trend" trade data')

                                    for candle in range(1, round(self.sell___unclogger_trend_lookback_candles_window.value / self.precision) + 1):
                                        # Convert the candle time to the one being used by the
                                        # 'informative_timeframe'
                                        candle_multiplier = int(self.informative_timeframe.rstrip("mhdwM"))
                                        candle_time = \
                                            timeframe_to_prev_date(self.informative_timeframe, current_time) - \
                                            timedelta(minutes=int(candle * candle_multiplier))
                                        if self.informative_timeframe.find('h') != -1:
                                            candle_time = \
                                                timeframe_to_prev_date(self.informative_timeframe, current_time) - \
                                                timedelta(hours=int(candle * candle_multiplier))
                                        elif self.informative_timeframe.find('d') != -1:
                                            candle_time =\
                                                timeframe_to_prev_date(self.informative_timeframe, current_time) - \
                                                timedelta(days=int(candle * candle_multiplier))
                                        elif self.informative_timeframe.find('w') != -1:
                                            candle_time = \
                                                timeframe_to_prev_date(self.informative_timeframe, current_time) - \
                                                timedelta(weeks=int(candle * candle_multiplier))
                                        elif self.informative_timeframe.find('M') != -1:
                                            candle_time = \
                                                timeframe_to_prev_date(self.informative_timeframe, current_time) - \
                                                timedelta64(int(1 * candle_multiplier), 'M')

                                        candle_trend = \
                                            dataframe.loc[dataframe['date'] == candle_time].squeeze()['trend']

                                        if isinstance(candle_trend, str):
                                            stored_trend_dataframe[candle] = candle_trend
                                        else:
                                            break

                                    # Check if enough trend data has been stored to do the next check
                                    if len(stored_trend_dataframe) < \
                                            round(self.sell___unclogger_trend_lookback_candles_window.value /
                                                  self.precision):
                                        self.mgm_logger('debug', open_trade_unclogger,
                                                        f'No unclogging needed! Not enough trend data stored yet!')
                                    else:

                                        # Print all fetched 'trend' trade data
                                        self.mgm_logger('debug', open_trade_unclogger,
                                                        f'All needed "trend" trade data '
                                                        f'({str(len(stored_trend_dataframe))}) fetched!')
                                        self.mgm_logger('debug', open_trade_unclogger,
                                                        f'stored_trend_dataframe contents: '
                                                        f'{repr(stored_trend_dataframe)}')

                                        # Check if open_trade's trend changed negatively during past X candles
                                        self.mgm_logger('debug', open_trade_unclogger,
                                                        f'Calculating amount of unclogger_trend_lookback_candles_window'
                                                        f' "satisfied" for pair: {pair}')
                                        unclogger_candles_satisfied = 0
                                        for lookback_candle \
                                                in range(1,
                                                         round(self.sell___unclogger_trend_lookback_candles_window.value
                                                               / self.precision) + 1):
                                            if self.sell___unclogger_trend_lookback_window_uses_downwards_candles.value \
                                                    & (stored_trend_dataframe[lookback_candle] == 'downwards'):
                                                unclogger_candles_satisfied += 1
                                            if self.sell___unclogger_trend_lookback_window_uses_sideways_candles.value \
                                                    & (stored_trend_dataframe[lookback_candle] == 'sideways'):
                                                unclogger_candles_satisfied += 1
                                            if self.sell___unclogger_trend_lookback_window_uses_upwards_candles.value \
                                                    & (stored_trend_dataframe[lookback_candle] == 'upwards'):
                                                unclogger_candles_satisfied += 1
                                        self.mgm_logger('debug', open_trade_unclogger,
                                                        f'Amount of unclogger_trend_lookback_candles_window '
                                                        f'"satisfied": {str(unclogger_candles_satisfied)} '
                                                        f'for pair: {pair}')

                                        # Calculate the percentage of the lookback window currently satisfied
                                        unclogger_candles_percentage_satisfied = \
                                            (unclogger_candles_satisfied /
                                             round(self.sell___unclogger_trend_lookback_candles_window.value /
                                                   self.precision)) * 100

                                        # Override Sell Signal: Unclog trade by forcing a sell & attempt to continue
                                        # the profit climb with the "freed up trading slot"
                                        if unclogger_candles_percentage_satisfied >= \
                                                round(
                                                    self.sell___unclogger_trend_lookback_candles_window_percentage_needed.value
                                                    / self.precision):
                                            self.mgm_logger('info', open_trade_unclogger, f'Unclogging losing trade...')
                                            return "MGM_unclogging_losing_trade"
                                        else:
                                            self.mgm_logger('info', open_trade_unclogger,
                                                            f'No need to unclog open trade...')

            except Exception as e:
                self.mgm_logger('error', open_trade_unclogger,
                                f'Following error has occurred in the Open Trade Unclogger:')
                self.mgm_logger('error', open_trade_unclogger, str(e))

        return None  # By default we don't want a force sell to occur

    def mgm_logger(self, message_type: str, code_section: str, message: str):
        """
        MoniGoMani Logger:
        ---------------------
        When passing a type and a message to this function it will log:
        - The timestamp of logging + the message_type provided + the message provided
        - To the console & To "./user_data/logs/freqtrade.log"
    
        :param message_type: The type of the message (INFO, DEBUG, WARNING, ERROR)
        :param code_section: The section in the code where the message occurred
        :param message: The log message to be displayed
        """

        if self.use_mgm_logging:
            if (self.mgm_log_levels_enabled['info'] is True) and (message_type.upper() == 'INFO'):
                logger.setLevel(logging.INFO)
                logger.info(code_section + ' - ' + message)
            elif (self.mgm_log_levels_enabled['debug'] is True) and (message_type.upper() == 'DEBUG'):
                logger.setLevel(logging.DEBUG)
                logger.debug(code_section + ' - ' + message)
            elif (self.mgm_log_levels_enabled['warning'] is True) and (message_type.upper() == 'WARNING'):
                logger.setLevel(logging.WARNING)
                logger.warning(code_section + ' - ' + message)
            elif (self.mgm_log_levels_enabled['error'] is True) and (message_type.upper() == 'ERROR'):
                logger.setLevel(logging.ERROR)
                logger.error(code_section + ' - ' + message)
