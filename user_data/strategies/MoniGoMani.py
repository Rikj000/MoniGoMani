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


class MoniGoMani(IStrategy):
    """
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.4.1 by Rikj000                         ###
    ##                          ----------------------------                          ##
    #               Isn't that what we all want? Our money to go many?                 #
    #               Well that's what this strategy hopes to do for you!                #
    ##       By giving you/hyperopt a lot of signals to alter the weight from         ##
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

    # Buy Signal Weight Influence Table: The idea is to fill in here how heavily you/hyperopt thinks an indicator
    # signals a buy signal compared to the other indicators (Signals can be turned off by allocating 0 or
    # turned into an override by setting them equal to or higher then total_buy_signal_needed)
    adx_buy_weight = 2  # triggers moderately
    bollinger_bands_buy_weight = 27  # triggers moderately
    ema_long_golden_cross_buy_weight = 71  # triggers very infrequently
    ema_short_golden_cross_buy_weight = 9  # triggers infrequently
    macd_buy_weight = 11  # triggers frequently
    plus_minus_direction_buy_weight = 17  # triggers very frequently
    rsi_buy_weight = 46  # triggers infrequently
    sma_long_golden_cross_buy_weight = 0  # triggers very infrequently
    sma_short_golden_cross_buy_weight = 80  # triggers infrequently
    vwap_cross_buy_weight = 63  # triggers infrequently

    # Sell Signal Weight Influence Table: The idea is to fill in here how heavily you/hyperopt thinks an indicator
    # signals a sell signal compared to the other indicators (Signals can be turned off by allocating 0 or
    # turned into an override by setting them equal to or higher then total_sell_signal_needed)
    adx_sell_weight = 25  # triggers moderately
    bollinger_bands_sell_weight = 77  # triggers moderately
    ema_long_death_cross_sell_weight = 36  # triggers very infrequently
    ema_short_death_cross_sell_weight = 17  # triggers very infrequently
    macd_sell_weight = 35  # triggers frequently
    plus_minus_direction_sell_weight = 38  # triggers very frequently
    rsi_sell_weight = 20  # triggers infrequently
    sma_long_death_cross_sell_weight = 4  # triggers very infrequently
    sma_short_death_cross_sell_weight = 66  # triggers very infrequently
    vwap_cross_sell_weight = 50  # triggers infrequently

    # Total Buy/Sell Signal Percentage needed for a signal to be positive: The idea is to fill in here how strong/weak
    # of a total buy/sell signal is needed for the best efficiency, expressed in percentage and hyperoptable
    total_buy_signal_needed = 86
    total_sell_signal_needed = 49

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04

        # "0": 10
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.10

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

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
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
            'tema': {},
            'sar': {'color': 'white'},
        },
        'subplots': {
            # Subplots - each dict defines one additional plot
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
            "RSI": {
                'rsi': {'color': 'red'},
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
            if self.adx_buy_weight > 0:
                dataframe['adx_weighted_buy_signal'] = 0
            if self.adx_sell_weight > 0:
                dataframe['adx_weighted_sell_signal'] = 0
            if self.plus_minus_direction_buy_weight > 0:
                dataframe['plus_minus_weighted_buy_signal'] = 0
            if self.plus_minus_direction_sell_weight > 0:
                dataframe['plus_minus_weighted_sell_signal'] = 0
            if self.rsi_buy_weight > 0:
                dataframe['rsi_weighted_buy_signal'] = 0
            if self.rsi_sell_weight > 0:
                dataframe['rsi_weighted_sell_signal'] = 0
            if self.macd_buy_weight > 0:
                dataframe['macd_weighted_buy_signal'] = 0
            if self.macd_sell_weight > 0:
                dataframe['macd_weighted_sell_signal'] = 0
            if self.sma_short_golden_cross_buy_weight > 0:
                dataframe['sma_short_golden_cross_weighted_buy_signal'] = 0
            if self.sma_short_death_cross_sell_weight > 0:
                dataframe['sma_short_death_cross_weighted_sell_signal'] = 0
            if self.ema_short_golden_cross_buy_weight > 0:
                dataframe['ema_short_golden_cross_weighted_buy_signal'] = 0
            if self.ema_short_death_cross_sell_weight > 0:
                dataframe['ema_short_death_cross_weighted_sell_signal'] = 0
            if self.sma_long_golden_cross_buy_weight > 0:
                dataframe['sma_long_golden_cross_weighted_buy_signal'] = 0
            if self.sma_long_death_cross_sell_weight > 0:
                dataframe['sma_long_death_cross_weighted_sell_signal'] = 0
            if self.ema_long_golden_cross_buy_weight > 0:
                dataframe['ema_long_golden_cross_weighted_buy_signal'] = 0
            if self.ema_long_death_cross_sell_weight > 0:
                dataframe['ema_long_death_cross_weighted_sell_signal'] = 0
            if self.bollinger_bands_buy_weight > 0:
                dataframe['bollinger_bands_weighted_buy_signal'] = 0
            if self.bollinger_bands_sell_weight > 0:
                dataframe['bollinger_bands_weighted_sell_signal'] = 0
            if self.vwap_cross_buy_weight > 0:
                dataframe['vwap_cross_weighted_buy_signal'] = 0
            if self.vwap_cross_sell_weight > 0:
                dataframe['vwap_cross_weighted_sell_signal'] = 0

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

        # If a Weighted Buy Signal goes off => Bullish Indication, Set to true (=1) and multiply by weight percentage

        # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
        if self.adx_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[(dataframe['adx'] > 25) & (dataframe['plus_di'] > dataframe['minus_di']),
                              'adx_weighted_buy_signal'] = 1 * self.adx_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['adx_weighted_buy_signal']
            else:
                dataframe.loc[(dataframe['adx'] > 25) & (dataframe['plus_di'] > dataframe['minus_di']),
                              'total_buy_signal_strength'] += 1 * self.adx_buy_weight

        # Weighted Buy Signal: +DI above -DI (Moving up)
        if self.plus_minus_direction_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[dataframe['plus_di'] > dataframe['minus_di'], 'plus_minus_weighted_buy_signal'] = \
                    1 * self.plus_minus_direction_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['plus_minus_weighted_buy_signal']
            else:
                dataframe.loc[dataframe['plus_di'] > dataframe['minus_di'], 'total_buy_signal_strength'] += \
                    1 * self.plus_minus_direction_buy_weight

        # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
        if self.rsi_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['rsi'], 30), 'rsi_weighted_buy_signal'] = \
                    1 * self.rsi_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['rsi_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['rsi'], 30), 'total_buy_signal_strength'] += \
                    1 * self.rsi_buy_weight

        # Weighted Buy Signal: MACD above Signal
        if self.macd_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[dataframe['macd'] > dataframe['macdsignal'], 'macd_weighted_buy_signal'] = \
                    1 * self.macd_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['macd_weighted_buy_signal']
            else:
                dataframe.loc[dataframe['macd'] > dataframe['macdsignal'], 'total_buy_signal_strength'] += \
                    1 * self.macd_buy_weight

        # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
        if self.sma_short_golden_cross_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['sma9'], dataframe['sma50']),
                              'sma_short_golden_cross_weighted_buy_signal'] = 1 * self.sma_short_golden_cross_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['sma_short_golden_cross_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['sma9'], dataframe['sma50']),
                              'total_buy_signal_strength'] += 1 * self.sma_short_golden_cross_buy_weight

        # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
        if self.ema_short_golden_cross_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['ema9'], dataframe['ema50']),
                              'ema_short_golden_cross_weighted_buy_signal'] = 1 * self.ema_short_golden_cross_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['ema_short_golden_cross_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['ema9'], dataframe['ema50']),
                              'total_buy_signal_strength'] += 1 * self.ema_short_golden_cross_buy_weight

        # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
        if self.sma_long_golden_cross_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['sma50'], dataframe['sma200']),
                              'sma_long_golden_cross_weighted_buy_signal'] = 1 * self.sma_long_golden_cross_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['sma_long_golden_cross_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['sma50'], dataframe['sma200']),
                              'total_buy_signal_strength'] += 1 * self.sma_long_golden_cross_buy_weight

        # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
        if self.ema_long_golden_cross_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['ema50'], dataframe['ema200']),
                              'ema_long_golden_cross_weighted_buy_signal'] = 1 * self.ema_long_golden_cross_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['ema_long_golden_cross_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['ema50'], dataframe['ema200']),
                              'total_buy_signal_strength'] += 1 * self.ema_long_golden_cross_buy_weight

        # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
        # (Candle closes below Upper Bollinger Band)
        if self.bollinger_bands_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['close'], dataframe['bb_lowerband']),
                              'bollinger_bands_weighted_buy_signal'] = 1 * self.bollinger_bands_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['bollinger_bands_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['close'], dataframe['bb_lowerband']),
                              'total_buy_signal_strength'] += 1 * self.bollinger_bands_buy_weight

        # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
        if self.vwap_cross_buy_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_above(dataframe['vwap'], dataframe['close']),
                              'vwap_cross_weighted_buy_signal'] = 1 * self.vwap_cross_buy_weight
                dataframe['total_buy_signal_strength'] += dataframe['vwap_cross_weighted_buy_signal']
            else:
                dataframe.loc[qtpylib.crossed_above(dataframe['vwap'], dataframe['close']),
                              'total_buy_signal_strength'] += 1 * self.vwap_cross_buy_weight

        # Check if buy signal should be sent
        dataframe.loc[(dataframe['total_buy_signal_strength'] >= self.total_buy_signal_needed), 'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """

        # If a Weighted Sell Signal goes off => Bearish Indication, Set to true (=1) and multiply by weight percentage

        # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
        if self.adx_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[(dataframe['adx'] > 25) & (dataframe['plus_di'] < dataframe['minus_di']),
                              'adx_weighted_sell_signal'] = 1 * self.adx_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['adx_weighted_sell_signal']
            else:
                dataframe.loc[(dataframe['adx'] > 25) & (dataframe['plus_di'] < dataframe['minus_di']),
                              'total_sell_signal_strength'] += 1 * self.adx_sell_weight

        # Weighted Sell Signal: ADX below 20 (The trend is weak or trend-less,
        # WARNING, no indication of up or down!
        # dataframe.loc[dataframe['adx'] < 20, 'adx_weighted_sell_signal'] = \
        #     1 * self.adx_sell_weight

        # Weighted Sell Signal: +DI below -DI (Moving Down)
        if self.plus_minus_direction_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[dataframe['plus_di'] < dataframe['minus_di'], 'plus_minus_weighted_sell_signal'] = \
                    1 * self.plus_minus_direction_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['plus_minus_weighted_sell_signal']
            else:
                dataframe.loc[dataframe['plus_di'] < dataframe['minus_di'], 'total_sell_signal_strength'] += \
                    1 * self.plus_minus_direction_sell_weight

        # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
        if self.rsi_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['rsi'], 70), 'rsi_weighted_sell_signal'] = \
                    1 * self.rsi_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['rsi_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['rsi'], 70), 'total_sell_signal_strength'] += \
                    1 * self.rsi_sell_weight

        # Weighted Sell Signal: MACD below Signal
        if self.macd_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[dataframe['macd'] < dataframe['macdsignal'], 'macd_weighted_sell_signal'] = \
                    1 * self.macd_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['macd_weighted_sell_signal']
            else:
                dataframe.loc[dataframe['macd'] < dataframe['macdsignal'], 'total_sell_signal_strength'] += \
                    1 * self.macd_sell_weight

        # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
        if self.sma_short_death_cross_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['sma9'], dataframe['sma50']),
                              'sma_short_death_cross_weighted_sell_signal'] = 1 * self.sma_short_death_cross_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['sma_short_death_cross_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['sma9'], dataframe['sma50']),
                              'total_sell_signal_strength'] += 1 * self.sma_short_death_cross_sell_weight

        # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
        if self.ema_short_death_cross_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['ema9'], dataframe['ema50']),
                              'ema_short_death_cross_weighted_sell_signal'] = 1 * self.ema_short_death_cross_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['ema_short_death_cross_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['ema9'], dataframe['ema50']),
                              'total_sell_signal_strength'] += 1 * self.ema_short_death_cross_sell_weight

        # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
        if self.sma_long_death_cross_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['sma50'], dataframe['sma200']),
                              'sma_long_death_cross_weighted_sell_signal'] = 1 * self.sma_long_death_cross_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['sma_long_death_cross_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['sma50'], dataframe['sma200']),
                              'total_sell_signal_strength'] += 1 * self.sma_long_death_cross_sell_weight

        # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
        if self.ema_long_death_cross_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['ema50'], dataframe['ema200']),
                              'ema_long_death_cross_weighted_sell_signal'] = 1 * self.ema_long_death_cross_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['ema_long_death_cross_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['ema50'], dataframe['ema200']),
                              'total_sell_signal_strength'] += 1 * self.ema_long_death_cross_sell_weight

        # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
        # (Candle closes below Upper Bollinger Band)
        if self.bollinger_bands_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['close'], dataframe['bb_upperband']),
                              'bollinger_bands_weighted_sell_signal'] = 1 * self.bollinger_bands_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['bollinger_bands_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['close'], dataframe['bb_upperband']),
                              'total_sell_signal_strength'] += 1 * self.bollinger_bands_sell_weight

        # Weighted Sell Signal: VWAP crosses below current price
        if self.vwap_cross_sell_weight > 0:
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[qtpylib.crossed_below(dataframe['vwap'], dataframe['close']),
                              'vwap_cross_weighted_sell_signal'] = 1 * self.vwap_cross_sell_weight
                dataframe['total_sell_signal_strength'] += dataframe['vwap_cross_weighted_sell_signal']
            else:
                dataframe.loc[qtpylib.crossed_below(dataframe['vwap'], dataframe['close']),
                              'total_sell_signal_strength'] += 1 * self.vwap_cross_sell_weight

        # Check if sell signal should be sent
        dataframe.loc[(dataframe['total_sell_signal_strength'] >= self.total_sell_signal_needed), 'sell'] = 1
        return dataframe
