# --- Do not remove these libs ----------------------------------------------------------------------
import freqtrade.vendor.qtpylib.indicators as qtpylib
import logging
import numpy as np  # noqa
import pandas as pd  # noqa
import talib.abstract as ta
from datetime import datetime, timedelta
from freqtrade.persistence import Trade
from freqtrade.strategy \
    import IStrategy, CategoricalParameter, IntParameter, RealParameter, merge_informative_pair, timeframe_to_minutes
from numpy import timedelta64
from pandas import DataFrame

logger = logging.getLogger(__name__)


# ^ TA-Lib Autofill mostly broken in JetBrains Products,
# ta._ta_lib.<function_name> can temporarily be used while writing as a workaround
# Then change back to ta.<function_name> so IDE won't nag about accessing a protected member of TA-Lib
# ----------------------------------------------------------------------------------------------------


class MoniGoManiHyperStrategy(IStrategy):
    """
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.9.1 by Rikj000                         ###
    ##                          ----------------------------                          ##
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

    # If enabled all Weighted Signal results will be added to the dataframe for easy debugging with BreakPoints
    # Warning: Disable this for anything else then debugging in an IDE! (Integrated Development Environment)
    debuggable_weighted_signal_dataframe = False

    # If enabled MoniGoMani logging will be displayed to the console and be integrated in Freqtrades native logging
    # For live it's recommended to disable at least info/debug logging, to keep MGM as lightweight as possible!
    use_mgm_logging = False
    mgm_log_levels_enabled = {
        'info': True,
        'warning': True,
        'error': True,
        'debug': True
        # ^ Debug is very verbose! Always set it to False when BackTesting/HyperOpting!
        # (Only recommended to be True in an IDE with Breakpoints enabled or when you suspect a bug in the code)
    }

    # If enabled MoniGoMani's custom stoploss function will be used (Needed for the new unclogger)
    use_custom_stoploss = True

    # Ps: Documentation has been moved to the Buy/Sell HyperOpt Space Parameters sections below this copy-paste section
    ####################################################################################################################
    #                                    START OF HYPEROPT RESULTS COPY-PASTE SECTION                                  #
    ####################################################################################################################

    # Buy hyperspace params:
    buy_params = {
        'buy___trades_when_downwards': True,
        'buy___trades_when_sideways': False,
        'buy___trades_when_upwards': True,
        'buy__downwards_trend_total_signal_needed': 0,
        'buy__sideways_trend_total_signal_needed': 3,
        'buy__upwards_trend_total_signal_needed': 12,
        'buy_downwards_trend_adx_strong_up_weight': 73,
        'buy_downwards_trend_bollinger_bands_weight': 21,
        'buy_downwards_trend_ema_long_golden_cross_weight': 40,
        'buy_downwards_trend_ema_short_golden_cross_weight': 59,
        'buy_downwards_trend_macd_weight': 52,
        'buy_downwards_trend_rsi_weight': 0,
        'buy_downwards_trend_sma_long_golden_cross_weight': 27,
        'buy_downwards_trend_sma_short_golden_cross_weight': 53,
        'buy_downwards_trend_vwap_cross_weight': 0,
        'buy_sideways_trend_adx_strong_up_weight': 51,
        'buy_sideways_trend_bollinger_bands_weight': 53,
        'buy_sideways_trend_ema_long_golden_cross_weight': 19,
        'buy_sideways_trend_ema_short_golden_cross_weight': 85,
        'buy_sideways_trend_macd_weight': 41,
        'buy_sideways_trend_rsi_weight': 81,
        'buy_sideways_trend_sma_long_golden_cross_weight': 79,
        'buy_sideways_trend_sma_short_golden_cross_weight': 31,
        'buy_sideways_trend_vwap_cross_weight': 16,
        'buy_upwards_trend_adx_strong_up_weight': 59,
        'buy_upwards_trend_bollinger_bands_weight': 83,
        'buy_upwards_trend_ema_long_golden_cross_weight': 100,
        'buy_upwards_trend_ema_short_golden_cross_weight': 77,
        'buy_upwards_trend_macd_weight': 100,
        'buy_upwards_trend_rsi_weight': 82,
        'buy_upwards_trend_sma_long_golden_cross_weight': 100,
        'buy_upwards_trend_sma_short_golden_cross_weight': 66,
        'buy_upwards_trend_vwap_cross_weight': 100
    }

    # Sell hyperspace params:
    sell_params = {
        'sell___trades_when_downwards': True,
        'sell___trades_when_sideways': False,
        'sell___trades_when_upwards': True,
        'sell___unclogger_enabled': True,
        'sell___unclogger_minimal_losing_trade_duration_minutes': 31,
        'sell___unclogger_minimal_losing_trades_open': 1,
        'sell___unclogger_open_trades_losing_percentage_needed': 21,
        'sell___unclogger_trend_lookback_candles_window': 50,
        'sell___unclogger_trend_lookback_candles_window_percentage_needed': 14,
        'sell___unclogger_trend_lookback_window_uses_downwards_candles': True,
        'sell___unclogger_trend_lookback_window_uses_sideways_candles': True,
        'sell___unclogger_trend_lookback_window_uses_upwards_candles': False,
        'sell__downwards_trend_total_signal_needed': 82,
        'sell__sideways_trend_total_signal_needed': 37,
        'sell__upwards_trend_total_signal_needed': 105,
        'sell_downwards_trend_adx_strong_down_weight': 1,
        'sell_downwards_trend_bollinger_bands_weight': 69,
        'sell_downwards_trend_ema_long_death_cross_weight': 61,
        'sell_downwards_trend_ema_short_death_cross_weight': 82,
        'sell_downwards_trend_macd_weight': 8,
        'sell_downwards_trend_rsi_weight': 27,
        'sell_downwards_trend_sma_long_death_cross_weight': 87,
        'sell_downwards_trend_sma_short_death_cross_weight': 31,
        'sell_downwards_trend_vwap_cross_weight': 27,
        'sell_sideways_trend_adx_strong_down_weight': 0,
        'sell_sideways_trend_bollinger_bands_weight': 85,
        'sell_sideways_trend_ema_long_death_cross_weight': 77,
        'sell_sideways_trend_ema_short_death_cross_weight': 92,
        'sell_sideways_trend_macd_weight': 100,
        'sell_sideways_trend_rsi_weight': 49,
        'sell_sideways_trend_sma_long_death_cross_weight': 61,
        'sell_sideways_trend_sma_short_death_cross_weight': 67,
        'sell_sideways_trend_vwap_cross_weight': 55,
        'sell_upwards_trend_adx_strong_down_weight': 0,
        'sell_upwards_trend_bollinger_bands_weight': 62,
        'sell_upwards_trend_ema_long_death_cross_weight': 65,
        'sell_upwards_trend_ema_short_death_cross_weight': 37,
        'sell_upwards_trend_macd_weight': 84,
        'sell_upwards_trend_rsi_weight': 47,
        'sell_upwards_trend_sma_long_death_cross_weight': 100,
        'sell_upwards_trend_sma_short_death_cross_weight': 0,
        'sell_upwards_trend_vwap_cross_weight': 32
    }

    # ROI table:
    minimal_roi = {
        "0": 0.11138,
        "40": 0.05048,
        "90": 0.0281,
        "198": 0
    }

    # Stoploss:
    stoploss = -0.32665

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01001
    trailing_stop_positive_offset = 0.04046
    trailing_only_offset_is_reached = False

    ####################################################################################################################
    #                                     END OF HYPEROPT RESULTS COPY-PASTE SECTION                                   #
    ####################################################################################################################

    # Create dictionary to store custom information MoniGoMani will be using in RAM
    custom_info = {
        'open_trades': {},
        'trend_indicator': {}
    }

    # Create class level runmode detection (No need for configuration, will automatically be detected,
    # changed & used at runtime)
    is_dry_live_run_detected = True

    # TimeFrame-Zoom
    # To prevent profit exploitation during backtesting/hyperopting we backtest/hyperopt MoniGoMani which would normally
    # use a 'timeframe' (1h candles) using a smaller 'backtest_timeframe' (5m candles) instead.
    # This happens while still using an 'informative_timeframe' (original 1h candles) to generate the buy/sell signals.

    # With this more realistic results should be found during backtesting/hyperopting. Since the buy/sell signals will 
    # operate on the same 'timeframe' that live would use (1h candles), while at the same time 'backtest_timeframe' 
    # (5m or 1m candles) will simulate price movement during that 'timeframe' (1h candle), providing more realistic 
    # trailing stoploss and ROI behaviour during backtesting/hyperopting.

    # Warning: Candle data for both 'timeframe' as 'backtest_timeframe' will have to be downloaded before you will be
    # able to backtest/hyperopt! (Since both will be used)
    # Warning: This will be slower than backtesting at 1h and 1m is a CPU killer. But if you plan on using trailing
    # stoploss or ROI, you probably want to know that your backtest results are not complete lies.
    # Source: https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/

    # To disable TimeFrame-Zoom just use the same candles for 'timeframe' & 'backtest_timeframe'
    timeframe = '1h'  # Optimal TimeFrame for MoniGoMani (used during Dry/Live-Runs)
    backtest_timeframe = '5m'  # Optimal TimeFrame-Zoom for MoniGoMani (used to zoom in during Backtesting/HyperOpting)
    informative_timeframe = timeframe

    # Run "populate_indicators()" only for new candle
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals.
    # In live and dry runs this ratio will be 1, so nothing changes there.
    # But we need `startup_candle_count` to be for the timeframe of 
    # `informative_timeframe` (1h) not `timeframe` (5m) for backtesting.
    startup_candle_count: int = 400 * int(timeframe_to_minutes(informative_timeframe) / timeframe_to_minutes(timeframe))
    # SMA200 needs 200 candles before producing valid signals
    # EMA200 needs an extra 200 candles of SMA200 before producing valid signals

    # Precision
    # This value can be used to control the precision of hyperopting.
    # A value of 1/5 will effectively set the step size to be 5 (0, 5, 10 ...)
    # A value of 5 will set the step size to be 1/5=0.2 (0, 0.2, 0.4, 0.8, ...)
    # A smaller value will limit the search space a lot, but may skip over good values.
    precision = 1

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

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
    buy__downwards_trend_total_signal_needed = IntParameter(0, int(100 * precision), default=65, space='buy',
                                                            optimize=True, load=True)

    # Buy Signal Weight Influence Table
    buy_downwards_trend_adx_strong_up_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_bollinger_bands_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_ema_long_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_ema_short_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_macd_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_rsi_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_sma_long_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_sma_short_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_downwards_trend_vwap_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)

    # Sideways Trend Buy
    # ------------------

    # Total Buy Signal Percentage needed for a signal to be positive
    buy__sideways_trend_total_signal_needed = IntParameter(0, int(100 * precision), default=65, space='buy',
                                                           optimize=True, load=True)

    # Buy Signal Weight Influence Table
    buy_sideways_trend_adx_strong_up_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_bollinger_bands_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_ema_long_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_ema_short_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_macd_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_rsi_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_sma_long_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_sma_short_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_sideways_trend_vwap_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)

    # Upwards Trend Buy
    # -----------------

    # Total Buy Signal Percentage needed for a signal to be positive
    buy__upwards_trend_total_signal_needed = IntParameter(0, int(100 * precision), default=65, space='buy',
                                                          optimize=True, load=True)

    # Buy Signal Weight Influence Table
    buy_upwards_trend_adx_strong_up_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_bollinger_bands_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_ema_long_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_ema_short_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_macd_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_rsi_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_sma_long_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_sma_short_golden_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)
    buy_upwards_trend_vwap_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='buy', optimize=True, load=True)

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
    sell__downwards_trend_total_signal_needed = IntParameter(0, int(100 * precision), default=65, space='sell',
                                                             optimize=True, load=True)

    # Sell Signal Weight Influence Table
    sell_downwards_trend_adx_strong_down_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_bollinger_bands_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_ema_long_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_ema_short_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_macd_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_rsi_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_sma_long_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_sma_short_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_downwards_trend_vwap_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)

    # Sideways Trend Sell
    # -------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    sell__sideways_trend_total_signal_needed = IntParameter(0, int(100 * precision), default=65, space='sell',
                                                            optimize=True, load=True)

    # Sell Signal Weight Influence Table
    sell_sideways_trend_adx_strong_down_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_bollinger_bands_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_ema_long_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_ema_short_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_macd_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_rsi_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_sma_long_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_sma_short_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_sideways_trend_vwap_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)

    # Upwards Trend Sell
    # ------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    sell__upwards_trend_total_signal_needed = IntParameter(0, int(100 * precision), default=65, space='sell',
                                                           optimize=True, load=True)

    # Sell Signal Weight Influence Table
    sell_upwards_trend_adx_strong_down_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_bollinger_bands_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_ema_long_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_ema_short_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_macd_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_rsi_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_sma_long_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_sma_short_death_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
    sell_upwards_trend_vwap_cross_weight = \
        IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)

    # ---------------------------------------------------------------- #
    #             Sell Unclogger HyperOpt Space Parameters             #
    # ---------------------------------------------------------------- #

    sell___unclogger_enabled = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_minimal_losing_trade_duration_minutes = \
    IntParameter(15, int(60 * precision), default=15, space='sell', optimize=True, load=True)
    sell___unclogger_minimal_losing_trades_open = \
        IntParameter(1, int(5 * precision), default=1, space='sell', optimize=True, load=True)
    sell___unclogger_open_trades_losing_percentage_needed = \
        IntParameter(1, int(100 * precision), default=1, space='sell', optimize=True, load=True)
    sell___unclogger_trend_lookback_candles_window = \
        IntParameter(10, int(100 * precision), default=10, space='sell', optimize=True, load=True)
    sell___unclogger_trend_lookback_candles_window_percentage_needed = \
        IntParameter(10, int(100 * precision), default=10, space='sell', optimize=True, load=True)
    sell___unclogger_trend_lookback_window_uses_downwards_candles = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_sideways_candles = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_upwards_candles = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)

    def __init__(self, *args, **kwargs):
        """
        First method to be called once during the MoniGoMani class initialization process
        :param args:
        :param kwargs:
        """
        initialization = 'Initialization'

        super().__init__(*args, **kwargs)
        if not self.dp:
            self.mgm_logger('error', initialization, f'Data Provider is not populated! No indicators will be computed!')

        if (self.dp is not None) and (self.dp.runmode.value in ('backtest', 'hyperopt')):
            self.mgm_logger('info', initialization, f'Current run mode detected as: HyperOpting/BackTesting. '
                                                    f'Auto updating is_dry_live_run_detected to: False')
            self.is_dry_live_run_detected = False

            self.timeframe = self.backtest_timeframe
            self.mgm_logger('info', 'TimeFrame-Zoom', f'Auto updating timeframe to: {self.timeframe}')
        else:
            self.mgm_logger('info', initialization, f'Current run mode detected as: Dry/Live-Run. '
                                                    f'Auto updating is_dry_live_run_detected to: True')
            self.is_dry_live_run_detected = True

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
        Adds indicators based on Run-Mode:
        If BackTesting/HyperOpting it pulls 'informative_pairs' (1h candles) to compute indicators, but then tests upon
        'backtest_timeframe' (5m or 1m candles) to simulate price movement during that 'timeframe' (1h candle).

        If Dry/Live-running it just pulls 'timeframe' (1h candles) to compute indicators.

        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for MoniGoMani
        """
        timeframe_zoom = 'TimeFrame-Zoom'

        # Compute indicator data during Backtesting / Hyperopting
        if self.is_dry_live_run_detected is False:
            self.mgm_logger('info', timeframe_zoom, f'Backtesting/Hyperopting this strategy with a '
                                                    f'informative_timeframe ({self.informative_timeframe}candles) and a'
                                                    f' backtest_timeframe ({self.backtest_timeframe} candles)')

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

        # Compute indicator data during Dry & Live Running
        else:
            self.mgm_logger('info', timeframe_zoom,
                            f'Dry/Live-running MoniGoMani with normal timeframe ({self.timeframe} candles)')
            # Just populate indicators.
            dataframe = self._populate_indicators(dataframe, metadata)

        return dataframe

    def _populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame.
        Should be called with 'informative_pair' (1h candles) during backtesting/hyperopting!

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
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
        dataframe.loc[dataframe['adx'] < 20, 'trend'] = 'sideways'
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

        # Trend Indicator Custom Information Storage
        # -------------------------------------
        # Store the trend indicator mapped to the correct date-times for all pairs in pair_list jf needed,
        # stored in custom information storage to maintain backtest/hyperopt-ability while using the sell unclogger
        if self.sell___unclogger_enabled.value and (self.is_dry_live_run_detected is False):
            self.mgm_logger('info', 'Custom Information Storage', f'Storing whole "trend" indicator for '
                                                                  f'pair ({metadata["pair"]}) in custom_info')

            if metadata['pair'] not in self.custom_info['trend_indicator']:
                self.custom_info['trend_indicator'][metadata['pair']] = {}
            self.custom_info['trend_indicator'][metadata['pair']] = \
                dataframe[['date', 'trend']].dropna().copy().set_index('date')

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

        # Check if buy signal should be sent depending on the current trend
        dataframe.loc[
            (
                    (dataframe['trend'] == 'downwards') &
                    (dataframe['total_buy_signal_strength'] >= self.buy__downwards_trend_total_signal_needed.value /
                     self.precision)
            ) | (
                    (dataframe['trend'] == 'sideways') &
                    (dataframe['total_buy_signal_strength'] >= self.buy__sideways_trend_total_signal_needed.value /
                     self.precision)
            ) | (
                    (dataframe['trend'] == 'upwards') &
                    (dataframe['total_buy_signal_strength'] >= self.buy__upwards_trend_total_signal_needed.value /
                     self.precision)
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

        # Check if sell signal should be sent depending on the current trend
        dataframe.loc[
            (
                    (dataframe['trend'] == 'downwards') &
                    (dataframe['total_sell_signal_strength'] >=
                     self.sell__downwards_trend_total_signal_needed.value / self.precision)
            ) | (
                    (dataframe['trend'] == 'sideways') &
                    (dataframe['total_sell_signal_strength'] >=
                     self.sell__sideways_trend_total_signal_needed.value / self.precision)
            ) | (
                    (dataframe['trend'] == 'upwards') &
                    (dataframe['total_sell_signal_strength'] >=
                     self.sell__upwards_trend_total_signal_needed.value / self.precision)
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
        Open Trade Unclogger:
        ---------------------
        Override Sell Signal: When enabled attempts to unclog the bot when it's stuck with losing trades & unable to
        trade more new trades. This custom_stoploss function should be able to work in tandem with Trailing stoploss.

        It will only unclog a losing trade when all of following checks have been full-filled:
        => Check if everything in custom_storage is up to date with all_open_trades
        => Check if there are enough losing trades open for unclogging to occur
        => Check if there is a losing trade open for the pair currently being ran through the MoniGoMani loop
        => Check if trade has been open for X minutes (long enough to give it a recovery chance)
        => Check if total open trades losing % is met
        => Check if open_trade's trend changed negatively during past X candles

        Please configurable/hyperoptable in the sell_params dictionary under the hyperopt results copy/paste section.
        Only used when use_custom_stoploss & sell_params['sell___unclogger_enabled'] are both set to True.

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in ask_strategy.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return float: New stoploss value, relative to the current-rate
        """
        open_trade_unclogger = 'Open Trade Unclogger'
        custom_information_storage = 'Custom Information Storage'
        garbage_collector = custom_information_storage + ' Garbage Collector'

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

                # Store current pair's open_trade + it's current profit & open_date in custom_info
                for open_trade in all_open_trades:
                    if str(open_trade.pair) == str(pair):
                        if str(open_trade.pair) not in self.custom_info['open_trades']:
                            self.custom_info['open_trades'][str(open_trade.pair)] = {}
                        self.custom_info['open_trades'][str(open_trade.pair)]['trade'] = str(open_trade)
                        self.custom_info['open_trades'][str(open_trade.pair)]['current_profit'] = current_profit
                        # self.custom_info['open_trades'][str(open_trade.pair)]['open_date'] = trade.open_date
                        # ToDo: ^ BugFix/Improve or remove (old trend_indicator garbage)
                        self.mgm_logger('info', custom_information_storage,
                                        f'Storing trade + current profit/loss + open date for pair ({str(pair)}) '
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

                    # ToDo: BugFix/Improve or remove (Warning: outdated code by now)
                    # Check if any old trend_indicator garbage needs to be removed
                    # if self.is_live_or_dry_run is False:

                    #    oldest_date = datetime.utcnow().replace(tzinfo=None)
                    #    for open_trade_pair in self.custom_info['open_trades']:
                    #        if self.custom_info['open_trades'][open_trade_pair]['open_date'].replace(tzinfo=None) < \
                    #                oldest_date:
                    #            oldest_date = self.custom_info['open_trades'][open_trade_pair][
                    #                'open_date'].replace(tzinfo=None)

                    #    for trend_indicator_pair in self.custom_info['trend_indicator']:
                    #        self.custom_info['trend_indicator'][trend_indicator_pair] = \
                    #            self.custom_info['trend_indicator'][trend_indicator_pair][
                    #                self.custom_info['trend_indicator'][trend_indicator_pair].index.tz_convert(None)
                    #                > (oldest_date.replace(tzinfo=None) -
                    #                timedelta(hours=(self.sell___unclogger_trend_lookback_candles_window.value /
                    #                self.precision))]

                # Check if everything in custom_storage is up to date with all_open_trades
                elif len(all_open_trades) > len(self.custom_info['open_trades']):
                    self.mgm_logger('warning', custom_information_storage,
                                    f'Open trades ({str(len(self.custom_info["open_trades"]))}) in custom_storage do '
                                    f'not match yet with trades in live open trades ({str(len(all_open_trades))}) '
                                    f'aborting unclogger for now!')
                    return self.stoploss

                # Print all stored open trade info in custom_storage
                self.mgm_logger('debug', custom_information_storage,
                                f'Open trades ({str(len(self.custom_info["open_trades"]))}) in custom_info updated '
                                f'successfully!')
                self.mgm_logger('debug', custom_information_storage,
                                f'custom_info["open_trades"] contents: {repr(self.custom_info["open_trades"])}')

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
                                f'Fetched losing_open_trades ({str(len(losing_open_trades))}) from custom information '
                                f'storage!')

                if len(losing_open_trades) < \
                        round(self.sell___unclogger_minimal_losing_trades_open.value / self.precision):
                    self.mgm_logger('debug', open_trade_unclogger,
                                    f'No unclogging needed! Not enough losing trades currently open!')
                else:
                    self.mgm_logger('debug', open_trade_unclogger,
                                    f'Enough losing trades detected! Proceeding to the next check!')

                    # Check if there is a losing trade open for the pair currently being ran through the MoniGoMani loop
                    if pair not in losing_open_trades:
                        self.mgm_logger('debug', open_trade_unclogger,
                                        f'No unclogging needed! Currently checked pair ({pair}) is not making a loss '
                                        f'at this point in time!')
                    else:
                        self.mgm_logger('debug', open_trade_unclogger,
                                        f'Currently checked pair ({pair}) is losing! Proceeding to the next check!')

                        # Check if trade has been open for X minutes (long enough to give it a recovery chance)
                        if self.is_dry_live_run_detected is True:
                            current_datetime_to_use = datetime.utcnow()
                        else:
                            current_datetime_to_use = current_time

                        self.mgm_logger('debug', open_trade_unclogger,
                                        f'Trade open time : {str(trade.open_date_utc.replace(tzinfo=None))}')
                        minimal_open_time = current_datetime_to_use.replace(tzinfo=None) - timedelta(minutes=round(
                            self.sell___unclogger_minimal_losing_trade_duration_minutes.value / self.precision))

                        self.mgm_logger('debug', open_trade_unclogger, f'Minimal open time: {str(minimal_open_time)}')

                        if trade.open_date_utc.replace(tzinfo=None) > minimal_open_time:
                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'No unclogging needed! Currently checked pair ({pair}) has not been open '
                                            f'been open for long enough!')
                        else:
                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'Trade has been open for long enough! Proceeding to the next check!')

                            # Check if total open trades losing % is met
                            percentage_open_trades_losing = int((len(losing_open_trades) / len(all_open_trades)) * 100)
                            self.mgm_logger('debug', open_trade_unclogger,
                                            f'percentage_open_trades_losing: {str(percentage_open_trades_losing)}%')
                            if percentage_open_trades_losing < round(
                                    self.sell___unclogger_open_trades_losing_percentage_needed.value / self.precision):
                                self.mgm_logger('debug', open_trade_unclogger,
                                                f'No unclogging needed! Percentage of open trades losing needed has '
                                                f'not been satisfied!')
                            else:
                                self.mgm_logger('debug', open_trade_unclogger,
                                                f'Percentage of open trades losing needed has been satisfied! '
                                                f'Proceeding to the next check!')

                                # Fetch current dataframe for the pair currently being ran through the MoniGoMani loop
                                self.mgm_logger('debug', open_trade_unclogger,
                                                f'Fetching currently needed "trend" dataframe data to check how pair '
                                                f'({pair}) has been doing in during the last '
                                                f'{str(self.sell___unclogger_trend_lookback_candles_window.value / self.precision)}'
                                                f' candles')

                                # Fetch all needed 'trend' trade data during Dry & Live Running
                                stored_trend_dataframe = {}
                                if self.is_dry_live_run_detected is True:
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'Fetching all needed "trend" trade data during Dry/Live Run')
                                    dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair,
                                                                                             timeframe=self.timeframe)

                                    # Data is nan at 0 so incrementing loop with 1
                                    for candle in range(1, round(
                                            self.sell___unclogger_trend_lookback_candles_window.value / self.precision)
                                                           + 1):
                                        stored_trend_dataframe[candle] = dataframe['trend'].iat[candle * -1]
                                        # Warning: Only use .iat[-1] in dry/live-run modes! Not during
                                        # backtesting/hyperopting! (Otherwise you will try to look into the future)

                                # Fetch all needed 'trend' trade data during Backtesting/Hyperopting
                                else:
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'Fetching all needed "trend" trade data during '
                                                    f'BackTesting/HyperOpting')

                                    for candle in range(1,
                                                        round(self.sell___unclogger_trend_lookback_candles_window.value
                                                              / self.precision) + 1):
                                        # Convert the candle time to the one being used by the 'informative_timeframe'
                                        candle_multiplier = int(self.informative_timeframe.rstrip("mhdwM"))
                                        candle_time = current_time - timedelta(minutes=int(candle * candle_multiplier))
                                        if self.informative_timeframe.find('h') != -1:
                                            candle_time = current_time - \
                                                          timedelta(hours=int(candle * candle_multiplier))
                                        elif self.informative_timeframe.find('d') != -1:
                                            candle_time = current_time - \
                                                          timedelta(days=int(candle * candle_multiplier))
                                        elif self.informative_timeframe.find('w') != -1:
                                            candle_time = current_time - \
                                                          timedelta(weeks=int(candle * candle_multiplier))
                                        elif self.informative_timeframe.find('M') != -1:
                                            candle_time = current_time - \
                                                          timedelta64(int(1 * candle_multiplier), 'M')
                                        stored_trend_dataframe[candle] = \
                                            self.custom_info['trend_indicator'][pair].loc[candle_time]['trend']

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
                                                    f'stored_trend_dataframe contents: {repr(stored_trend_dataframe)}')

                                    # Check if open_trade's trend changed negatively during past X candles
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'Calculating amount of unclogger_candles_satisfied satisfied for '
                                                    f'pair: {pair}')
                                    unclogger_candles_satisfied = 0
                                    for lookback_candle \
                                            in range(1, round(self.sell___unclogger_trend_lookback_candles_window.value
                                                              / self.precision) + 1):
                                        if self.sell___unclogger_trend_lookback_window_uses_downwards_candles.value & \
                                                (stored_trend_dataframe[lookback_candle] == 'downwards'):
                                            unclogger_candles_satisfied += 1
                                        if self.sell___unclogger_trend_lookback_window_uses_sideways_candles.value & \
                                                (stored_trend_dataframe[lookback_candle] == 'sideways'):
                                            unclogger_candles_satisfied += 1
                                        if self.sell___unclogger_trend_lookback_window_uses_upwards_candles.value & \
                                                (stored_trend_dataframe[lookback_candle] == 'upwards'):
                                            unclogger_candles_satisfied += 1
                                    self.mgm_logger('debug', open_trade_unclogger,
                                                    f'unclogger_candles_satisfied: {str(unclogger_candles_satisfied)} '
                                                    f'for pair: {pair}')

                                    # Calculate the percentage of the lookback window currently satisfied
                                    unclogger_candles_percentage_satisfied = \
                                        (unclogger_candles_satisfied /
                                         round(self.sell___unclogger_trend_lookback_candles_window.value /
                                               self.precision)) * 100

                                    # Override Sell Signal: Unclog trade by setting it's stoploss to 0% forcing a sell &
                                    # attempt to continue the profit climb with the "freed up trading slot"
                                    if unclogger_candles_percentage_satisfied >= \
                                            round(
                                                self.sell___unclogger_trend_lookback_candles_window_percentage_needed.value
                                                / self.precision):
                                        self.mgm_logger('info', open_trade_unclogger, f'Unclogging losing trade...')
                                        return -0.00001  # Setting very low since 0% is seen as invalid by Freqtrade
                                    else:
                                        self.mgm_logger('info', open_trade_unclogger, f'No need to unclog open trade...')

            except Exception as e:
                self.mgm_logger('error', open_trade_unclogger,
                                f'Following error has occurred in the Open Trade Unclogger:')
                self.mgm_logger('error', open_trade_unclogger, str(e))

        """
        # ==============================================================================================================
        # Unsure if this is needed, Freqtrade bot-loop-execution docs unclear on the matter
        # ==============================================================================================================
        patched_stoploss = 'Patched Trailing StopLoss'
        if self.trailing_stop:
            if (current_profit > 0) and (self.trailing_stop_positive > 0) \
                    and (not self.trailing_only_offset_is_reached):
                self.mgm_logger('debug', patched_stoploss,
                                f'Returning {-self.trailing_stop_positive} in no offset mode')
                return -self.trailing_stop_positive
            elif (current_profit >= self.trailing_stop_positive_offset) and (self.trailing_stop_positive > 0) \
                    and self.trailing_only_offset_is_reached:
                self.mgm_logger('debug', patched_stoploss,
                                f'Returning {-self.trailing_stop_positive} in offset mode since {current_profit} >= '
                                f'{self.trailing_stop_positive_offset}')
                return -self.trailing_stop_positive
            else:
                return self.stoploss
        else:
            self.mgm_logger('debug', patched_stoploss, f'Returning default stoploss {self.stoploss}')
            return self.stoploss
        # ==============================================================================================================
        """

        return self.stoploss

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
