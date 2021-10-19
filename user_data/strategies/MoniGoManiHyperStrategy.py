# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import sys
from pathlib import Path

import numpy as np  # noqa
import pandas as pd  # noqa
import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.constants import ListPairsWithTimeframes


# Master Framework file must reside in same folder as Strategy file
sys.path.append(str(Path(__file__).parent))
from MasterMoniGoManiHyperStrategy import MasterMoniGoManiHyperStrategy
# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

# Define the Weighted Buy Signals to be used by MGM
buy_signals = {
    # Weighted Buy Signal: MACD above Signal
    'macd': lambda df: (df['macd'] > df['macdsignal']),
    # Weighted Buy Signal: MFI crosses above 20 (Under-bought / low-price and rising indication)
    'mfi': lambda df: (qtpylib.crossed_above(df['mfi'], 20)),
    # Weighted Buy Signal: VWAP crosses above current price
    'vwap_cross': lambda df: (qtpylib.crossed_above(df['vwap'], df['close'])),
    # Weighted Buy Signal: Price crosses above Parabolic SAR
    'sar_cross': lambda df: (qtpylib.crossed_above(df['sar'], df['close'])),
    # Weighted Buy Signal: Stochastic Slow below 20 (Under-bought, indication of starting to move up)
    'stoch': lambda df: (df['slowk'] < 20),
    # Weighted Buy Signal: SMA long term Golden Cross (Medium term SMA crosses above Long term SMA)
    'sma_long_golden_cross': lambda df: (qtpylib.crossed_above(df['sma50'], df['sma200'])),
    # Weighted Buy Signal: SMA short term Golden Cross (Short term SMA crosses above Medium term SMA)
    'sma_short_golden_cross': lambda df: (qtpylib.crossed_above(df['sma9'], df['sma50'])),
    # Weighted Buy Signal: TEMA
    'tema': lambda df: (df['tema'] <= df['bb_middleband']) & (df['tema'] > df['tema'].shift(1))
}

# Define the Weighted Sell Signals to be used by MGM
sell_signals = {
    # Weighted Sell Signal: MACD below Signal
    'macd': lambda df: (df['macd'] < df['macdsignal']),
    # Weighted Sell Signal: MFI crosses below 80 (Over-bought / high-price and dropping indication)
    'mfi': lambda df: (qtpylib.crossed_below(df['mfi'], 80)),
    # Weighted Sell Signal: VWAP crosses below current price
    'vwap_cross': lambda df: (qtpylib.crossed_below(df['vwap'], df['close'])),
    # Weighted Sell Signal: Price crosses below Parabolic SAR
    'sar_cross': lambda df: (qtpylib.crossed_below(df['sar'], df['close'])),
    # Weighted Sell Signal: Stochastic Slow above 80 (Over-bought, indication of starting to move down)
    'stoch': lambda df: (df['slowk'] > 80),
    # Weighted Sell Signal: SMA long term Death Cross (Medium term SMA crosses below Long term SMA)
    'sma_long_death_cross': lambda df: (qtpylib.crossed_below(df['sma50'], df['sma200'])),
    # Weighted Sell Signal: SMA short term Death Cross (Short term SMA crosses below Medium term SMA)
    'sma_short_death_cross': lambda df: (qtpylib.crossed_below(df['sma9'], df['sma50'])),
    # Weighted Buy Signal: TEMA
    'tema': lambda df: (df['tema'] > df['bb_middleband']) & (df['tema'] < df['tema'].shift(1))
}


# Returns the method responsible for decorating the current class with all the parameters of the MGM
generate_mgm_attributes = MasterMoniGoManiHyperStrategy.generate_mgm_attributes(buy_signals, sell_signals)


@generate_mgm_attributes
class MoniGoManiHyperStrategy(MasterMoniGoManiHyperStrategy):
    """
    ####################################################################################
    ####                                                                            ####
    ###                  MoniGoMani Base Strategy v0.13.0 by Rikj000                 ###
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

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the Freqtrade documentation or it's Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Plot configuration to show all Weighted Signals/Indicators used by MoniGoMani in FreqUI.
    # Also loads in MGM Framework Plots for Buy/Sell Signals/Indicators and Trend Detection.
    plot_config = MasterMoniGoManiHyperStrategy.populate_frequi_plots({
        # Main Plots Signals/Indicators (SMAs, EMAs, Bollinger Bands, VWAP, TEMA)
        'main_plot': {
            'sma9': {'color': '#2c05f6'},
            'sma50': {'color': '#19038a'},
            'sma200': {'color': '#0d043b'},
            'ema9': {'color': '#12e5a6'},
            'ema50': {'color': '#0a8963'},
            'ema200': {'color': '#074b36'},
            'bb_middleband': {'color': '#6f1a7b'},
            'vwap': {'color': '#727272'},
            'tema': {'color': '#9345ee'}
        },
        # Sub Plots - Each dict defines one additional plot
        'subplots': {
            # Sub Plots - Individual Weighted Signals/Indicators
            'ADX (Average Directional Index)': {
                'adx': {'color': '#6f1a7b'}
            },
            'MACD (Moving Average Convergence Divergence)': {
                'macd': {'color': '#19038a'},
                'macdsignal': {'color': '#ae231c'}
            },
            'MFI (Money Flow Index)': {
                'mfi': {'color': '#7fba3c'}
            },
            'RSI (Relative Strength Index)': {
                'rsi': {'color': '#7fb92a'}
            },
            'Stochastic Slow': {
                'slowk': {'color': '#14efe7'}
            }
        }
    })

    def informative_pairs(self) -> ListPairsWithTimeframes:
        """
        Defines additional informative pair/interval combinations to be cached from the exchange,
        these will be used during TimeFrame-Zoom.

        :return informative_pairs: (list) List populated with additional informative pairs
        """

        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        informative_pairs += [(pair, self.core_trend_timeframe) for pair in pairs]
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds base indicators based on Run-Mode & TimeFrame-Zoom

        :param dataframe: (DataFrame) DataFrame with data from the exchange
        :param metadata: (dict) Additional information, like the currently traded pair
        :return DataFrame: DataFrame for MoniGoMani with all mandatory indicator data populated
        """

        return self._populate_indicators(dataframe=dataframe, metadata=metadata)

    def do_populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to MoniGoMani's DataFrame per pair.
        Should be called with 'informative_pair' (1h candles) during backtesting/hyperopting with TimeFrame-Zoom!

        Performance Note: For the best performance be frugal on the number of indicators you are using.
        Only add in indicators that you are using in your weighted signal configuration for MoniGoMani,
        otherwise you will waste your memory and CPU usage.

        :param dataframe: (DataFrame) DataFrame with data from the exchange
        :param metadata: (dict) Additional information, like the currently traded pair
        :return DataFrame: DataFrame for MoniGoMani with all mandatory indicator data populated
        """

        # Momentum Indicators (timeperiod is expressed in candles)
        # -------------------

        # Parabolic SAR
        dataframe['sar'] = ta.SAR(dataframe)

        # Stochastic Slow
        stoch = ta.STOCH(dataframe)
        dataframe['slowk'] = stoch['slowk']

        # MACD - Moving Average Convergence Divergence
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']  # MACD - Blue TradingView Line (Bullish if on top)
        dataframe['macdsignal'] = macd['macdsignal']  # Signal - Orange TradingView Line (Bearish if on top)

        # MFI - Money Flow Index (Under bought / Over sold & Over bought / Under sold / volume Indicator)
        dataframe['mfi'] = ta.MFI(dataframe)

        # Overlap Studies
        # ---------------

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_middleband'] = bollinger['mid']

        # SMA's & EMA's are trend following tools (Should not be used when line goes sideways)
        # SMA - Simple Moving Average (Moves slower compared to EMA, price trend over X periods)
        dataframe['sma9'] = ta.SMA(dataframe, timeperiod=9)
        dataframe['sma50'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['sma200'] = ta.SMA(dataframe, timeperiod=200)

        # TEMA - Triple Exponential Moving Average
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

        # Volume Indicators
        # -----------------

        # VWAP - Volume Weighted Average Price
        dataframe['vwap'] = qtpylib.vwap(dataframe)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the buy trend with weighted buy signals used in MoniGoMani's DataFrame per pair.

        :param dataframe: (DataFrame) DataFrame with data from the exchange and all mandatory indicator data populated
        :param metadata: (dict) Additional information, like the currently traded pair
        :return DataFrame: DataFrame for MoniGoMani with all mandatory weighted buy signals populated
        """

        # Keep this call to populate the conditions responsible for the weights of your buy signals
        dataframe = self._populate_trend('buy', dataframe, metadata)

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the buy trend with weighted buy signals used in MoniGoMani's DataFrame per pair.

        :param dataframe: (DataFrame) DataFrame with data from the exchange,
            all mandatory indicator and weighted buy signal data populated
        :param metadata: (dict) Additional information, like the currently traded pair
        :return DataFrame: DataFrame for MoniGoMani with all mandatory weighted sell signals populated
        """

        # Keep this call to populate the conditions responsible for the weights of your sell signals
        dataframe = self._populate_trend('sell', dataframe, metadata)

        return dataframe
