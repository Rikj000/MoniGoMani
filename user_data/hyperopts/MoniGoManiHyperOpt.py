# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
# --------------------------------
# Add your lib to import here
import talib.abstract as ta  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


class MoniGoManiHyperOpt(IHyperOpt):
    """
    ####################################################################################
    ####                                                                            ####
    ###                  MoniGoManiHyperOpt for v0.6.4 by Rikj000                    ###
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
            # Decide on which kinds of trends the bot should trade or hold
            Categorical([True, False], name='.trade_buys_when_downwards'),
            Categorical([True, False], name='.trade_buys_when_sideways'),
            Categorical([True, False], name='.trade_buys_when_upwards'),
            # Downwards Trend
            # ------------
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_downwards_trend_total_buy_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='downwards_trend_adx_strong_up_buy_weight'),
            Integer(0, 100, name='downwards_trend_rsi_buy_weight'),
            Integer(0, 100, name='downwards_trend_macd_buy_weight'),
            Integer(0, 100, name='downwards_trend_sma_short_golden_cross_buy_weight'),
            Integer(0, 100, name='downwards_trend_ema_short_golden_cross_buy_weight'),
            Integer(0, 100, name='downwards_trend_sma_long_golden_cross_buy_weight'),
            Integer(0, 100, name='downwards_trend_ema_long_golden_cross_buy_weight'),
            Integer(0, 100, name='downwards_trend_bollinger_bands_buy_weight'),
            Integer(0, 100, name='downwards_trend_vwap_cross_buy_weight'),
            # Sideways Trend
            # ------------
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_sideways_trend_total_buy_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='sideways_trend_adx_strong_up_buy_weight'),
            Integer(0, 100, name='sideways_trend_rsi_buy_weight'),
            Integer(0, 100, name='sideways_trend_macd_buy_weight'),
            Integer(0, 100, name='sideways_trend_sma_short_golden_cross_buy_weight'),
            Integer(0, 100, name='sideways_trend_ema_short_golden_cross_buy_weight'),
            Integer(0, 100, name='sideways_trend_sma_long_golden_cross_buy_weight'),
            Integer(0, 100, name='sideways_trend_ema_long_golden_cross_buy_weight'),
            Integer(0, 100, name='sideways_trend_bollinger_bands_buy_weight'),
            Integer(0, 100, name='sideways_trend_vwap_cross_buy_weight'),
            # Upwards Trend
            # ------------
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_upwards_trend_total_buy_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='upwards_trend_adx_strong_up_buy_weight'),
            Integer(0, 100, name='upwards_trend_rsi_buy_weight'),
            Integer(0, 100, name='upwards_trend_macd_buy_weight'),
            Integer(0, 100, name='upwards_trend_sma_short_golden_cross_buy_weight'),
            Integer(0, 100, name='upwards_trend_ema_short_golden_cross_buy_weight'),
            Integer(0, 100, name='upwards_trend_sma_long_golden_cross_buy_weight'),
            Integer(0, 100, name='upwards_trend_ema_long_golden_cross_buy_weight'),
            Integer(0, 100, name='upwards_trend_bollinger_bands_buy_weight'),
            Integer(0, 100, name='upwards_trend_vwap_cross_buy_weight')
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

            # Detect if current trend going Downwards / Sideways / Upwards, strategy will respond accordingly
            dataframe.loc[(dataframe['adx'] > 20) &
                          (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
            dataframe.loc[dataframe['adx'] < 20, 'trend'] = 'sideways'
            dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

            # If a Weighted Buy Signal goes off => Bullish Indication, Set to true (=1) and multiply by weight
            # percentage

            # Weighted Buy Signal: ADX above 25 & +DI above -DI (The trend has strength while moving up)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += 1 * params['downwards_trend_adx_strong_up_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += 1 * params['sideways_trend_adx_strong_up_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'total_buy_signal_strength'] += 1 * params['upwards_trend_adx_strong_up_buy_weight']

            # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += 1 * params['downwards_trend_rsi_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += 1 * params['sideways_trend_rsi_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['rsi'], 30),
                          'total_buy_signal_strength'] += 1 * params['upwards_trend_rsi_buy_weight']

            # Weighted Buy Signal: MACD above Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += 1 * params['downwards_trend_macd_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += 1 * params['sideways_trend_macd_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] > dataframe['macdsignal']),
                          'total_buy_signal_strength'] += 1 * params['upwards_trend_macd_buy_weight']

            # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += \
                1 * params['downwards_trend_sma_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += \
                1 * params['sideways_trend_sma_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma9'], dataframe[
                'sma50']), 'total_buy_signal_strength'] += \
                1 * params['upwards_trend_sma_short_golden_cross_buy_weight']

            # Weighted Buy Signal: EMA short term Golden Cross (Short term EMA crosses above Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += \
                1 * params['downwards_trend_ema_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += \
                1 * params['sideways_trend_ema_short_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema9'], dataframe[
                'ema50']), 'total_buy_signal_strength'] += \
                1 * params['upwards_trend_ema_short_golden_cross_buy_weight']

            # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += \
                1 * params['downwards_trend_sma_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += \
                1 * params['sideways_trend_sma_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['sma50'], dataframe[
                'sma200']), 'total_buy_signal_strength'] += \
                1 * params['upwards_trend_sma_long_golden_cross_buy_weight']

            # Weighted Buy Signal: EMA long term Golden Cross (Medium term EMA crosses above Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += \
                1 * params['downwards_trend_ema_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += \
                1 * params['sideways_trend_ema_long_golden_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['ema50'], dataframe[
                'ema200']), 'total_buy_signal_strength'] += \
                1 * params['upwards_trend_ema_long_golden_cross_buy_weight']

            # Weighted Buy Signal: Re-Entering Lower Bollinger Band after downward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += \
                1 * params['downwards_trend_bollinger_bands_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += \
                1 * params['sideways_trend_bollinger_bands_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['close'], dataframe[
                'bb_lowerband']), 'total_buy_signal_strength'] += \
                1 * params['upwards_trend_bollinger_bands_buy_weight']

            # Weighted Buy Signal: VWAP crosses above current price (Simultaneous rapid increase in volume and price)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += 1 * params['downwards_trend_vwap_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += 1 * params['sideways_trend_vwap_cross_buy_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_above(dataframe['vwap'], dataframe[
                'close']), 'total_buy_signal_strength'] += 1 * params['upwards_trend_vwap_cross_buy_weight']

            # Check if buy signal should be sent depending on the current trend
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['total_buy_signal_strength'] >= params[
                '_downwards_trend_total_buy_signal_needed']), 'buy'] = 1
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['total_buy_signal_strength'] >= params[
                '_sideways_trend_total_buy_signal_needed']), 'buy'] = 1
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['total_buy_signal_strength'] >= params[
                '_upwards_trend_total_buy_signal_needed']), 'buy'] = 1

            # Override Buy Signal: When configured buy signals can be completely turned off for each kind of trend
            if not params['.trade_buys_when_downwards']:
                dataframe.loc[dataframe['trend'] == 'downwards', 'buy'] = 0
            if not params['.trade_buys_when_sideways']:
                dataframe.loc[dataframe['trend'] == 'sideways', 'buy'] = 0
            if not params['.trade_buys_when_upwards']:
                dataframe.loc[dataframe['trend'] == 'upwards', 'buy'] = 0

            return dataframe

        return populate_buy_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            # Decide on which kinds of trends the bot should trade or hold
            Categorical([True, False], name='.trade_sells_when_downwards'),
            Categorical([True, False], name='.trade_sells_when_sideways'),
            Categorical([True, False], name='.trade_sells_when_upwards'),
            # Downwards Trend
            # ------------
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_downwards_trend_total_sell_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='downwards_trend_adx_strong_down_sell_weight'),
            Integer(0, 100, name='downwards_trend_rsi_sell_weight'),
            Integer(0, 100, name='downwards_trend_macd_sell_weight'),
            Integer(0, 100, name='downwards_trend_sma_short_death_cross_sell_weight'),
            Integer(0, 100, name='downwards_trend_ema_short_death_cross_sell_weight'),
            Integer(0, 100, name='downwards_trend_sma_long_death_cross_sell_weight'),
            Integer(0, 100, name='downwards_trend_ema_long_death_cross_sell_weight'),
            Integer(0, 100, name='downwards_trend_bollinger_bands_sell_weight'),
            Integer(0, 100, name='downwards_trend_vwap_cross_sell_weight'),
            # Sideways Trend
            # ------------
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_sideways_trend_total_sell_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='sideways_trend_adx_strong_down_sell_weight'),
            Integer(0, 100, name='sideways_trend_rsi_sell_weight'),
            Integer(0, 100, name='sideways_trend_macd_sell_weight'),
            Integer(0, 100, name='sideways_trend_sma_short_death_cross_sell_weight'),
            Integer(0, 100, name='sideways_trend_ema_short_death_cross_sell_weight'),
            Integer(0, 100, name='sideways_trend_sma_long_death_cross_sell_weight'),
            Integer(0, 100, name='sideways_trend_ema_long_death_cross_sell_weight'),
            Integer(0, 100, name='sideways_trend_bollinger_bands_sell_weight'),
            Integer(0, 100, name='sideways_trend_vwap_cross_sell_weight'),
            # Upwards Trend
            # ------------
            # Total Buy Signal Percentage needed for a signal to be positive
            Integer(0, 100, name='_upwards_trend_total_sell_signal_needed'),
            # Buy Signal Weight Influence Table
            Integer(0, 100, name='upwards_trend_adx_strong_down_sell_weight'),
            Integer(0, 100, name='upwards_trend_rsi_sell_weight'),
            Integer(0, 100, name='upwards_trend_macd_sell_weight'),
            Integer(0, 100, name='upwards_trend_sma_short_death_cross_sell_weight'),
            Integer(0, 100, name='upwards_trend_ema_short_death_cross_sell_weight'),
            Integer(0, 100, name='upwards_trend_sma_long_death_cross_sell_weight'),
            Integer(0, 100, name='upwards_trend_ema_long_death_cross_sell_weight'),
            Integer(0, 100, name='upwards_trend_bollinger_bands_sell_weight'),
            Integer(0, 100, name='upwards_trend_vwap_cross_sell_weight')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            # Detect if current trend going Downwards / Sideways / Upwards, strategy will respond accordingly
            dataframe.loc[(dataframe['adx'] > 20) &
                          (dataframe['plus_di'] < dataframe['minus_di']), 'trend'] = 'downwards'
            dataframe.loc[dataframe['adx'] < 20, 'trend'] = 'sideways'
            dataframe.loc[(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di']), 'trend'] = 'upwards'

            # If a Weighted Sell Signal goes off => Bearish Indication, Set to true (=1) and multiply by weight
            # percentage

            # Weighted Sell Signal: ADX above 25 & +DI below -DI (The trend has strength while moving down)
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += 1 * params['downwards_trend_adx_strong_down_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += 1 * params['sideways_trend_adx_strong_down_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['adx'] > 25),
                          'total_sell_signal_strength'] += 1 * params['upwards_trend_adx_strong_down_sell_weight']

            # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += 1 * params['downwards_trend_rsi_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += 1 * params['sideways_trend_rsi_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['rsi'], 70),
                          'total_sell_signal_strength'] += 1 * params['upwards_trend_rsi_sell_weight']

            # Weighted Sell Signal: MACD below Signal
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += 1 * params['downwards_trend_macd_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += 1 * params['sideways_trend_macd_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['macd'] < dataframe['macdsignal']),
                          'total_sell_signal_strength'] += 1 * params['upwards_trend_macd_sell_weight']

            # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += \
                1 * params['downwards_trend_sma_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += \
                1 * params['sideways_trend_sma_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma9'], dataframe[
                'sma50']), 'total_sell_signal_strength'] += \
                1 * params['upwards_trend_sma_short_death_cross_sell_weight']

            # Weighted Sell Signal: EMA short term Death Cross (Short term EMA crosses below Medium term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += \
                1 * params['downwards_trend_ema_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += \
                1 * params['sideways_trend_ema_short_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema9'], dataframe[
                'ema50']), 'total_sell_signal_strength'] += \
                1 * params['upwards_trend_ema_short_death_cross_sell_weight']

            # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += \
                1 * params['downwards_trend_sma_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += \
                1 * params['sideways_trend_sma_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['sma50'], dataframe[
                'sma200']), 'total_sell_signal_strength'] += \
                1 * params['upwards_trend_sma_long_death_cross_sell_weight']

            # Weighted Sell Signal: EMA long term Death Cross (Medium term EMA crosses below Long term EMA)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += \
                1 * params['downwards_trend_ema_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += \
                1 * params['sideways_trend_ema_long_death_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['ema50'], dataframe[
                'ema200']), 'total_sell_signal_strength'] += \
                1 * params['upwards_trend_ema_long_death_cross_sell_weight']

            # Weighted Sell Signal: Re-Entering Upper Bollinger Band after upward breakout
            # (Candle closes below Upper Bollinger Band)
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                1 * params['downwards_trend_bollinger_bands_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                1 * params['sideways_trend_bollinger_bands_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['close'], dataframe[
                'bb_upperband']), 'total_sell_signal_strength'] += \
                1 * params['upwards_trend_bollinger_bands_sell_weight']

            # Weighted Sell Signal: VWAP crosses below current price
            dataframe.loc[(dataframe['trend'] == 'downwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += 1 * params['downwards_trend_vwap_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'sideways') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += 1 * params['sideways_trend_vwap_cross_sell_weight']
            dataframe.loc[(dataframe['trend'] == 'upwards') & qtpylib.crossed_below(dataframe['vwap'], dataframe[
                'close']), 'total_sell_signal_strength'] += 1 * params['upwards_trend_vwap_cross_sell_weight']

            # Check if sell signal should be sent depending on the current trend
            dataframe.loc[(dataframe['trend'] == 'downwards') & (dataframe['total_sell_signal_strength'] >= params[
                '_downwards_trend_total_sell_signal_needed']), 'sell'] = 1
            dataframe.loc[(dataframe['trend'] == 'sideways') & (dataframe['total_sell_signal_strength'] >= params[
                '_sideways_trend_total_sell_signal_needed']), 'sell'] = 1
            dataframe.loc[(dataframe['trend'] == 'upwards') & (dataframe['total_sell_signal_strength'] >= params[
                '_upwards_trend_total_sell_signal_needed']), 'sell'] = 1

            # Override Sell Signal: When configured sell signals can be completely turned off for each kind of trend
            if not params['.trade_sells_when_downwards']:
                dataframe.loc[dataframe['trend'] == 'downwards', 'sell'] = 0
            if not params['.trade_sells_when_sideways']:
                dataframe.loc[dataframe['trend'] == 'sideways', 'sell'] = 0
            if not params['.trade_sells_when_upwards']:
                dataframe.loc[dataframe['trend'] == 'upwards', 'sell'] = 0

            return dataframe

        return populate_sell_trend
