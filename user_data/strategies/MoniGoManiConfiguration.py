# --- Do not remove these libs ----------------------------------------------------------------------
from MoniGoManiHyperStrategy import MoniGoManiHyperStrategy as MGMStrategy
from freqtrade.strategy \
    import CategoricalParameter, IntParameter
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))


def init_vars(parameter_dictionary: dict, parameter_name: str, parameter_min_value: int, parameter_max_value: int,
              parameter_threshold: int, precision: float, overrideable: bool = True):
    """
    Function to automatically initialize MoniGoMani's HyperOptable parameter values for both HyperOpt Runs.

    :param parameter_dictionary: Buy or Sell params dictionary
    :param parameter_name: Name of the signal in the dictionary
    :param parameter_min_value: Minimal search space value to use during the 1st HyperOpt Run
    :param parameter_max_value: Maximum search space value to use during the 1st HyperOpt Run
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


class MoniGoManiConfiguration(MGMStrategy):
    """
    MoniGoManiConfiguration is a Child Strategy which requires import of it's Parent Strategy, MoniGoManiHyperStrategy.
    It separates most code from settings, and automates the refining of the search spaces and setting up of overrides in
    between HyperOpt Runs.
    """

    ####################################################################################################################
    #                                          START MONIGOMANI SETTINGS SECTION                                       #
    ####################################################################################################################
    timeframe = '1h'
    backtest_timeframe = '5m'
    precision = 1

    # Default Minimal/Maximum search space values for signals:
    min_weighted_signal_value = 0
    max_weighted_signal_value = 100
    min_trend_total_signal_needed_value = 30
    min_trend_total_signal_needed_candles_lookback_window_value = 1
    max_trend_total_signal_needed_candles_lookback_window_value = 6

    # Search space thresholds, for detecting overrides and refining search spaces during the 2nd HyperOpt Run
    search_threshold_weighted_signal_values = 10
    search_threshold_trend_total_signal_needed_candles_lookback_window_value = 1

    # Number of weighted signals:
    # Fill in the total number of different weighted signals in use in the weighted tables
    # 'buy/sell__downwards/sideways/upwards_trend_total_signal_needed' settings will be multiplied with this value
    # so their search spaces will be larger, resulting in more equally divided weighted signal scores when hyperopting
    number_of_weighted_signals = 9

    # ROI Table StepSize:
    # Size of the steps in minutes to be used when calculating the long continuous ROI table
    # MGM generates a custom really long table so it will have less gaps in it and be more continuous in it's decrease
    roi_table_step_size = 5

    ####################################################################################################################
    #                                           END MONIGOMANI SETTINGS SECTION                                        #
    ####################################################################################################################

    # Initialize empty buy/sell_params dictionaries
    buy_params = {}
    sell_params = {}

    ####################################################################################################################
    #                              START OF 1ST RUN HYPEROPT RESULTS COPY-PASTE SECTION                                #
    ####################################################################################################################

    # Paste 1st Run HyperOpt Results here...

    ####################################################################################################################
    #                                END OF 1ST RUN HYPEROPT RESULTS COPY-PASTE SECTION                                #
    ####################################################################################################################

    # Initialize the buy/sell_param_final dictionaries with results from the 1st HyperOpt Run
    buy_param_final = buy_params
    sell_param_final = sell_params

    ####################################################################################################################
    #                         START OF 2ND (OR MORE) RUN HYPEROPT RESULTS COPY-PASTE SECTION                           #
    ####################################################################################################################

    ####################################################################################################################
    #                          END OF 2ND (OR MORE) RUN HYPEROPT RESULTS COPY-PASTE SECTION                            #
    ####################################################################################################################

    # Update buy/sell_param_final dictionaries with 2nd HyperOpt Run Results
    buy_param_final.update(buy_params)
    sell_param_final.update(sell_params)
    buy_params = buy_param_final
    sell_params = sell_param_final

    ####################################################################################################################
    #                                 START OF HYPEROPT PARAMETERS CONFIGURATION SECTION                               #
    ####################################################################################################################

    # HyperOpt Settings Override
    # --------------------------
    # When the Parameters in below HyperOpt Space Parameters sections are altered as following examples then they can be
    # used as overrides while hyperopting / backtesting / dry/live-running (only truly useful when hyperopting though!)
    # Meaning you can use this to set individual buy_params/sell_params to a fixed value when hyperopting!
    # WARNING: Always double check that when doing a fresh hyperopt or doing a dry/live-run that all overrides are
    # turned off!
    #
    # Override Examples:
    # Override to False:    CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
    # Override to 0:        IntParameter(0, int(100*precision), default=0, space='sell', optimize=False, load=False)
    #
    # default=           The value used when overriding
    # optimize=False     Exclude from hyperopting (Make static)
    # load=False         Don't load from above HYPEROPT RESULTS COPY-PASTE SECTION

    # ---------------------------------------------------------------- #
    #                  Buy HyperOpt Space Parameters                   #
    # ---------------------------------------------------------------- #

    # Trend Detecting Buy Signal Weight Influence Tables
    # -------------------------------------------------------
    # The idea is to let hyperopt find out which signals are more important over other signals by allocating weights to
    # them while also finding the "perfect" weight division between each-other.
    # These Signal Weight Influence Tables will be allocated to signals when their respective trend is detected
    # (Signals can be turned off by allocating 0 or turned into an override by setting them equal to or higher then
    # total_buy_signal_needed)

    # React to Buy Signals when certain trends are detected (False would disable trading in said trend)
    buy___trades_when_downwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)
    buy___trades_when_sideways = \
        CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
    buy___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)

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

    # Trend Detecting Buy Signal Weight Influence Tables
    # -------------------------------------------------------
    # The idea is to let hyperopt find out which signals are more important over other signals by allocating weights to
    # them while also finding the "perfect" weight division between each-other.
    # These Signal Weight Influence Tables will be allocated to signals when their respective trend is detected
    # (Signals can be turned off by allocating 0 or turned into an override by setting them equal to or higher then
    # total_buy_signal_needed)

    # React to Sell Signals when certain trends are detected (False would disable trading in said trend)
    sell___trades_when_downwards = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___trades_when_sideways = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)
    sell___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)

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
