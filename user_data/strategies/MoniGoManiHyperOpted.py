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
    ###            MoniGoMani v0.6.4 HyperOpted by Rikj000 (29-03-2021)              ###
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

    # If enabled all Weighted Signal results will be added to the dataframe for easy debugging
    debuggable_weighted_signal_dataframe = False

    # Trend Detecting Buy/Sell Signal Weight Influence Tables
    # -------------------------------------------------------
    # The idea is to fill in here how heavily you/hyperopt thinks an indicator
    # signals a buy/sell signal compared to the other indicators (Signals can be turned off by allocating 0 or
    # turned into an override by setting them equal to or higher then total_buy_signal_needed)
    # These Signal Weight Influence Tables will be allocated to signals when their respective trend is detected

    trend = {
        'downwards': {
            # React to Buy/Sell Signals when Downwards trends are detected (False = Disable trading in downwards trends)
            'trade_buys_when_downwards': True,
            'trade_sells_when_downwards': False,
            # Total Buy/Sell Signal Percentage needed for a signal to be positive
            'total_buy_signal_needed': 5,
            'total_sell_signal_needed': 93,

            # Buy Signal Weight Influence Table
            'adx_strong_up_buy_weight': 86,  # triggers moderately
            'bollinger_bands_buy_weight': 97,  # triggers moderately
            'ema_long_golden_cross_buy_weight': 35,  # triggers very infrequently
            'ema_short_golden_cross_buy_weight': 21,  # triggers infrequently
            'macd_buy_weight': 34,  # triggers frequently
            'rsi_buy_weight': 72,  # triggers infrequently
            'sma_long_golden_cross_buy_weight': 7,  # triggers very infrequently
            'sma_short_golden_cross_buy_weight': 100,  # triggers infrequently
            'vwap_cross_buy_weight': 83,  # triggers infrequently

            # Sell Signal Weight Influence Table
            'adx_strong_down_sell_weight': 60,  # triggers moderately
            'bollinger_bands_sell_weight': 5,  # triggers moderately
            'ema_long_death_cross_sell_weight': 59,  # triggers very infrequently
            'ema_short_death_cross_sell_weight': 54,  # triggers very infrequently
            'macd_sell_weight': 35,  # triggers frequently
            'rsi_sell_weight': 11,  # triggers infrequently
            'sma_long_death_cross_sell_weight': 69,  # triggers very infrequently
            'sma_short_death_cross_sell_weight': 93,  # triggers very infrequently
            'vwap_cross_sell_weight': 77  # triggers infrequently
        },

        'sideways': {
            # React to Buy/Sell Signals when Sideways trends are detected (Risky, but doing nothing isn't good either)
            'trade_buys_when_sideways': True,
            'trade_sells_when_sideways': True,

            # Total Buy/Sell Signal Percentage needed for a signal to be positive
            'total_buy_signal_needed': 21,
            'total_sell_signal_needed': 70,

            # Buy Signal Weight Influence Table
            'adx_strong_up_buy_weight': 84,  # triggers moderately
            'bollinger_bands_buy_weight': 27,  # triggers moderately
            'ema_long_golden_cross_buy_weight': 49,  # triggers very infrequently
            'ema_short_golden_cross_buy_weight': 82,  # triggers infrequently
            'macd_buy_weight': 0,  # triggers frequently
            'rsi_buy_weight': 49,  # triggers infrequently
            'sma_long_golden_cross_buy_weight': 12,  # triggers very infrequently
            'sma_short_golden_cross_buy_weight': 21,  # triggers infrequently
            'vwap_cross_buy_weight': 97,  # triggers infrequently

            # Sell Signal Weight Influence Table
            'adx_strong_down_sell_weight': 26,  # triggers moderately
            'bollinger_bands_sell_weight': 86,  # triggers moderately
            'ema_long_death_cross_sell_weight': 0,  # triggers very infrequently
            'ema_short_death_cross_sell_weight': 49,  # triggers very infrequently
            'macd_sell_weight': 84,  # triggers frequently
            'rsi_sell_weight': 3,  # triggers infrequently
            'sma_long_death_cross_sell_weight': 43,  # triggers very infrequently
            'sma_short_death_cross_sell_weight': 10,  # triggers very infrequently
            'vwap_cross_sell_weight': 69  # triggers infrequently
        },

        # These Signal Weight Influence Tables will be allocated to signals when an upward trend is detected
        'upwards': {
            # React to Buy/Sell Signals when Upwards trends are detected (False = Disable trading in upwards trends)
            'trade_buys_when_upwards': True,
            'trade_sells_when_upwards': False,
            # Total Buy/Sell Signal Percentage needed for a signal to be positive
            'total_buy_signal_needed': 60,
            'total_sell_signal_needed': 25,

            # Buy Signal Weight Influence Table
            'adx_strong_up_buy_weight': 52,  # triggers moderately
            'bollinger_bands_buy_weight': 15,  # triggers moderately
            'ema_long_golden_cross_buy_weight': 11,  # triggers very infrequently
            'ema_short_golden_cross_buy_weight': 23,  # triggers infrequently
            'macd_buy_weight': 93,  # triggers frequently
            'rsi_buy_weight': 21,  # triggers infrequently
            'sma_long_golden_cross_buy_weight': 27,  # triggers very infrequently
            'sma_short_golden_cross_buy_weight': 95,  # triggers infrequently
            'vwap_cross_buy_weight': 50,  # triggers infrequently

            # Sell Signal Weight Influence Table
            'adx_strong_down_sell_weight': 69,  # triggers moderately
            'bollinger_bands_sell_weight': 8,  # triggers moderately
            'ema_long_death_cross_sell_weight': 28,  # triggers very infrequently
            'ema_short_death_cross_sell_weight': 68,  # triggers very infrequently
            'macd_sell_weight': 3,  # triggers frequently
            'rsi_sell_weight': 89,  # triggers infrequently
            'sma_long_death_cross_sell_weight': 33,  # triggers very infrequently
            'sma_short_death_cross_sell_weight': 87,  # triggers very infrequently
            'vwap_cross_sell_weight': 51  # triggers infrequently
        }
    }

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.29935,
        "167": 0.10834,
        "743": 0.047,
        "1535": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.11009

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01063
    trailing_stop_positive_offset = 0.01839
    trailing_only_offset_is_reached = True

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

        if self.debuggable_weighted_signal_dataframe:
            # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'adx_strong_up_weighted_buy_signal'] = 1 * self.trend['downwards']['adx_strong_up_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'adx_strong_up_weighted_buy_signal'] = 1 * self.trend['sideways']['adx_strong_up_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'adx_strong_up_weighted_buy_signal'] = 1 * self.trend['upwards']['adx_strong_up_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['adx_strong_up_weighted_buy_signal']

            # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'rsi_weighted_buy_signal'] = 1 * self.trend['downwards']['rsi_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'rsi_weighted_buy_signal'] = 1 * self.trend['sideways']['rsi_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'rsi_weighted_buy_signal'] = 1 * self.trend['upwards']['rsi_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['rsi_weighted_buy_signal']

            # Weighted Buy Signal: MACD above Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'macd_weighted_buy_signal'] = 1 * self.trend['downwards']['macd_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] > dataframe['macdsignal']),
                          'macd_weighted_buy_signal'] = 1 * self.trend['sideways']['macd_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'macd_weighted_buy_signal'] = 1 * self.trend['upwards']['macd_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['macd_weighted_buy_signal']

            # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['downwards']['sma_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['sideways']['sma_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['upwards']['sma_short_golden_cross_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['sma_short_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['downwards']['ema_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['sideways']['ema_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['upwards']['ema_short_golden_cross_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['ema_short_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['downwards']['sma_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['sideways']['sma_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['upwards']['sma_long_golden_cross_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['sma_long_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['downwards']['ema_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['sideways']['ema_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_golden_cross_weighted_buy_signal'] = \
                1 * self.trend['upwards']['ema_long_golden_cross_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['ema_long_golden_cross_weighted_buy_signal']

            # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'bollinger_bands_weighted_buy_signal'] = \
                1 * self.trend['downwards']['bollinger_bands_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'bollinger_bands_weighted_buy_signal'] = \
                1 * self.trend['sideways']['bollinger_bands_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'bollinger_bands_weighted_buy_signal'] = \
                1 * self.trend['upwards']['bollinger_bands_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['bollinger_bands_weighted_buy_signal']

            # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_buy_signal'] = 1 * self.trend['downwards']['vwap_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_buy_signal'] = 1 * self.trend['sideways']['vwap_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_buy_signal'] = 1 * self.trend['upwards']['vwap_cross_buy_weight']
            dataframe['total_buy_signal_strength'] += dataframe['vwap_cross_weighted_buy_signal']

        else:
            # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += 1 * self.trend['downwards']['adx_strong_up_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += 1 * self.trend['sideways']['adx_strong_up_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += 1 * self.trend['upwards']['adx_strong_up_buy_weight']

            # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += 1 * self.trend['downwards']['rsi_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += 1 * self.trend['sideways']['rsi_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += 1 * self.trend['upwards']['rsi_buy_weight']

            # Weighted Buy Signal: MACD above Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += 1 * self.trend['downwards']['macd_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += 1 * self.trend['sideways']['macd_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += 1 * self.trend['upwards']['macd_buy_weight']

            # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += 1 * self.trend['downwards'][
                'sma_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += 1 * self.trend['sideways'][
                'sma_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += 1 * self.trend['upwards'][
                'sma_short_golden_cross_buy_weight']

            # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += 1 * self.trend['downwards'][
                'ema_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += 1 * self.trend['sideways'][
                'ema_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += 1 * self.trend['upwards'][
                'ema_short_golden_cross_buy_weight']

            # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += 1 * self.trend['downwards'][
                'sma_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += 1 * self.trend['sideways'][
                'sma_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += 1 * self.trend['upwards'][
                'sma_long_golden_cross_buy_weight']

            # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += 1 * self.trend['downwards'][
                'ema_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += 1 * self.trend['sideways'][
                'ema_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += 1 * self.trend['upwards'][
                'ema_long_golden_cross_buy_weight']

            # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += 1 * self.trend['downwards'][
                'bollinger_bands_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += 1 * self.trend['sideways'][
                'bollinger_bands_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += 1 * self.trend['upwards'][
                'bollinger_bands_buy_weight']

            # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += 1 * self.trend['downwards']['vwap_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += 1 * self.trend['sideways']['vwap_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += 1 * self.trend['upwards']['vwap_cross_buy_weight']

        # Check if buy signal should be sent depending on the current trend
        dataframe.loc[(dataframe['trend'] == 'downwards') &
                      (dataframe['total_buy_signal_strength'] >= self.trend['downwards']['total_buy_signal_needed']),
                      'buy'] = 1
        dataframe.loc[(dataframe['trend'] == 'sideways') &
                      (dataframe['total_buy_signal_strength'] >= self.trend['sideways']['total_buy_signal_needed']),
                      'buy'] = 1
        dataframe.loc[(dataframe['trend'] == 'upwards') &
                      (dataframe['total_buy_signal_strength'] >= self.trend['upwards']['total_buy_signal_needed']),
                      'buy'] = 1

        # Override Buy Signal: When configured buy signals can be completely turned off for each kind of trend
        if not self.trend['downwards']['trade_buys_when_downwards']:
            dataframe.loc[dataframe['trend'] == 'downwards', 'buy'] = 0
        if not self.trend['sideways']['trade_buys_when_sideways']:
            dataframe.loc[dataframe['trend'] == 'sideways', 'buy'] = 0
        if not self.trend['upwards']['trade_buys_when_upwards']:
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

        if self.debuggable_weighted_signal_dataframe:
            # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'adx_strong_down_weighted_sell_signal'] = \
                1 * self.trend['downwards']['adx_strong_down_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'adx_strong_down_weighted_sell_signal'] = \
                1 * self.trend['sideways']['adx_strong_down_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'adx_strong_down_weighted_sell_signal'] = \
                1 * self.trend['upwards']['adx_strong_down_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['adx_strong_down_weighted_sell_signal']

            # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'rsi_weighted_sell_signal'] = 1 * self.trend['downwards']['rsi_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'rsi_weighted_sell_signal'] = 1 * self.trend['sideways']['rsi_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'rsi_weighted_sell_signal'] = 1 * self.trend['upwards']['rsi_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['rsi_weighted_sell_signal']

            # Weighted Sell Signal: MACD below Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'macd_weighted_sell_signal'] = 1 * self.trend['downwards']['macd_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] < dataframe['macdsignal']),
                          'macd_weighted_sell_signal'] = 1 * self.trend['sideways']['macd_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'macd_weighted_sell_signal'] = 1 * self.trend['upwards']['macd_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['macd_weighted_sell_signal']

            # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_death_cross_weighted_sell_signal'] = \
                1 * self.trend['downwards']['sma_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_death_cross_weighted_sell_signal'] = \
                1 * self.trend['sideways']['sma_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'sma_short_death_cross_weighted_sell_signal'] = \
                1 * self.trend['upwards']['sma_short_death_cross_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['sma_short_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_death_cross_weighted_sell_signal'] = \
                1 * self.trend['downwards']['ema_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_death_cross_weighted_sell_signal'] = \
                1 * self.trend['sideways']['ema_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'ema_short_death_cross_weighted_sell_signal'] = \
                1 * self.trend['upwards']['ema_short_death_cross_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['ema_short_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_death_cross_weighted_sell_signal'] = \
                1 * self.trend['downwards']['sma_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_death_cross_weighted_sell_signal'] = \
                1 * self.trend['sideways']['sma_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'sma_long_death_cross_weighted_sell_signal'] = \
                1 * self.trend['upwards']['sma_long_death_cross_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['sma_long_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_death_cross_weighted_sell_signal'] = \
                1 * self.trend['downwards']['ema_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_death_cross_weighted_sell_signal'] = \
                1 * self.trend['sideways']['ema_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'ema_long_death_cross_weighted_sell_signal'] = \
                1 * self.trend['upwards']['ema_long_death_cross_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['ema_long_death_cross_weighted_sell_signal']

            # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'bollinger_bands_weighted_sell_signal'] = \
                1 * self.trend['downwards']['bollinger_bands_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'bollinger_bands_weighted_sell_signal'] = \
                1 * self.trend['sideways']['bollinger_bands_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'bollinger_bands_weighted_sell_signal'] = \
                1 * self.trend['upwards']['bollinger_bands_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['bollinger_bands_weighted_sell_signal']

            # Weighted Sell Signal: VWAP crosses below current price
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_sell_signal'] = 1 * self.trend['downwards']['vwap_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_sell_signal'] = 1 * self.trend['sideways']['vwap_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'vwap_cross_weighted_sell_signal'] = 1 * self.trend['upwards']['vwap_cross_sell_weight']
            dataframe['total_sell_signal_strength'] += dataframe['vwap_cross_weighted_sell_signal']

        else:
            # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += 1 * self.trend['downwards']['adx_strong_down_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += 1 * self.trend['sideways']['adx_strong_down_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += 1 * self.trend['upwards']['adx_strong_down_sell_weight']

            # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += 1 * self.trend['downwards']['rsi_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += 1 * self.trend['sideways']['rsi_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += 1 * self.trend['upwards']['rsi_sell_weight']

            # Weighted Sell Signal: MACD below Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += 1 * self.trend['downwards']['macd_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += 1 * self.trend['sideways']['macd_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += 1 * self.trend['upwards']['macd_sell_weight']

            # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += 1 * self.trend['downwards'][
                'sma_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += 1 * self.trend['sideways'][
                'sma_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += 1 * self.trend['upwards'][
                'sma_short_death_cross_sell_weight']

            # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += 1 * self.trend['downwards'][
                'ema_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += 1 * self.trend['sideways'][
                'ema_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += 1 * self.trend['upwards'][
                'ema_short_death_cross_sell_weight']

            # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += 1 * self.trend['downwards'][
                'sma_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += 1 * self.trend['sideways'][
                'sma_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += 1 * self.trend['upwards'][
                'sma_long_death_cross_sell_weight']

            # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += 1 * self.trend['downwards'][
                'ema_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += 1 * self.trend['sideways'][
                'ema_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += 1 * self.trend['upwards'][
                'ema_long_death_cross_sell_weight']

            # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                1 * self.trend['downwards']['bollinger_bands_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                1 * self.trend['sideways']['bollinger_bands_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                1 * self.trend['upwards']['bollinger_bands_sell_weight']

            # Weighted Sell Signal: VWAP crosses below current price
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += 1 * self.trend['downwards']['vwap_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += 1 * self.trend['sideways']['vwap_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += 1 * self.trend['upwards']['vwap_cross_sell_weight']

        # Check if sell signal should be sent depending on the current trend
        dataframe.loc[(dataframe['trend'] == 'downwards') &
                      (dataframe['total_sell_signal_strength'] >= self.trend['downwards']['total_sell_signal_needed']),
                      'sell'] = 1
        dataframe.loc[(dataframe['trend'] == 'sideways') &
                      (dataframe['total_sell_signal_strength'] >= self.trend['sideways']['total_sell_signal_needed']),
                      'sell'] = 1
        dataframe.loc[(dataframe['trend'] == 'upwards') &
                      (dataframe['total_sell_signal_strength'] >= self.trend['upwards']['total_sell_signal_needed']),
                      'sell'] = 1

        # Override Sell Signal: When configured sell signals can be completely turned off for each kind of trend
        if not self.trend['downwards']['trade_sells_when_downwards']:
            dataframe.loc[dataframe['trend'] == 'downwards', 'sell'] = 0
        if not self.trend['sideways']['trade_sells_when_sideways']:
            dataframe.loc[dataframe['trend'] == 'sideways', 'sell'] = 0
        if not self.trend['upwards']['trade_sells_when_upwards']:
            dataframe.loc[dataframe['trend'] == 'upwards', 'sell'] = 0

        return dataframe
