# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
# --------------------------------
# Add your lib to import here
import talib.abstract as ta
from pandas import DataFrame

# ^ TA-Lib Autofill mostly broken in JetBrains Products,
# ta._ta_lib.<function_name> can temporarily be used while writing as a workaround
# Then change back to ta.<function_name> so IDE won't nag about accessing a protected member of TA-Lib
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy import IStrategy


class MoniGoManiHyperOpted(IStrategy):
    """
    ####################################################################################
    ####                                                                            ####
    ###            MoniGoMani v0.7.2 HyperOpted by Rikj000 (01-04-2021)              ###
    ##             ----------------------------------------------------               ##
    #               Isn't that what we all want? Our money to go many?                 #
    #          Well that's what this Freqtrade strategy hopes to do for you!           #
    ##       By giving you/HyperOpt a lot of signals to alter the weight from         ##
    ###           ------------------------------------------------------             ###
    ##        Big thank you to xmatthias and everyone who helped on Freqtrade,        ##
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

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the prototype for the methods: minimal_roi, stoploss, populate_indicators, populate_buy_trend,
    populate_sell_trend, hyperopt_space, buy_strategy_generator
    """

    # Trend Detecting Buy/Sell Signal Weight Influence Tables
    # -------------------------------------------------------
    # The idea is to fill in here how heavily you/hyperopt thinks an indicator
    # signals a buy/sell signal compared to the other indicators (Signals can be turned off by allocating 0 or
    # turned into an override by setting them equal to or higher then total_buy_signal_needed)
    # These Signal Weight Influence Tables will be allocated to signals when their respective trend is detected

    # Buy hyperspace params:
    buy_params = {
        '.trade_buys_when_downwards': True,
        '.trade_buys_when_sideways': False,
        '.trade_buys_when_upwards': True,
        '_downwards_trend_total_buy_signal_needed': 70,
        '_sideways_trend_total_buy_signal_needed': 35,
        '_upwards_trend_total_buy_signal_needed': 97,
        'downwards_trend_adx_strong_up_buy_weight': 47,
        'downwards_trend_bollinger_bands_buy_weight': 47,
        'downwards_trend_ema_long_golden_cross_buy_weight': 4,
        'downwards_trend_ema_short_golden_cross_buy_weight': 13,
        'downwards_trend_macd_buy_weight': 92,
        'downwards_trend_rsi_buy_weight': 64,
        'downwards_trend_sma_long_golden_cross_buy_weight': 94,
        'downwards_trend_sma_short_golden_cross_buy_weight': 37,
        'downwards_trend_vwap_cross_buy_weight': 41,
        'sideways_trend_adx_strong_up_buy_weight': 75,
        'sideways_trend_bollinger_bands_buy_weight': 40,
        'sideways_trend_ema_long_golden_cross_buy_weight': 37,
        'sideways_trend_ema_short_golden_cross_buy_weight': 74,
        'sideways_trend_macd_buy_weight': 30,
        'sideways_trend_rsi_buy_weight': 81,
        'sideways_trend_sma_long_golden_cross_buy_weight': 73,
        'sideways_trend_sma_short_golden_cross_buy_weight': 67,
        'sideways_trend_vwap_cross_buy_weight': 48,
        'upwards_trend_adx_strong_up_buy_weight': 98,
        'upwards_trend_bollinger_bands_buy_weight': 15,
        'upwards_trend_ema_long_golden_cross_buy_weight': 27,
        'upwards_trend_ema_short_golden_cross_buy_weight': 24,
        'upwards_trend_macd_buy_weight': 99,
        'upwards_trend_rsi_buy_weight': 1,
        'upwards_trend_sma_long_golden_cross_buy_weight': 62,
        'upwards_trend_sma_short_golden_cross_buy_weight': 82,
        'upwards_trend_vwap_cross_buy_weight': 79
    }

    # Sell hyperspace params:
    sell_params = {
        '.trade_sells_when_downwards': True,
        '.trade_sells_when_sideways': True,
        '.trade_sells_when_upwards': False,
        '_downwards_trend_total_sell_signal_needed': 91,
        '_sideways_trend_total_sell_signal_needed': 79,
        '_upwards_trend_total_sell_signal_needed': 90,
        'downwards_trend_adx_strong_down_sell_weight': 42,
        'downwards_trend_bollinger_bands_sell_weight': 84,
        'downwards_trend_ema_long_death_cross_sell_weight': 85,
        'downwards_trend_ema_short_death_cross_sell_weight': 75,
        'downwards_trend_macd_sell_weight': 12,
        'downwards_trend_rsi_sell_weight': 0,
        'downwards_trend_sma_long_death_cross_sell_weight': 12,
        'downwards_trend_sma_short_death_cross_sell_weight': 100,
        'downwards_trend_vwap_cross_sell_weight': 83,
        'sideways_trend_adx_strong_down_sell_weight': 19,
        'sideways_trend_bollinger_bands_sell_weight': 85,
        'sideways_trend_ema_long_death_cross_sell_weight': 45,
        'sideways_trend_ema_short_death_cross_sell_weight': 96,
        'sideways_trend_macd_sell_weight': 92,
        'sideways_trend_rsi_sell_weight': 13,
        'sideways_trend_sma_long_death_cross_sell_weight': 100,
        'sideways_trend_sma_short_death_cross_sell_weight': 34,
        'sideways_trend_vwap_cross_sell_weight': 13,
        'upwards_trend_adx_strong_down_sell_weight': 22,
        'upwards_trend_bollinger_bands_sell_weight': 95,
        'upwards_trend_ema_long_death_cross_sell_weight': 79,
        'upwards_trend_ema_short_death_cross_sell_weight': 20,
        'upwards_trend_macd_sell_weight': 56,
        'upwards_trend_rsi_sell_weight': 82,
        'upwards_trend_sma_long_death_cross_sell_weight': 41,
        'upwards_trend_sma_short_death_cross_sell_weight': 53,
        'upwards_trend_vwap_cross_sell_weight': 91
    }

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.30588,
        "142": 0.20322,
        "847": 0.06578,
        "1218": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.24019

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01184
    trailing_stop_positive_offset = 0.03793
    trailing_only_offset_is_reached = False

    # Optimal timeframe for the strategy.
    timeframe = '1h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 400
    # SMA200 needs 200 candles before producing valid signals
    # EMA200 needs an extra 200 candles of SMA200 before producing valid signals

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

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
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
            dataframe['rsi_weighted_buy_signal'] = dataframe['rsi_weighted_sell_signal'] = 0
            dataframe['macd_weighted_buy_signal'] = dataframe['macd_weighted_sell_signal'] = 0
            dataframe['sma_short_golden_cross_weighted_buy_signal'] = 0
            dataframe['sma_short_death_cross_weighted_sell_signal'] = 0
            dataframe['ema_short_golden_cross_weighted_buy_signal'] = 0
            dataframe['ema_short_death_cross_weighted_sell_signal'] = 0
            dataframe['sma_long_golden_cross_weighted_buy_signal'] = 0
            dataframe['sma_long_death_cross_weighted_sell_signal'] = 0
            dataframe['ema_long_golden_cross_weighted_buy_signal'] = 0
            dataframe['ema_long_death_cross_weighted_sell_signal'] = 0
            dataframe['bollinger_bands_weighted_buy_signal'] = dataframe['bollinger_bands_weighted_sell_signal'] = 0
            dataframe['vwap_cross_weighted_buy_signal'] = dataframe['vwap_cross_weighted_sell_signal'] = 0

        # Initialize total signal variables (should be 0 = false by default)
        dataframe['total_buy_signal_strength'] = dataframe['total_sell_signal_strength'] = 0

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """

        # Detect if current trend going Downwards / Sideways / Upwards, strategy will respond accordingly
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
        dataframe.loc[dataframe['adx'] < 20, 'trend'] = 'sideways'
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

        # If a Weighted Buy Signal goes off => Bullish Indication, Set to true (=1) and multiply by weight percentage

        # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
        dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                      'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_adx_strong_up_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                      'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_adx_strong_up_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                      'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_adx_strong_up_buy_weight']

        # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                      'total_buy_signal_strength'] += 1 * self.buy_params['downwards_trend_rsi_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['rsi'], 30),
                      'total_buy_signal_strength'] += 1 * self.buy_params['sideways_trend_rsi_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                      'total_buy_signal_strength'] += 1 * self.buy_params['upwards_trend_rsi_buy_weight']

        # Weighted Buy Signal: MACD above Signal
        dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] > dataframe['macdsignal']),
                      'total_buy_signal_strength'] += 1 * self.buy_params['downwards_trend_macd_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] > dataframe['macdsignal']),
                      'total_buy_signal_strength'] += 1 * self.buy_params['sideways_trend_macd_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] > dataframe['macdsignal']),
                      'total_buy_signal_strength'] += 1 * self.buy_params['upwards_trend_macd_buy_weight']

        # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
            'sma50']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_sma_short_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
            'sma50']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_sma_short_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
            'sma50']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_sma_short_golden_cross_buy_weight']

        # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
            'ema50']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_ema_short_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
            'ema50']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_ema_short_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
            'ema50']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_ema_short_golden_cross_buy_weight']

        # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
            'sma200']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_sma_long_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
            'sma200']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_sma_long_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
            'sma200']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_sma_long_golden_cross_buy_weight']

        # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
            'ema200']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_ema_long_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
            'ema200']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_ema_long_golden_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
            'ema200']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_ema_long_golden_cross_buy_weight']

        # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
        # (Candle closes below Upper Bollinger Band)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
            'bb_lowerband']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_bollinger_bands_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['close'], dataframe[
            'bb_lowerband']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_bollinger_bands_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
            'bb_lowerband']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_bollinger_bands_buy_weight']

        # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
            'close']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['downwards_trend_vwap_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
            'close']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['sideways_trend_vwap_cross_buy_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
            'close']), 'total_buy_signal_strength'] += \
            1 * self.buy_params['upwards_trend_vwap_cross_buy_weight']

        # Check if buy signal should be sent depending on the current trend
        dataframe.loc[(dataframe['trend'] == 'downwards') &
                      (dataframe['total_buy_signal_strength'] >=
                       self.buy_params['_downwards_trend_total_buy_signal_needed']), 'buy'] = 1
        dataframe.loc[(dataframe['trend'] == 'sideways') &
                      (dataframe['total_buy_signal_strength'] >=
                       self.buy_params['_sideways_trend_total_buy_signal_needed']), 'buy'] = 1
        dataframe.loc[(dataframe['trend'] == 'upwards') &
                      (dataframe['total_buy_signal_strength'] >=
                       self.buy_params['_upwards_trend_total_buy_signal_needed']), 'buy'] = 1

        # Override Buy Signal: When configured buy signals can be completely turned off for each kind of trend
        if not self.buy_params['.trade_buys_when_downwards']:
            dataframe.loc[dataframe['trend'] == 'downwards', 'buy'] = 0
        if not self.buy_params['.trade_buys_when_sideways']:
            dataframe.loc[dataframe['trend'] == 'sideways', 'buy'] = 0
        if not self.buy_params['.trade_buys_when_upwards']:
            dataframe.loc[dataframe['trend'] == 'upwards', 'buy'] = 0

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """

        # Detect if current trend going Downwards / Sideways / Upwards, strategy will respond accordingly
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
        dataframe.loc[dataframe['adx'] < 20, 'trend'] = 'sideways'
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

        # If a Weighted Sell Signal goes off => Bearish Indication, Set to true (=1) and multiply by weight percentage
        # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
        dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                      'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_adx_strong_down_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                      'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_adx_strong_down_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                      'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_adx_strong_down_sell_weight']

        # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                      'total_sell_signal_strength'] += 1 * self.sell_params['downwards_trend_rsi_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['rsi'], 70),
                      'total_sell_signal_strength'] += 1 * self.sell_params['sideways_trend_rsi_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                      'total_sell_signal_strength'] += 1 * self.sell_params['upwards_trend_rsi_sell_weight']

        # Weighted Sell Signal: MACD below Signal
        dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] < dataframe['macdsignal']),
                      'total_sell_signal_strength'] += 1 * self.sell_params['downwards_trend_macd_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] < dataframe['macdsignal']),
                      'total_sell_signal_strength'] += 1 * self.sell_params['sideways_trend_macd_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] < dataframe['macdsignal']),
                      'total_sell_signal_strength'] += 1 * self.sell_params['upwards_trend_macd_sell_weight']

        # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
            'sma50']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_sma_short_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
            'sma50']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_sma_short_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
            'sma50']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_sma_short_death_cross_sell_weight']

        # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
            'ema50']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_ema_short_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
            'ema50']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_ema_short_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
            'ema50']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_ema_short_death_cross_sell_weight']

        # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
            'sma200']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_sma_long_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
            'sma200']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_sma_long_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
            'sma200']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_sma_long_death_cross_sell_weight']

        # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
            'ema200']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_ema_long_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
            'ema200']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_ema_long_death_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
            'ema200']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_ema_long_death_cross_sell_weight']

        # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
        # (Candle closes below Upper Bollinger Band)
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
            'bb_upperband']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_bollinger_bands_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['close'], dataframe[
            'bb_upperband']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_bollinger_bands_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
            'bb_upperband']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_bollinger_bands_sell_weight']

        # Weighted Sell Signal: VWAP crosses below current price
        dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
            'close']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['downwards_trend_vwap_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
            'close']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['sideways_trend_vwap_cross_sell_weight']
        dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
            'close']), 'total_sell_signal_strength'] += \
            1 * self.sell_params['upwards_trend_vwap_cross_sell_weight']

        # Check if sell signal should be sent depending on the current trend
        dataframe.loc[(dataframe['trend'] == 'downwards') &
                      (dataframe['total_sell_signal_strength'] >=
                       self.sell_params['_downwards_trend_total_sell_signal_needed']), 'sell'] = 1
        dataframe.loc[(dataframe['trend'] == 'sideways') &
                      (dataframe['total_sell_signal_strength'] >=
                       self.sell_params['_sideways_trend_total_sell_signal_needed']), 'sell'] = 1
        dataframe.loc[(dataframe['trend'] == 'upwards') &
                      (dataframe['total_sell_signal_strength'] >=
                       self.sell_params['_upwards_trend_total_sell_signal_needed']), 'sell'] = 1

        # Override Sell Signal: When configured sell signals can be completely turned off for each kind of trend
        if not self.sell_params['.trade_sells_when_downwards']:
            dataframe.loc[dataframe['trend'] == 'downwards', 'sell'] = 0
        if not self.sell_params['.trade_sells_when_sideways']:
            dataframe.loc[dataframe['trend'] == 'sideways', 'sell'] = 0
        if not self.sell_params['.trade_sells_when_upwards']:
            dataframe.loc[dataframe['trend'] == 'upwards', 'sell'] = 0

        return dataframe
