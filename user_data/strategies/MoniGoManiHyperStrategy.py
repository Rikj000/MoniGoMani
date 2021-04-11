# --- Do not remove these libs ----------------------------------------------------------------------
import numpy as np  # noqa
import pandas as pd  # noqa
import talib.abstract as ta
from pandas import DataFrame
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy import IStrategy, CategoricalParameter, IntParameter
import logging


# ^ TA-Lib Autofill mostly broken in JetBrains Products,
# ta._ta_lib.<function_name> can temporarily be used while writing as a workaround
# Then change back to ta.<function_name> so IDE won't nag about accessing a protected member of TA-Lib
# ----------------------------------------------------------------------------------------------------


class Signal:
    optimize = True
    min_value = 0
    max_value = 100
    default_value = 0
    type = ''
    name = ''

    def __init__(self, name: str, test, overridable: bool = True, min_value: int = 0, max_value: int = 100,
                 default_value: int = 0):
        self.optimize = overridable
        self.min_value = min_value
        self.max_value = max_value
        self.test = test
        self.default_value = default_value
        self.name = name


class BuySignal(Signal):
    type = 'buy'
    pass


class SellSignal(Signal):
    type = 'sell'
    pass


class MoniGoManiHyperStrategy(IStrategy):
    """
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.8.1 by Rikj000                         ###
    ##                          ----------------------------                          ##
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
    """

    # If enabled all Weighted Signal results will be added to the dataframe for easy debugging with BreakPoints
    # Warning: Disable this for anything else then debugging in an IDE! (Integrated Development Environment)
    debuggable_weighted_signal_dataframe = False

    sell_unclogger_enabled = False

    # Ps: Documentation has been moved to the Buy/Sell HyperOpt Space Parameters sections below this copy-paste section
    ####################################################################################################################
    #                                    START OF HYPEROPT RESULTS COPY-PASTE SECTION                                  #
    ####################################################################################################################

    # Buy hyperspace params:
    buy_params = {
        'buy___trades_when_downwards': True,
        'buy___trades_when_sideways': False,
        'buy___trades_when_upwards': True,
        'buy__downwards_trend_total_signal_needed': 4,
        'buy__sideways_trend_total_signal_needed': 17,
        'buy__upwards_trend_total_signal_needed': 50,
        'buy_downwards_trend_adx_strong_up_weight': 71,
        'buy_downwards_trend_bollinger_bands_weight': 54,
        'buy_downwards_trend_ema_long_golden_cross_weight': 0,
        'buy_downwards_trend_ema_short_golden_cross_weight': 87,
        'buy_downwards_trend_macd_weight': 47,
        'buy_downwards_trend_rsi_weight': 62,
        'buy_downwards_trend_sma_long_golden_cross_weight': 56,
        'buy_downwards_trend_sma_short_golden_cross_weight': 46,
        'buy_downwards_trend_vwap_cross_weight': 44,
        'buy_sideways_trend_adx_strong_up_weight': 65,
        'buy_sideways_trend_bollinger_bands_weight': 25,
        'buy_sideways_trend_ema_long_golden_cross_weight': 74,
        'buy_sideways_trend_ema_short_golden_cross_weight': 59,
        'buy_sideways_trend_macd_weight': 64,
        'buy_sideways_trend_rsi_weight': 52,
        'buy_sideways_trend_sma_long_golden_cross_weight': 4,
        'buy_sideways_trend_sma_short_golden_cross_weight': 86,
        'buy_sideways_trend_vwap_cross_weight': 57,
        'buy_upwards_trend_adx_strong_up_weight': 13,
        'buy_upwards_trend_bollinger_bands_weight': 21,
        'buy_upwards_trend_ema_long_golden_cross_weight': 71,
        'buy_upwards_trend_ema_short_golden_cross_weight': 12,
        'buy_upwards_trend_macd_weight': 94,
        'buy_upwards_trend_rsi_weight': 24,
        'buy_upwards_trend_sma_long_golden_cross_weight': 14,
        'buy_upwards_trend_sma_short_golden_cross_weight': 26,
        'buy_upwards_trend_vwap_cross_weight': 23
    }

    # Sell hyperspace params:
    sell_params = {
        'sell___trades_when_downwards': True,
        'sell___trades_when_sideways': True,
        'sell___trades_when_upwards': False,
        'sell__downwards_trend_total_signal_needed': 87,
        'sell__sideways_trend_total_signal_needed': 22,
        'sell__upwards_trend_total_signal_needed': 89,
        'sell_downwards_trend_adx_strong_down_weight': 34,
        'sell_downwards_trend_bollinger_bands_weight': 83,
        'sell_downwards_trend_ema_long_death_cross_weight': 0,
        'sell_downwards_trend_ema_short_death_cross_weight': 42,
        'sell_downwards_trend_macd_weight': 0,
        'sell_downwards_trend_rsi_weight': 49,
        'sell_downwards_trend_sma_long_death_cross_weight': 40,
        'sell_downwards_trend_sma_short_death_cross_weight': 0,
        'sell_downwards_trend_vwap_cross_weight': 12,
        'sell_sideways_trend_adx_strong_down_weight': 45,
        'sell_sideways_trend_bollinger_bands_weight': 94,
        'sell_sideways_trend_ema_long_death_cross_weight': 8,
        'sell_sideways_trend_ema_short_death_cross_weight': 33,
        'sell_sideways_trend_macd_weight': 65,
        'sell_sideways_trend_rsi_weight': 11,
        'sell_sideways_trend_sma_long_death_cross_weight': 57,
        'sell_sideways_trend_sma_short_death_cross_weight': 23,
        'sell_sideways_trend_vwap_cross_weight': 55,
        'sell_upwards_trend_adx_strong_down_weight': 54,
        'sell_upwards_trend_bollinger_bands_weight': 0,
        'sell_upwards_trend_ema_long_death_cross_weight': 36,
        'sell_upwards_trend_ema_short_death_cross_weight': 12,
        'sell_upwards_trend_macd_weight': 90,
        'sell_upwards_trend_rsi_weight': 52,
        'sell_upwards_trend_sma_long_death_cross_weight': 97,
        'sell_upwards_trend_sma_short_death_cross_weight': 18,
        'sell_upwards_trend_vwap_cross_weight': 51
    }

    # ROI table:
    minimal_roi = {
        "0": 0.38648,
        "335": 0.15347,
        "674": 0.05148,
        "1928": 0
    }

    # Stoploss:
    stoploss = -0.34755

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01156
    trailing_stop_positive_offset = 0.02329
    trailing_only_offset_is_reached = True

    ####################################################################################################################
    #                                     END OF HYPEROPT RESULTS COPY-PASTE SECTION                                   #
    ####################################################################################################################

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
    # Override to 0:        IntParameter(0, 100, default=0, space='sell', optimize=False, load=False)
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
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=True)
    buy___trades_when_sideways = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=True)
    buy___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=True)

    # Total Buy Signal Percentage needed for a signal to be positive
    buy__downwards_trend_total_signal_needed = IntParameter(0, 100, default=65, space='buy', optimize=True, load=True)

    # Total Buy Signal Percentage needed for a signal to be positive
    buy__sideways_trend_total_signal_needed = IntParameter(0, 100, default=65, space='buy', optimize=True, load=True)

    # Total Buy Signal Percentage needed for a signal to be positive
    buy__upwards_trend_total_signal_needed = IntParameter(0, 100, default=65, space='buy', optimize=True, load=True)

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
        CategoricalParameter([True, False], default=True, space='sell', optimize=True, load=True)
    sell___trades_when_sideways = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=True, load=True)
    sell___trades_when_upwards = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=True, load=True)

    # Total Sell Signal Percentage needed for a signal to be positive
    sell__downwards_trend_total_signal_needed = IntParameter(0, 100, default=65, space='sell', optimize=True, load=True)

    # Total Sell Signal Percentage needed for a signal to be positive
    sell__sideways_trend_total_signal_needed = IntParameter(0, 100, default=65, space='sell', optimize=True, load=True)

    # Total Sell Signal Percentage needed for a signal to be positive
    sell__upwards_trend_total_signal_needed = IntParameter(0, 100, default=65, space='sell', optimize=True, load=True)

    # ---------------------------------------------------------------- #
    #                 Custom HyperOpt Space Parameters                 #
    # ---------------------------------------------------------------- #

    # Signal hyperopt is configurable by changing Signal object
    # Signal(lambda df: True, overridable=False, min_value=0, max_value=100)

    buy_signals = [
        BuySignal('adx_strong_up', lambda df: df['adx'] > 25, overridable=True, min_value=0, max_value=100, default_value=65),
        BuySignal('adx_strong_up', lambda df: df['adx'] > 25),
        BuySignal('rsi', lambda df: qtpylib.crossed_above(df['rsi'], 30)),
        BuySignal('macd', lambda df: df['macd'] > df['macdsignal']),
        BuySignal('sma_short_golden_cross', lambda df: qtpylib.crossed_above(df['sma9'], df['sma50'])),
        BuySignal('ema_short_golden_cross', lambda df: qtpylib.crossed_above(df['ema9'], df['ema50'])),
        BuySignal('sma_long_golden_cross', lambda df: qtpylib.crossed_above(df['sma50'], df['sma200'])),
        BuySignal('ema_long_golden_cross', lambda df: qtpylib.crossed_above(df['ema50'], df['ema200'])),
        BuySignal('bollinger_bands', lambda df: qtpylib.crossed_above(df['close'], df['bb_lowerband'])),
        BuySignal('vwap_cross', lambda df: qtpylib.crossed_above(df['vwap'], df['close'])),
    ]

    sell_signals = [
        SellSignal('adx_strong_down', lambda df: df['adx'] > 25),
        SellSignal('rsi', lambda df: qtpylib.crossed_below(df['rsi'], 30)),
        SellSignal('macd', lambda df: df['macd'] < df['macdsignal']),
        SellSignal('sma_short_death_cross', lambda df: qtpylib.crossed_below(df['sma9'], df['sma50'])),
        SellSignal('ema_short_death_cross', lambda df: qtpylib.crossed_below(df['ema9'], df['ema50'])),
        SellSignal('sma_long_death_cross', lambda df: qtpylib.crossed_below(df['sma50'], df['sma200'])),
        SellSignal('ema_long_death_cross', lambda df: qtpylib.crossed_below(df['ema50'], df['ema200'])),
        SellSignal('bollinger_bands', lambda df: qtpylib.crossed_below(df['close'], df['bb_lowerband'])),
        SellSignal('vwap_cross', lambda df: qtpylib.crossed_below(df['vwap'], df['close'])),
    ]

    trends = ['upwards', 'sideways', 'downwards']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Add loading parameter values from json
        logger = logging.getLogger(__name__)

        # buy_weight_names = self.buy_signals.keys()
        for trend in self.trends:
            for signal in [*self.buy_signals, *self.sell_signals]:
                logger.info(signal.name)
                setattr(self, f"{signal.type}_{trend}_trend_{signal.name}_weight",
                        IntParameter(
                            signal.min_value,
                            signal.max_value,
                            default=signal.default_value,
                            space=signal.type,
                            optimize=signal.optimize,
                            load=True))

    def generate_buy_config(self, signals: list) -> dict:
        config = {}
        for signal in signals:
            config[signal] = self.generate_config_for(signal.name, signal.test, 'buy')
        return config

    def generate_sell_config(self, signals: list) -> dict:
        config = {}
        for signal in signals:
            config[signal] = self.generate_config_for(signal.name, signal.test, 'sell')
        return config

    def generate_config_for(self, signal: str, test, param_space: str) -> dict:
        return {
            'test': test,
            'trend_weights': self.generate_weight_table_for(signal, param_space),
            'debug_param': f'{signal}_weighted_{param_space}_signal'
        }

    def generate_weight_table_for(self, signal: str, param_space: str) -> dict:
        data = {}
        for trend in self.trends:
            data[trend] = getattr(self, f'{param_space}_{trend}_trend_{signal}_weight').value
        return data

    @staticmethod
    def generate_weight_column(dataframe: DataFrame, signal: dict):
        return dataframe['trend'].map(signal['trend_weights'])

    def calculate_signal_strength(self, dataframe: DataFrame, config: dict):
        for signal in config.values():
            weight_column = self.generate_weight_column(dataframe, signal)
            if self.debuggable_weighted_signal_dataframe:
                dataframe.loc[signal['test'](dataframe), signal['debug_param']] = weight_column
                dataframe['total_buy_signal_strength'] += dataframe[signal['debug_param']]
            else:
                dataframe.loc[signal['test'](dataframe), 'total_buy_signal_strength'] += weight_column
        return dataframe

    # class HyperOpt:
    #     # Define a custom stoploss space.
    #     @staticmethod
    #     def stoploss_space():
    #         return [RealParameter(-0.01, -0.35, name='stoploss')]

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

        # Trend Detection
        # ---------------

        # Detect if current trend going Downwards / Sideways / Upwards, strategy will respond accordingly
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
        dataframe.loc[dataframe['adx'] < 20, 'trend'] = 'sideways'
        dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        config = self.generate_buy_config(self.buy_signals)
        dataframe = self.calculate_signal_strength(dataframe, config)

        dataframe.loc[
            (
                    (dataframe['trend'] == 'downwards') &
                    (dataframe['total_buy_signal_strength'] >= self.buy__downwards_trend_total_signal_needed.value)
            ) | (
                    (dataframe['trend'] == 'sideways') &
                    (dataframe['total_buy_signal_strength'] >= self.buy__sideways_trend_total_signal_needed.value)
            ) | (
                    (dataframe['trend'] == 'upwards') &
                    (dataframe['total_buy_signal_strength'] >= self.buy__upwards_trend_total_signal_needed.value)
            ), 'buy'] = 1

        # Override Buy Signal: When configured buy signals can be completely turned off for each kind of trend
        if not self.buy___trades_when_downwards.value:
            dataframe.loc[dataframe['trend'] == 'downwards', 'buy'] = 0
        if not self.buy___trades_when_sideways.value:
            dataframe.loc[dataframe['trend'] == 'sideways', 'buy'] = 0
        if not self.buy___trades_when_upwards.value:
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
        config = self.generate_sell_config(self.sell_signals)
        dataframe = self.calculate_signal_strength(dataframe, config)

        # Check if sell signal should be sent depending on the current trend
        dataframe.loc[
            (
                    (dataframe['trend'] == 'downwards') &
                    (dataframe['total_sell_signal_strength'] >= self.sell__downwards_trend_total_signal_needed.value)
            ) | (
                    (dataframe['trend'] == 'sideways') &
                    (dataframe['total_sell_signal_strength'] >= self.sell__sideways_trend_total_signal_needed.value)
            ) | (
                    (dataframe['trend'] == 'upwards') &
                    (dataframe['total_sell_signal_strength'] >= self.sell__upwards_trend_total_signal_needed.value)
            ), 'sell'] = 1

        # Override Sell Signal: When configured sell signals can be completely turned off for each kind of trend
        if not self.sell___trades_when_downwards.value:
            dataframe.loc[dataframe['trend'] == 'downwards', 'sell'] = 0
        if not self.sell___trades_when_sideways.value:
            dataframe.loc[dataframe['trend'] == 'sideways', 'sell'] = 0
        if not self.sell___trades_when_upwards.value:
            dataframe.loc[dataframe['trend'] == 'upwards', 'sell'] = 0

        return dataframe