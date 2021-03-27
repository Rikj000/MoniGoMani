# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
# Add your lib to import here
import talib.abstract as ta  # noqa
import freqtrade.vendor.qtpylib.indicators as qtpylib


class MoniGoManiHyperOpt(IHyperOpt):
    """
    ####################################################################################
    ####                                                                            ####
    ###                  MoniGoManiHyperOpt for v0.4.1 by Rikj000                    ###
    ####                                                                            ####
    ####################################################################################

    You should:
    - Add any lib you need to build your hyperopt.

    You must keep:
    - The prototypes for the methods: populate_indicators, indicator_space, buy_strategy_generator.

    The methods roi_space, generate_roi_table and stoploss_space are not required
    and are provided by default.
    However, you may override them if you need 'roi' and 'stoploss' spaces that
    differ from the defaults offered by Freqtrade.
    Sample implementation of these methods will be copied to `user_data/hyperopts` when
    creating the user-data directory using `freqtrade create-userdir --userdir user_data`,
    or is available online under the following URL:
    https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_hyperopt_advanced.py.
    """

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_total_buy_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='adx_buy_weight'),
            Integer(0, 100, name='plus_minus_direction_buy_weight'),
            Integer(0, 100, name='rsi_buy_weight'),
            Integer(0, 100, name='macd_buy_weight'),
            Integer(0, 100, name='sma_short_golden_cross_buy_weight'),
            Integer(0, 100, name='ema_short_golden_cross_buy_weight'),
            Integer(0, 100, name='sma_long_golden_cross_buy_weight'),
            Integer(0, 100, name='ema_long_golden_cross_buy_weight'),
            Integer(0, 100, name='bollinger_bands_buy_weight'),
            Integer(0, 100, name='vwap_cross_buy_weight')
        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by Hyperopt.
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use.
            """

            # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
            if params['adx_buy_weight'] > 0:
                dataframe.loc[(dataframe['adx'] > 25) & (dataframe['plus_di'] > dataframe['minus_di']),
                              'total_buy_signal_strength'] += 1 * params['adx_buy_weight']

            # Weighted Buy Signal: +DI above -DI (Moving up)
            if params['plus_minus_direction_buy_weight'] > 0:
                dataframe.loc[dataframe['plus_di'] > dataframe['minus_di'], 'total_buy_signal_strength'] += \
                    1 * params['plus_minus_direction_buy_weight']

            # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
            if params['rsi_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['rsi'], 30), 'total_buy_signal_strength'] += \
                    1 * params['rsi_buy_weight']

            # Weighted Buy Signal: MACD above Signal
            if params['macd_buy_weight'] > 0:
                dataframe.loc[dataframe['macd'] > dataframe['macdsignal'], 'total_buy_signal_strength'] += \
                    1 * params['macd_buy_weight']

            # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
            if params['sma_short_golden_cross_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['sma9'], dataframe['sma50']),
                              'total_buy_signal_strength'] += 1 * params['sma_short_golden_cross_buy_weight']

            # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
            if params['ema_short_golden_cross_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['ema9'], dataframe['ema50']),
                              'total_buy_signal_strength'] += 1 * params['ema_short_golden_cross_buy_weight']

            # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
            if params['sma_long_golden_cross_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['sma50'], dataframe['sma200']),
                              'total_buy_signal_strength'] += 1 * params['sma_long_golden_cross_buy_weight']

            # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
            if params['ema_long_golden_cross_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['ema50'], dataframe['ema200']),
                              'total_buy_signal_strength'] += 1 * params['ema_long_golden_cross_buy_weight']

            # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
            # (Candle closes below Upper Bollinger Band)
            if params['bollinger_bands_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['close'], dataframe['bb_lowerband']),
                              'total_buy_signal_strength'] += 1 * params['bollinger_bands_buy_weight']

            # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
            if params['vwap_cross_buy_weight'] > 0:
                dataframe.loc[qtpylib.crossed_above(dataframe['vwap'], dataframe['close']),
                              'total_buy_signal_strength'] += 1 * params['vwap_cross_buy_weight']

            # Check if buy signal should be sent
            dataframe.loc[(dataframe['total_buy_signal_strength'] >= params['_total_buy_signal_needed']), 'buy'] = 1
            return dataframe

        return populate_buy_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            # Total Sell Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_total_sell_signal_needed'),
            # Sell Signal Weight Influence Table
            Integer(0, 100, name='adx_sell_weight'),
            Integer(0, 100, name='plus_minus_direction_sell_weight'),
            Integer(0, 100, name='rsi_sell_weight'),
            Integer(0, 100, name='macd_sell_weight'),
            Integer(0, 100, name='sma_short_death_cross_sell_weight'),
            Integer(0, 100, name='ema_short_death_cross_sell_weight'),
            Integer(0, 100, name='sma_long_death_cross_sell_weight'),
            Integer(0, 100, name='ema_long_death_cross_sell_weight'),
            Integer(0, 100, name='bollinger_bands_sell_weight'),
            Integer(0, 100, name='vwap_cross_sell_weight')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
            if params['adx_sell_weight'] > 0:
                dataframe.loc[(dataframe['adx'] > 25) & (dataframe['plus_di'] < dataframe['minus_di']),
                              'total_sell_signal_strength'] += 1 * params['adx_sell_weight']

            # Weighted Sell Signal: +DI below -DI (Moving Down)
            if params['plus_minus_direction_sell_weight'] > 0:
                dataframe.loc[dataframe['plus_di'] < dataframe['minus_di'], 'total_sell_signal_strength'] += \
                    1 * params['plus_minus_direction_sell_weight']

            # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
            if params['rsi_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['rsi'], 70), 'total_sell_signal_strength'] += \
                    1 * params['rsi_sell_weight']

            # Weighted Sell Signal: MACD below Signal
            if params['macd_sell_weight'] > 0:
                dataframe.loc[dataframe['macd'] < dataframe['macdsignal'], 'total_sell_signal_strength'] += \
                    1 * params['macd_sell_weight']

            # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
            if params['sma_short_death_cross_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['sma9'], dataframe['sma50']),
                              'total_sell_signal_strength'] += 1 * params['sma_short_death_cross_sell_weight']

            # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
            if params['ema_short_death_cross_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['ema9'], dataframe['ema50']),
                              'total_sell_signal_strength'] += 1 * params['ema_short_death_cross_sell_weight']

            # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
            if params['sma_long_death_cross_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['sma50'], dataframe['sma200']),
                              'total_sell_signal_strength'] += 1 * params['sma_long_death_cross_sell_weight']

            # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
            if params['ema_long_death_cross_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['ema50'], dataframe['ema200']),
                              'total_sell_signal_strength'] += 1 * params['ema_long_death_cross_sell_weight']

            # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
            # (Candle closes below Upper Bollinger Band)
            if params['bollinger_bands_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['close'], dataframe['bb_upperband']),
                              'total_sell_signal_strength'] += 1 * params['bollinger_bands_sell_weight']

            # Weighted Sell Signal: VWAP crosses below current price
            if params['vwap_cross_sell_weight'] > 0:
                dataframe.loc[qtpylib.crossed_below(dataframe['vwap'], dataframe['close']),
                              'total_sell_signal_strength'] += 1 * params['vwap_cross_sell_weight']

            # Check if sell signal should be sent
            dataframe.loc[(dataframe['total_sell_signal_strength'] >= params['_total_sell_signal_needed']), 'sell'] = 1
            return dataframe

        return populate_sell_trend
