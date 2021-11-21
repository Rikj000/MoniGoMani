# -*- coding: utf-8 -*-
# --- ↓ Do not remove these libs ↓ -------------------------------------------------------------------------------------
import copy
import json
import logging
import math
import os
import sys
from abc import ABC
from datetime import datetime, timedelta
from functools import reduce
from typing import Any, Dict, List, Optional, Union

import numpy as np  # noqa
import pandas as pd  # noqa
import talib.abstract as ta
from numpy import timedelta64
from pandas import DataFrame
from scipy.interpolate import interp1d
from yaml import full_load

from freqtrade.data.history import load_pair_history
from freqtrade.enums import RunMode
from freqtrade.exchange import timeframe_to_prev_date
from freqtrade.misc import deep_merge_dicts, round_dict
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal
from freqtrade.persistence import Trade
from freqtrade.strategy import IntParameter, IStrategy, merge_informative_pair, timeframe_to_minutes

logger = logging.getLogger(__name__)


# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------


class MasterMoniGoManiHyperStrategy(IStrategy, ABC):
    """
    ####################################################################################
    ####                                                                            ####
    ###                MoniGoMani Master Framework v0.13.0 by Rikj000                ###
    ##                          -----------------------------                         ##
    #               Isn't that what we all want? Our money to go many?                 #
    #          Well that's what this Freqtrade framework hopes to do for you!          #
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

    # MGM trend names
    mgm_trends = ['downwards', 'sideways', 'upwards']

    # Initialize empty buy/sell_params dictionaries
    buy_params = {}
    sell_params = {}

    # Load the MoniGoMani config names from '.hurry'
    mgm_config_name = mgm_config_hyperopt_name = None
    hurry_config_path = f'{os.getcwd()}/.hurry'
    if os.path.isfile(hurry_config_path) is True:
        with open(hurry_config_path, 'r') as yml_file:
            config = full_load(yml_file) or {}

        if 'config' in config:
            hurry_config = config['config']
            mgm_config_name = hurry_config['mgm_config_names']['mgm-config']
            mgm_config_hyperopt_name = hurry_config['mgm_config_names']['mgm-config-hyperopt']

    if (mgm_config_name is None) or (mgm_config_hyperopt_name is None):
        sys.exit('MoniGoManiHyperStrategy - ERROR - The MoniGoMani Configuration filenames could not be loaded from'
                 '".hurry"... Please run "python3 ./mgm-hurry setup" to create your ".hurry" file')

    # Load the MoniGoMani settings
    mgm_config_path = f'{os.getcwd()}/user_data/{mgm_config_name}'
    if os.path.isfile(mgm_config_path) is True:
        # Load the 'mgm-config.json' file as an object and parse it as a dictionary
        file_object = open(mgm_config_path, )
        json_data = json.load(file_object)
        mgm_config = json_data['monigomani_settings']
    else:
        sys.exit(f'MoniGoManiHyperStrategy - ERROR - The main MoniGoMani configuration file "mgm-config" can\'t '
                 f'be found at: {mgm_config_path}... Please provide the correct file and/or alter "mgm_config_name" in '
                 f'".hurry"')

    # Apply the loaded MoniGoMani Settings
    try:
        backtest_timeframe = mgm_config['timeframes']['backtest_timeframe']
        core_trend_timeframe = mgm_config['timeframes']['core_trend_timeframe']
        roi_timeframe = mgm_config['timeframes']['roi_timeframe']
        timeframe = mgm_config['timeframes']['timeframe']
        startup_candle_count = mgm_config['startup_candle_count']
        precision = mgm_config['precision']
        min_weighted_signal_value = mgm_config['weighted_signal_spaces']['min_weighted_signal_value']
        max_weighted_signal_value = mgm_config['weighted_signal_spaces']['max_weighted_signal_value']
        min_trend_total_signal_needed_value = mgm_config[
            'weighted_signal_spaces']['min_trend_total_signal_needed_value']
        min_trend_total_signal_needed_candles_lookback_window_value = mgm_config[
            'weighted_signal_spaces']['min_trend_total_signal_needed_candles_lookback_window_value']
        max_trend_total_signal_needed_candles_lookback_window_value = mgm_config[
            'weighted_signal_spaces']['max_trend_total_signal_needed_candles_lookback_window_value']
        min_trend_signal_triggers_needed_value = mgm_config[
            'weighted_signal_spaces']['min_trend_signal_triggers_needed']
        search_threshold_weighted_signal_values = mgm_config[
            'weighted_signal_spaces']['search_threshold_weighted_signal_values']
        search_threshold_trend_total_signal_needed_candles_lookback_window_value = mgm_config[
            'weighted_signal_spaces']['search_threshold_trend_total_signal_needed_candles_lookback_window_value']
        search_threshold_trend_signal_triggers_needed = mgm_config[
            'weighted_signal_spaces']['search_threshold_trend_signal_triggers_needed']
        roi_delay = mgm_config['roi_spaces']['roi_delay']
        roi_table_step_size = mgm_config['roi_spaces']['roi_table_step_size']
        roi_time_interval_scaling = mgm_config['roi_spaces']['roi_time_interval_scaling']
        roi_value_step_scaling = mgm_config['roi_spaces']['roi_value_step_scaling']
        roi_when_downwards = mgm_config['roi_spaces']['roi_when_downwards']
        roi_when_sideways = mgm_config['roi_spaces']['roi_when_sideways']
        roi_when_upwards = mgm_config['roi_spaces']['roi_when_upwards']
        stoploss_min_value = mgm_config['stoploss_spaces']['stoploss_min_value']
        stoploss_max_value = mgm_config['stoploss_spaces']['stoploss_max_value']
        trailing_stop_positive_min_value = mgm_config['stoploss_spaces']['trailing_stop_positive_min_value']
        trailing_stop_positive_max_value = mgm_config['stoploss_spaces']['trailing_stop_positive_max_value']
        trailing_stop_positive_offset_min_value = mgm_config[
            'stoploss_spaces']['trailing_stop_positive_offset_min_value']
        trailing_stop_positive_offset_max_value = mgm_config[
            'stoploss_spaces']['trailing_stop_positive_offset_max_value']
        mgm_unclogger_add_params = mgm_config['unclogger_spaces']
        minimal_roi = mgm_config['default_stub_values']['minimal_roi']
        stoploss = mgm_config['default_stub_values']['stoploss']
        trailing_stop = mgm_config['default_stub_values']['trailing_stop']
        trailing_stop_positive = mgm_config['default_stub_values']['trailing_stop_positive']
        trailing_stop_positive_offset = mgm_config['default_stub_values']['trailing_stop_positive_offset']
        trailing_only_offset_is_reached = mgm_config['default_stub_values']['trailing_only_offset_is_reached']
        debuggable_weighted_signal_dataframe = mgm_config['debuggable_weighted_signal_dataframe']
        use_mgm_logging = mgm_config['use_mgm_logging']
        mgm_log_levels_enabled = mgm_config['mgm_log_levels_enabled']
    except KeyError as missing_setting:
        sys.exit(f'MoniGoManiHyperStrategy - ERROR - '
                 f'The main MoniGoMani configuration file "mgm-config" is missing some settings.'
                 f'\nPlease make sure that all MoniGoMani related settings are existing inside this file!'
                 f'\n{missing_setting} has been detected as missing from the file...'
                 f'\nCompare with the latest "mgm-config.example" to see if you are up to date with the latest settings'
                 f': \nhttps://github.com/Rikj000/MoniGoMani/blob/development/user_data/mgm-config.example.json')

    # If results from a previous HyperOpt Run are found then continue the next HyperOpt Run upon them
    mgm_config_hyperopt_path = f'{os.getcwd()}/user_data/{mgm_config_hyperopt_name}'
    if os.path.isfile(mgm_config_hyperopt_path) is True:
        # Try to load the previous 'mgm-config-hyperopt' file as an object and parse it as a dictionary
        # if the parse fails, warn and continue as if it didn't exist.
        try:
            file_object = open(mgm_config_hyperopt_path, )
            mgm_config_hyperopt = json.load(file_object)
        except ValueError as e:
            mgm_config_hyperopt = {}
            logger.warning(f'MoniGoManiHyperStrategy - WARN - {mgm_config_hyperopt_path} is inaccessible or is '
                           f'not valid JSON, disregarding existing "mgm-config-hyperopt" file and '
                           f'treating as first hyperopt run!')

        # Convert the loaded 'mgm-config-hyperopt' data to the needed HyperOpt Results format if it's found
        # Default stub values from 'mgm-config' are used otherwise.
        if mgm_config_hyperopt != {}:
            for space in mgm_config_hyperopt['params']:
                if space in ['buy', 'sell']:
                    for param, param_value in mgm_config_hyperopt['params'][space].items():
                        if param.startswith('buy'):
                            buy_params[param] = param_value
                        else:
                            sell_params[param] = param_value

                if space == 'roi':
                    minimal_roi = mgm_config_hyperopt['params'][space]

                if space == 'stoploss':
                    stoploss = mgm_config_hyperopt['params'][space][space]

                if space == 'trailing':
                    trailing_stop = mgm_config_hyperopt['params'][space]['trailing_stop']
                    trailing_stop_positive = mgm_config_hyperopt['params'][space]['trailing_stop_positive']
                    trailing_stop_positive_offset = mgm_config_hyperopt[
                        'params'][space]['trailing_stop_positive_offset']
                    trailing_only_offset_is_reached = mgm_config_hyperopt[
                        'params'][space]['trailing_only_offset_is_reached']
    else:
        mgm_config_hyperopt = {}

    # Create dictionary to store custom information MoniGoMani will be using in RAM
    initial_custom_info: dict = {'open_trades': {}, 'unclogger_cooldown_pairs': {}}
    custom_info: dict = copy.deepcopy(initial_custom_info)

    # Initialize some parameters which will be automatically configured/used by MoniGoMani
    use_custom_stoploss = True  # Leave this enabled (Needed for open_trade custom_information_storage)
    is_dry_live_run_detected = True  # Class level runmode detection, Gets set automatically
    informative_timeframe = timeframe  # Gets set automatically
    timeframe_multiplier = None  # Gets set automatically
    separator = 1.5  # Gets set automatically
    separator_candle_weight_reducer = 0.03  # Gets set automatically

    # Initialize comparison values to check if total signals utilized by HyperOpt are possible
    total_signals_possible = {}
    total_triggers_possible = {}
    for trend in mgm_trends:
        for space in ['buy', 'sell']:
            total_signals_possible[f'{space}_{trend}'] = 0
            total_triggers_possible[f'{space}_{trend}'] = 0

    class HyperOpt:
        @staticmethod
        def generate_roi_table(params: Dict) -> Dict[int, float]:
            """
            Generates a Custom Long Continuous ROI (Return of Interest) Table with less gaps in it.
            Configurable step_size is loaded in from the Master MGM Framework.

            :param params: (Dict) Base Parameters used for the ROI Table calculation
            :return Dict: Generated ROI Table
            """
            step = MasterMoniGoManiHyperStrategy.roi_table_step_size

            minimal_roi = {0: params['roi_p1'] + params['roi_p2'] + params['roi_p3'],
                           params['roi_t3']: params['roi_p1'] + params['roi_p2'],
                           params['roi_t3'] + params['roi_t2']: params['roi_p1'],
                           params['roi_t3'] + params['roi_t2'] + params['roi_t1']: 0}

            max_value = max(map(int, minimal_roi.keys()))
            min_value = MasterMoniGoManiHyperStrategy.roi_delay
            f = interp1d(list(map(int, minimal_roi.keys())), list(minimal_roi.values()))
            x = list(range(min_value, max_value, step))
            y = list(map(float, map(f, x)))
            if y[-1] != 0:
                x.append(x[-1] + step)
                y.append(0)
            return dict(zip(x, y))

        @staticmethod
        def roi_space() -> List[Dimension]:
            """
            Create a ROI (Return of Interest) space. Defines values to search for each ROI steps.
            This method implements adaptive ROI HyperSpace with varied ranges for parameters which automatically adapts
            to the un-zoomed base_weighted_signal_timeframe used by the MGM Framework during BackTesting & HyperOpting.

            :return List: Generated ROI Space
            """

            # Default scaling coefficients for the ROI HyperSpace. Can be changed to adjust resulting ranges of the ROI
            # tables. Increase if you need wider ranges in the ROI HyperSpace, decrease if shorter ranges are needed:
            # roi_t_alpha: Limits for the time intervals in the ROI Tables. Components are scaled linearly.
            roi_t_alpha = MasterMoniGoManiHyperStrategy.roi_time_interval_scaling
            # roi_p_alpha: Limits for the ROI value steps. Components are scaled logarithmically.
            roi_p_alpha = MasterMoniGoManiHyperStrategy.roi_value_step_scaling

            # Load in the ROI timeframe size from the Master MGM Framework
            timeframe_min = timeframe_to_minutes(MasterMoniGoManiHyperStrategy.roi_timeframe)

            # The scaling is designed so that it maps exactly to the legacy Freqtrade roi_space()
            # method for the 5m timeframe.
            roi_t_scale = timeframe_min / 5
            roi_p_scale = math.log1p(timeframe_min) / math.log1p(5)
            roi_limits = {'roi_t1_min': int(10 * roi_t_scale * roi_t_alpha),
                          'roi_t1_max': int(120 * roi_t_scale * roi_t_alpha),
                          'roi_t2_min': int(10 * roi_t_scale * roi_t_alpha),
                          'roi_t2_max': int(60 * roi_t_scale * roi_t_alpha),
                          'roi_t3_min': int(10 * roi_t_scale * roi_t_alpha),
                          'roi_t3_max': int(40 * roi_t_scale * roi_t_alpha),
                          'roi_p1_min': 0.01 * roi_p_scale * roi_p_alpha,
                          'roi_p1_max': 0.04 * roi_p_scale * roi_p_alpha,
                          'roi_p2_min': 0.01 * roi_p_scale * roi_p_alpha,
                          'roi_p2_max': 0.07 * roi_p_scale * roi_p_alpha,
                          'roi_p3_min': 0.01 * roi_p_scale * roi_p_alpha,
                          'roi_p3_max': 0.20 * roi_p_scale * roi_p_alpha}

            # Generate MGM's custom long continuous ROI table
            logger.debug(f'Using ROI space limits: {roi_limits}')
            p = {'roi_t1': roi_limits['roi_t1_min'], 'roi_t2': roi_limits['roi_t2_min'],
                 'roi_t3': roi_limits['roi_t3_min'], 'roi_p1': roi_limits['roi_p1_min'],
                 'roi_p2': roi_limits['roi_p2_min'], 'roi_p3': roi_limits['roi_p3_min']}
            logger.info(f'Min ROI table: {round_dict(MasterMoniGoManiHyperStrategy.HyperOpt.generate_roi_table(p), 3)}')
            p = {'roi_t1': roi_limits['roi_t1_max'], 'roi_t2': roi_limits['roi_t2_max'],
                 'roi_t3': roi_limits['roi_t3_max'], 'roi_p1': roi_limits['roi_p1_max'],
                 'roi_p2': roi_limits['roi_p2_max'], 'roi_p3': roi_limits['roi_p3_max']}
            logger.info(f'Max ROI table: {round_dict(MasterMoniGoManiHyperStrategy.HyperOpt.generate_roi_table(p), 3)}')

            return [Integer(roi_limits['roi_t1_min'], roi_limits['roi_t1_max'], name='roi_t1'),
                    Integer(roi_limits['roi_t2_min'], roi_limits['roi_t2_max'], name='roi_t2'),
                    Integer(roi_limits['roi_t3_min'], roi_limits['roi_t3_max'], name='roi_t3'),
                    SKDecimal(roi_limits['roi_p1_min'], roi_limits['roi_p1_max'], decimals=3, name='roi_p1'),
                    SKDecimal(roi_limits['roi_p2_min'], roi_limits['roi_p2_max'], decimals=3, name='roi_p2'),
                    SKDecimal(roi_limits['roi_p3_min'], roi_limits['roi_p3_max'], decimals=3, name='roi_p3')]

        @staticmethod
        def stoploss_space() -> List[Dimension]:
            """
            Define custom stoploss search space with configurable parameters for the Stoploss Value to search.
            Override it if you need some different range for the parameter in the 'stoploss' optimization hyperspace.

            :return List: Generated Stoploss Space
            """
            return [SKDecimal(MasterMoniGoManiHyperStrategy.stoploss_max_value,
                              MasterMoniGoManiHyperStrategy.stoploss_min_value, decimals=3, name='stoploss')]

        @staticmethod
        def trailing_space() -> List[Dimension]:
            """
            Define custom trailing search space with parameters configurable in 'mgm-config'

            :return List: Generated Trailing Space
            """
            return [
                # It was decided to always set trailing_stop is to True if the 'trailing' hyperspace
                # is used. Otherwise hyperopt will vary other parameters that won't have effect if
                # trailing_stop is set False.
                # This parameter is included into the hyperspace dimensions rather than assigning
                # it explicitly in the code in order to have it printed in the results along with
                # other 'trailing' hyperspace parameters.
                Categorical([True], name='trailing_stop'),
                SKDecimal(MasterMoniGoManiHyperStrategy.trailing_stop_positive_min_value,
                          MasterMoniGoManiHyperStrategy.trailing_stop_positive_max_value,
                          decimals=3, name='trailing_stop_positive'),
                # 'trailing_stop_positive_offset' should be greater than 'trailing_stop_positive',
                # so this intermediate parameter is used as the value of the difference between
                # them. The value of the 'trailing_stop_positive_offset' is constructed in the
                # generate_trailing_params() method.
                # This is similar to the hyperspace dimensions used for constructing the ROI tables.
                SKDecimal(MasterMoniGoManiHyperStrategy.trailing_stop_positive_offset_min_value,
                          MasterMoniGoManiHyperStrategy.trailing_stop_positive_offset_max_value,
                          decimals=3, name='trailing_stop_positive_offset_p1'),
                Categorical([True, False], name='trailing_only_offset_is_reached')]

    def __init__(self, config: dict):
        """
        First method to be called once during the MoniGoMani class initialization process

        :param config: (dict)
        """

        i = 'Initialization'
        if RunMode(config.get('runmode', RunMode.OTHER)) in (RunMode.BACKTEST, RunMode.HYPEROPT):
            self.timeframe = self.backtest_timeframe
            self.mgm_logger('info', 'TimeFrame-Zoom', f'Auto updating to zoomed "backtest_timeframe": {self.timeframe}')

            self.is_dry_live_run_detected = False
            self.mgm_logger('info', i, 'Current run mode detected as: HyperOpting/BackTesting. '
                                       'Auto updated is_dry_live_run_detected to: False')

            self.mgm_logger('info', i, 'Calculating and storing "timeframe_multiplier"')
            self.timeframe_multiplier = int(timeframe_to_minutes(self.informative_timeframe)
                                            / timeframe_to_minutes(self.timeframe))
            if self.timeframe_multiplier < 1:
                raise SystemExit('MoniGoManiHyperStrategy - ERROR - TimeFrame-Zoom - '
                                 '"timeframe" must be bigger than "backtest_timeframe"')

        else:
            if os.path.isfile(self.mgm_config_hyperopt_path) is False:
                sys.exit(f'MoniGoManiHyperStrategy - ERROR - The MoniGoMani HyperOpt Results configuration file '
                         f'({self.mgm_config_hyperopt_name}) can\'t be found at: {self.mgm_config_hyperopt_path}... '
                         f'Please Optimize your MoniGoMani before Dry/Live running! Once optimized provide the correct '
                         f'file and/or alter "mgm_config_names" in ".hurry"')

            self.is_dry_live_run_detected = True
            self.mgm_logger('info', i, 'Current run mode detected as: Dry/Live-Run. '
                                       'Auto updated is_dry_live_run_detected to: True')

        if self.mgm_config['unclogger_spaces']['unclogger_enabled'] is True:
            self.separator = self.mgm_config['unclogger_spaces'][
                'unclogger_trend_lookback_candles_window_recent_past_weight_separator']
            separator_window = (self.separator / 1) - (1 / self.separator)
            trend_lookback_candles_window = self.get_param_value('sell___unclogger_trend_lookback_candles_window')
            self.separator_candle_weight_reducer = (separator_window / trend_lookback_candles_window)

        super().__init__(config)

    @staticmethod
    def populate_frequi_plots(weighted_signal_plots: dict) -> dict:
        """
        Merges the Weighted Signal Plots together with the Buy/Sell Signal Plots and the Trend Detection Plots for
        a nice visualization in FreqUI

        :param weighted_signal_plots: FreqUI plotting data used for weighted signals (and their indicators)
        :return dict: Complete FreqUI plotting data containing weighted signal + other MGM Framework plotting
        """

        # Plot configuration to show all signals used in MoniGoMani in FreqUI (Use load from Strategy in FreqUI)
        framework_plots = {
            # Main Plots - Trend Indicator (SAR)
            'main_plot': {
                'sar': {'color': '#2c05f6'}
            },
            # Sub Plots - Each dict defines one additional plot
            'subplots': {
                # Sub Plots - Trend Detection
                'MoniGoMani Core Trend': {
                    'mgm_trend': {'color': '#7fba3c'}
                },
                'Hilbert Transform (Trend vs Cycle)': {
                    'ht_trendmode': {'color': '#6f1a7b'}
                },
                # Sub Plots - Final Buy + Sell Signals
                'Buy + Sell Signals Firing': {
                    'buy': {'color': '#09d528'},
                    'sell': {'color': '#d19e28'}
                },
                'Total Buy + Sell Signal Strength': {
                    'total_buy_signal_strength': {'color': '#09d528'},
                    'total_sell_signal_strength': {'color': '#d19e28'}
                },
                'Weighted Buy + Sell Signals Firing': {
                    'buy_signals_triggered': {'color': '#09d528'},
                    'sell_signals_triggered': {'color': '#d19e28'}
                }
            }
        }

        return deep_merge_dicts(framework_plots, weighted_signal_plots)

    def _populate_core_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds the core indicators used to define trends to the strategy engine.

        :param dataframe: (DataFrame) DataFrame with data from the exchange
        :param metadata: (dict) Additional information, like the currently traded pair
        :return: a Dataframe with all core trend indicators for MoniGoMani
        """

        # Momentum Indicators
        # -------------------
        # Hilbert Transform - Trend vs Cycle
        dataframe['ht_trendmode'] = ta.HT_TRENDMODE(dataframe)

        # Parabolic SAR
        dataframe['sar'] = ta.SAR(dataframe)

        # Core Trend Detection
        # --------------------
        dataframe.loc[(dataframe['ht_trendmode'] == 1) & (dataframe['sar'] > dataframe['close']), 'trend'] = 'downwards'
        dataframe.loc[(dataframe['ht_trendmode'] == 0) | (dataframe['sar'] == dataframe['close']), 'trend'] = 'sideways'
        dataframe.loc[(dataframe['ht_trendmode'] == 1) & (dataframe['sar'] < dataframe['close']), 'trend'] = 'upwards'

        # Add DataFrame column for visualization in FreqUI when Dry/Live RunMode is detected
        if self.is_dry_live_run_detected is True:
            dataframe.loc[(dataframe['trend'] == 'downwards'), 'mgm_trend'] = -1
            dataframe.loc[(dataframe['trend'] == 'sideways'), 'mgm_trend'] = 0
            dataframe.loc[(dataframe['trend'] == 'upwards'), 'mgm_trend'] = 1

        return dataframe

    def minutes_to_timeframe(self, minutes: int) -> str:
        """
        Calculates the corresponding timeframe for the amount of minutes provided

        :param minutes: (int) Amount of minutes to parse to the closest candle size
        :return: (str) The parsed timeframe / candle size
        """

        if minutes < 1:
            timeframe_number = 60 * minutes
            timeframe_size = 's'  # Return seconds
        elif minutes < 60:
            timeframe_number = minutes
            timeframe_size = 'm'  # Return minutes
        elif minutes < 1440:
            timeframe_number = minutes / 60
            timeframe_size = 'h'  # Return hours
        elif minutes < 10080:
            timeframe_number = minutes / 1440
            timeframe_size = 'd'  # Return days
        elif minutes < 40320:
            timeframe_number = minutes / 10080
            timeframe_size = 'w'  # Return weeks
        else:
            timeframe_number = minutes / 40320
            timeframe_size = 'M'  # Return months

        if (timeframe_number - int(timeframe_number) == 0) is False:
            sys.exit(f'MoniGoManiHyperStrategy - ERROR - MoniGoMani could not correctly parse the provided minutes '
                     f'({minutes}m) to a usable timeframe format ({str(timeframe_number)}{timeframe_size})! '
                     f'Please adjust the "timeframes" section of your "mgm-config"!')

        return f'{str(int(timeframe_number))}{timeframe_size}'

    def _populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds indicators based on Run-Mode & TimeFrame-Zoom:
        If Dry/Live-running or BackTesting/HyperOpting without TimeFrame-Zoom it just pulls
        'timeframe' (1h candles) to compute indicators.

        If BackTesting/HyperOpting with TimeFrame-Zoom it pulls 'informative_pairs' (1h candles)
        to compute indicators, but then tests upon 'backtest_timeframe' (5m or 1m candles)
        to simulate price movement during that 'timeframe' (1h candle).

        :param dataframe: (DataFrame) DataFrame with data from the exchange
        :param metadata: (dict) Additional information, like the currently traded pair
        :return DataFrame: DataFrame for MoniGoMani with all mandatory indicator data populated
        """

        tfz = 'TimeFrame-Zoom'

        # Compute indicator data during Backtesting / Hyperopting when TimeFrame-Zooming
        if (self.is_dry_live_run_detected is False) and (self.informative_timeframe != self.backtest_timeframe):
            self.mgm_logger('info', tfz, f'Backtesting/Hyperopting this strategy with a informative_timeframe '
                                         f'({self.informative_timeframe} candles) and a zoomed backtest_timeframe '
                                         f'({self.backtest_timeframe} candles)')

            # Populate core trend indicators
            core_trend = load_pair_history(pair=metadata['pair'],
                                           datadir=self.config['datadir'],
                                           timeframe=self.core_trend_timeframe,
                                           # ToDo: calculate correct startup_candles needed for HT_TRENDMODE and SAR
                                           startup_candles=self.startup_candle_count,
                                           data_format=self.config.get('dataformat_ohlcv', 'json'))
            core_trend = self._populate_core_trend(core_trend, metadata)

            # Warning! This method gets ALL downloaded data for the given timeframe (when in BackTesting mode).
            # If you have many months or years downloaded for this pair, this will take a long time!
            informative = load_pair_history(pair=metadata['pair'],
                                            datadir=self.config['datadir'],
                                            timeframe=self.informative_timeframe,
                                            startup_candles=self.startup_candle_count,
                                            data_format=self.config.get('dataformat_ohlcv', 'json'))
            # Throw away older data that isn't needed.
            first_informative = dataframe['date'].min().floor('H')
            informative = informative[informative['date'] >= first_informative]

            # Merge core trend to informative data frame
            informative = merge_informative_pair(
                informative, core_trend[['date', 'ht_trendmode', 'sar', 'trend']].copy(),
                self.informative_timeframe, self.core_trend_timeframe, ffill=True)
            skip_columns = [f'{s}_{self.core_trend_timeframe}' for s in
                            ['date', 'open', 'high', 'low', 'close', 'volume']]
            informative.rename(columns=lambda s: s.replace('_{}'.format(self.core_trend_timeframe),
                                                           '') if (s not in skip_columns) else s, inplace=True)

            # Populate indicators at a larger timeframe
            informative = self.do_populate_indicators(informative.copy(), metadata)
            # Drop unused columns to keep the dataframe lightweight
            drop_columns = ['open', 'high', 'low', 'close', 'volume', f'date_{self.core_trend_timeframe}']
            informative.drop(drop_columns, inplace=True, axis=1)
            # Merge indicators back in with, filling in missing values.
            dataframe = merge_informative_pair(dataframe, informative, self.timeframe,
                                               self.informative_timeframe, ffill=True)
            # Rename columns, since merge_informative_pair adds `_<timeframe>` to the end of each name.
            # Skip over date etc..
            skip_columns = [f'{s}_{self.informative_timeframe}' for s in
                            ['date', 'open', 'high', 'low', 'close', 'volume']]
            dataframe.rename(columns=lambda s: s.replace('_{}'.format(self.informative_timeframe),
                                                         '') if (s not in skip_columns) else s, inplace=True)
            dataframe.drop([f'date_{self.informative_timeframe}'], inplace=True, axis=1)

        # Compute indicator data normally during Dry & Live Running or when not using TimeFrame-Zoom
        else:
            self.mgm_logger('info', tfz,
                            f'Dry/Live-running MoniGoMani with normal timeframe ({self.timeframe} candles)')

            # Populate core trend indicators
            core_trend = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.core_trend_timeframe)
            core_trend = self._populate_core_trend(core_trend, metadata)

            # Merge core trend to main data frame
            dataframe = merge_informative_pair(
                dataframe, core_trend[['date', 'ht_trendmode', 'sar', 'trend', 'mgm_trend']].copy(),
                self.timeframe, self.core_trend_timeframe, ffill=True)
            skip_columns = [f'{s}_{self.core_trend_timeframe}' for s in
                            ['date', 'open', 'high', 'low', 'close', 'volume']]
            dataframe.rename(columns=lambda s: s.replace('_{}'.format(self.core_trend_timeframe),
                                                         '') if (s not in skip_columns) else s, inplace=True)
            dataframe.drop([f'date_{self.core_trend_timeframe}'], inplace=True, axis=1)

            # Just populate indicators.
            dataframe = self.do_populate_indicators(dataframe, metadata)

        return dataframe

    def get_param_value(self, parameter_name: str):
        """
        Fetches a parameter value from the initialized MoniGoMani class by name

        :param parameter_name: (str) Name of the parameter
        :return: (double) Parameter value divided by precision and rounded
        """
        parameter = getattr(self, parameter_name)
        return round(parameter.value / self.precision)

    def get_all_current_open_trades(self, trade: 'Trade') -> List:
        """
        Fetches all the trades currently open depending on the current RunMode of Freqtrade

        :param trade: (trade) Current open trade object.
        :return List: List containing all current open trades
        """
        cis = 'custom_stoploss - Custom Information Storage'
        if self.is_dry_live_run_detected is True:
            self.mgm_logger('debug', cis, 'Fetching all currently open trades during Dry/Live Run')

            all_open_trades = Trade.get_trades([Trade.is_open.is_(True)]).order_by(Trade.open_date).all()
        # Fetch all open trade data during Back Testing & Hyper Opting
        else:
            self.mgm_logger('debug', cis, 'Fetching all currently open trades during BackTesting/HyperOpting')
            all_open_trades = trade.trades_open

        self.mgm_logger('debug', cis, f'Up-to-date open trades ({str(len(all_open_trades))}) fetched!')
        self.mgm_logger('debug', cis, f'all_open_trades contents: {repr(all_open_trades)}')

        return all_open_trades

    def get_unclogger_trade_trend_data(self, pair: str, current_time: datetime) -> dict:
        """
        Fetches the trade trend data for a pair over a length of the sell___unclogger_trend_lookback_candles_window

        :param pair: (str) Pair of which the trend data needs to be fetched
        :param current_time: (datetime) Current time, represents the start of unclogger_trend_lookback_candles_window
        :return: (dict) Dictionary containing the trend data for the pairs unclogger_trend_lookback_candles_window
        """

        # Fetch all needed 'trend' trade data
        stored_trend_dataframe = {}
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)

        self.mgm_logger('debug', 'Open Trade Unclogger', 'Fetching all needed "trend" trade data')
        trend_lookback_candles_window = self.get_param_value('sell___unclogger_trend_lookback_candles_window')
        for candle in range(1, trend_lookback_candles_window + 1):
            candle_time = self.convert_candle_time(current_time=current_time, current_candle=candle)
            candle_trend = dataframe.loc[dataframe['date'] == candle_time].squeeze()['trend']

            if isinstance(candle_trend, str):
                stored_trend_dataframe[candle] = candle_trend
            else:
                break

        return stored_trend_dataframe

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
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

        cis = 'custom_stoploss - Custom Information Storage'
        gc = cis + ' Garbage Collector'

        # Open Trade Custom Information Storage
        # -------------------------------------
        # Fetch all open trade data depending on RunMode
        all_open_trades = self.get_all_current_open_trades(trade)

        # Store current pair's open_trade + it's current profit in custom_info
        for open_trade in all_open_trades:
            if str(open_trade.pair) == pair:
                if str(open_trade.pair) not in self.custom_info['open_trades']:
                    self.custom_info['open_trades'][str(open_trade.pair)] = {}
                self.custom_info['open_trades'][str(open_trade.pair)]['trade'] = str(open_trade)
                self.custom_info['open_trades'][str(open_trade.pair)]['current_profit'] = current_profit
                self.mgm_logger('info', cis, f'Storing trade + current profit/loss for pair ({pair}) in custom_info')
                break

        # Custom Information Storage Garbage Collector
        # --------------------------------------------
        # Check if any old open_trade garbage needs to be removed
        if len(all_open_trades) < len(self.custom_info['open_trades']):
            garbage_trade_amount = len(self.custom_info['open_trades']) - len(all_open_trades)
            self.mgm_logger('info', gc,
                            f'Old open trade garbage detected for {str(garbage_trade_amount)} trades, starting cleanup')

            for garbage_trade in range(garbage_trade_amount):
                for stored_trade in self.custom_info['open_trades']:
                    pair_still_open = False
                    for open_trade in all_open_trades:
                        if str(stored_trade) == str(open_trade.pair):
                            self.mgm_logger('debug', gc, f'Open trade found, '
                                                         f'no action needed for pair ({stored_trade}) in custom_info')
                            pair_still_open = True
                            break

                    # Remove old open_trade garbage
                    if not pair_still_open:
                        self.mgm_logger('info', gc,
                                        f'No open trade found for pair ({stored_trade}), removing from custom_info')
                        self.custom_info['open_trades'].pop(stored_trade)
                        self.mgm_logger('debug', gc,
                                        f'Successfully removed garbage_trade {str(garbage_trade)} from custom_info!')
                        break

        # Print all stored open trade info in custom_storage
        self.mgm_logger('debug', cis, f'Open trades ({str(len(self.custom_info["open_trades"]))}) '
                                      f'in custom_info updated successfully!')
        self.mgm_logger('debug', cis, f'custom_info["open_trades"] contents: {repr(self.custom_info["open_trades"])}')

        # Always return a value bigger than the initial stoploss to keep using the initial stoploss.
        # Since we (currently) only want to use this function for custom information storage!
        return -1

    def custom_sell(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                    current_profit: float, **kwargs) -> Optional[Union[str, bool]]:
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
        Only used when 'unclogger_enabled' is set to 'true'.

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in ask_strategy.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return: True or string if a custom sell should occur, otherwise None
        """

        if ((self.mgm_config['unclogger_spaces']['unclogger_enabled'] is
             True) and (pair in self.custom_info['open_trades']) and (self.custom_info['open_trades'][pair] != {})):
            # Initialize some re-occurring logging strings
            abort = 'No unclogging needed! '
            proceed = ' Proceeding to the next check!'
            otu = 'Open Trade Unclogger'
            cis = 'custom_sell - Custom Information Storage'
            su = 'sell___unclogger_'

            try:
                # Open Trade Custom Information Storage
                # -------------------------------------
                # Fetch all open trade data depending on RunMode
                all_open_trades = self.get_all_current_open_trades(trade)
                # Check if everything in custom_storage is up to date with all_open_trades
                if len(all_open_trades) > len(self.custom_info['open_trades']):
                    self.mgm_logger('warning', cis, f'Open trades ({str(len(self.custom_info["open_trades"]))}) in '
                                                    f'custom_storage do not match yet with trades in live open trades '
                                                    f'({str(len(all_open_trades))}) aborting unclogger for now!')
                    return None  # By default we don't want a force sell to occurs

                # Open Trade Unclogger
                # --------------------
                self.mgm_logger('debug', otu, 'Running trough all checks to see if unclogging is needed')
                # Check if there are enough losing trades open for unclogging to occur
                self.mgm_logger('debug', otu,
                                'Fetching all currently losing_open_trades from custom information storage')
                losing_open_trades = {}
                for stored_trade in self.custom_info['open_trades']:
                    stored_current_profit = self.custom_info['open_trades'][stored_trade]['current_profit']
                    if stored_current_profit < 0:
                        if pair not in losing_open_trades:
                            losing_open_trades[str(stored_trade)] = {}
                        losing_open_trades[str(stored_trade)] = stored_current_profit
                self.mgm_logger('debug', otu, f'Fetched losing_open_trades ({str(len(losing_open_trades))}) '
                                              f'from custom information storage!')

                minimal_losing_trades_open = self.get_param_value(f'{su}minimal_losing_trades_open')
                if len(losing_open_trades) < minimal_losing_trades_open:
                    self.mgm_logger('debug', otu, f'{abort}Not enough losing trades currently open!')
                    return None  # By default we don't want a force sell to occur
                self.mgm_logger('debug', otu, f'Enough losing trades detected!{proceed}')

                # Check if there is a losing trade open for the pair currently being ran through the MoniGoMani
                if pair not in losing_open_trades:
                    self.mgm_logger('debug', otu, f'{abort}Currently checked pair ({pair}) is not '
                                                  f'making a loss at this point in time!')
                    return None  # By default we don't want a force sell to occur
                self.mgm_logger('debug', otu, f'Currently checked pair ({pair}) is losing!{proceed}')

                trade_open_time = trade.open_date_utc.replace(tzinfo=None)
                self.mgm_logger('debug', otu, f'Trade open time: {str(trade_open_time)}')

                min_losing_trade_duration = self.get_param_value(f'{su}minimal_losing_trade_duration_minutes')
                minimal_open_time = (current_time.replace(tzinfo=None) - timedelta(minutes=min_losing_trade_duration))

                self.mgm_logger('debug', otu, f'Minimal open time: {str(minimal_open_time)}')

                if trade_open_time > minimal_open_time:
                    self.mgm_logger('debug', otu, f'{abort}Currently checked pair ({pair}) has not '
                                                  f'been open been open for long enough!')
                    return None  # By default we don't want a force sell to occur
                self.mgm_logger('debug', otu, f'Trade has been open for long enough!{proceed}')

                # Check if total open trades losing % is met
                percentage_open_trades_losing = int((len(losing_open_trades) / len(all_open_trades)) * 100)
                self.mgm_logger('debug', otu, f'percentage_open_trades_losing: {str(percentage_open_trades_losing)}%')
                trades_losing_percentage_needed = self.get_param_value(f'{su}open_trades_losing_percentage_needed')
                if percentage_open_trades_losing < trades_losing_percentage_needed:
                    self.mgm_logger('debug', otu,
                                    f'{abort}Percentage of open trades losing needed has not been satisfied!')
                    return None  # By default we don't want a force sell to occur
                self.mgm_logger('debug', otu, f'Percentage of open trades losing needed has been satisfied!{proceed}')

                # Fetch current dataframe for the pair currently being ran through MoniGoMani
                trend_lookback_candles_window = self.get_param_value(f'{su}trend_lookback_candles_window')
                self.mgm_logger('debug', otu, f'Fetching currently needed "trend" dataframe data to check how pair '
                                              f'({pair}) has been doing in during the last '
                                              f'{str(trend_lookback_candles_window)} candles')

                # Fetch all needed 'trend' trade data
                stored_trend_dataframe = self.get_unclogger_trade_trend_data(pair=pair, current_time=current_time)

                # Check if enough trend data has been stored to do the next check
                if len(stored_trend_dataframe) < trend_lookback_candles_window:
                    self.mgm_logger('debug', otu, f'{abort}Not enough trend data stored yet!')
                    return None  # By default we don't want a force sell to occur

                # Print all fetched 'trend' trade data
                self.mgm_logger('debug', otu, f'All needed "trend" trade data '
                                              f'({str(len(stored_trend_dataframe))}) fetched!')
                self.mgm_logger('debug', otu, f'stored_trend_dataframe contents: {repr(stored_trend_dataframe)}')

                # Check if the currently detected trend is positive
                negative_trend = True
                for trend in self.mgm_trends:
                    if ((self.mgm_config['unclogger_spaces'][f'unclogger_trend_lookback_window_uses_{trend}_candles']
                         is False) & (stored_trend_dataframe[1] == trend)):
                        negative_trend = False
                        break

                if negative_trend is False:
                    self.mgm_logger('debug', otu, f'{abort}Positive trend currently detected!')
                    return None  # By default we don't want a force sell to occur

                # Check if open_trade's trend changed negatively during past X candles
                self.mgm_logger('debug', otu, f'Calculating amount of unclogger_trend_lookback_candles_window '
                                              f'"satisfied" for pair: {pair}')

                unclogger_weighted_candles_satisfied = 0
                for lookback_candle in range(1, trend_lookback_candles_window + 1):
                    for trend in self.mgm_trends:
                        if (self.mgm_config['unclogger_spaces'][f'unclogger_trend_lookback_window_uses_{trend}_candles'
                        ] & (stored_trend_dataframe[lookback_candle] == trend)):
                            unclogger_weighted_candles_satisfied += (
                                self.separator - (lookback_candle * self.separator_candle_weight_reducer))
                self.mgm_logger('debug', otu, f'Amount of unclogger_trend_lookback_candles_window "satisfied": '
                                              f'{str(unclogger_weighted_candles_satisfied)} for pair: {pair}')

                # Calculate the percentage of the lookback window currently satisfied
                unclogger_candles_percentage_satisfied = (unclogger_weighted_candles_satisfied /
                                                          trend_lookback_candles_window) * 100

                # Override Sell Signal: Unclog trade by forcing a sell & attempt to continue
                # the profit climb with the "freed up trading slot"
                trend_lookback_candles_window_percentage_needed = self.get_param_value(
                    f'{su}trend_lookback_candles_window_percentage_needed')
                if unclogger_candles_percentage_satisfied >= trend_lookback_candles_window_percentage_needed:
                    # Buy Cooldown Window Custom Information Storage
                    if pair not in self.custom_info['unclogger_cooldown_pairs']:
                        self.custom_info['unclogger_cooldown_pairs'][pair] = []

                    buy_cooldown_minutes_window = self.get_param_value(f'{su}buy_cooldown_minutes_window')
                    self.custom_info['unclogger_cooldown_pairs'][pair].append({
                        'start_time': current_time,
                        'end_time': current_time + timedelta(minutes=buy_cooldown_minutes_window)
                    })

                    self.mgm_logger('info', otu, 'Unclogging losing trade...')
                    return 'MGM_unclogging_losing_trade'
                else:
                    self.mgm_logger('info', otu, 'No need to unclog open trade...')

            except Exception as e:
                self.mgm_logger('error', otu, f'Following error has occurred: {str(e)}')

        return None  # By default we don't want a force sell to occur

    def convert_candle_time(self, current_time: datetime, current_candle: int = 1) -> datetime:
        """
        Converts the current_time to a candle_time (of an informative_timeframe candle size),
        which can be used to query the dataframe

        :param current_time: (datetime) Current time object
        :param current_candle: (int) Amount of candles to offset (look back) from the current_time
        :return: (datetime) Converted candle time object
        """
        # Convert the candle time to the one being used by the 'informative_timeframe'
        candle_multiplier = int(self.informative_timeframe.rstrip('mhdwM'))
        candle_time = (timeframe_to_prev_date(self.informative_timeframe, current_time) -
                       timedelta(minutes=int(current_candle * candle_multiplier)))
        if self.informative_timeframe.find('h') != -1:
            candle_time = (timeframe_to_prev_date(self.informative_timeframe, current_time) -
                           timedelta(hours=int(current_candle * candle_multiplier)))
        elif self.informative_timeframe.find('d') != -1:
            candle_time = (timeframe_to_prev_date(self.informative_timeframe, current_time) -
                           timedelta(days=int(current_candle * candle_multiplier)))
        elif self.informative_timeframe.find('w') != -1:
            candle_time = (timeframe_to_prev_date(self.informative_timeframe, current_time) -
                           timedelta(weeks=int(current_candle * candle_multiplier)))
        elif self.informative_timeframe.find('M') != -1:
            candle_time = (timeframe_to_prev_date(self.informative_timeframe, current_time) -
                           timedelta64(int(current_candle * candle_multiplier), 'M'))

        return candle_time

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, **kwargs) -> bool:
        """
        Open Trade Unclogger Buy Cooldown Window
        ----------------------------------------
        Override Buy Signal - Cancels out a buy order when all of the following are fulfilled:
            - The Open Trade Unclogger is enabled
            - The Buy Cooldown Window set into place after unclogging said losing pair has not expired yet

        Timing for this function is critical, it's needed to avoid doing heavy tasks or network requests in this method.

        :param pair: Pair that's about to be bought.
        :param order_type: Order type (as configured in order_types). usually limit or market.
        :param amount: Amount in target (quote) currency that's going to be traded.
        :param rate: Rate that's going to be used when using limit orders
        :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return bool: When True is returned, then the buy-order is placed on the exchange. False aborts the process
        """

        uc = 'Unclogger Cooldown'
        n = '\n    '

        if ((self.mgm_config['unclogger_spaces']['unclogger_enabled'] is
             True) and (pair in self.custom_info['unclogger_cooldown_pairs'])):
            for cooldown_period in self.custom_info['unclogger_cooldown_pairs'][pair][:]:
                self.mgm_logger('debug', uc, f'{pair} CoolDown Period:'
                                             f'{n}Cooldown Start Time: {cooldown_period["start_time"]}'
                                             f'{n}Cooldown End Time: {cooldown_period["end_time"]}'
                                             f'{n}Current Time: {current_time}')

                if cooldown_period['end_time'] < current_time:
                    self.mgm_logger('debug', uc, f'Cooldown period for unclogged pair ({pair}) has expired, '
                                                 f'removing from custom_info! (CurrentTime: {current_time})')
                    self.custom_info['unclogger_cooldown_pairs'][pair].remove(cooldown_period)
                elif cooldown_period['start_time'] < current_time < cooldown_period['end_time']:
                    self.mgm_logger('debug', uc, 'Blocking buy signal since pair is cooling down...')
                    return False  # Block the buy signal from going through when the pair is still under cooldown

        return True  # Allow the buy signal to go through if the pair is not under cooldown

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, sell_reason: str,
                           current_time: datetime, **kwargs) -> bool:
        """
        Weighted Signals Sell Profit Only
        ---------------------------------
        Override Sell Signal - Configurable setting, if enabled
        weighted sell signals require to be profitable to go through.

        Timing for this function is critical, it's needed to avoid doing heavy tasks or network requests in this method.

        :param pair: Pair that's about to be sold.
        :param trade: trade object.
        :param order_type: Order type (as configured in order_types). usually limit or market.
        :param amount: Amount in quote currency.
        :param rate: Rate that's going to be used when using limit orders
        :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
        :param sell_reason: Sell reason, can be any of ['MGM_unclogging_losing_trade', 'sell_signal', 'force_sell',
            'emergency_sell', 'roi', 'stop_loss', 'stoploss_on_exchange', 'trailing_stop_loss']
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return bool: When True is returned, then the sell-order is placed on the exchange. False aborts the process
        """

        # Check if weighted signal is profitable if sell_profit_only is enabled in the weighted_signal_spaces
        if ((self.mgm_config['weighted_signal_spaces']['sell_profit_only'] is
             True) and (sell_reason == 'sell_signal') and (trade.calc_profit_ratio(rate) < 0)):
            return False
        # Check if ROI is enabled for the currently detected trend
        elif sell_reason == 'roi':
            # Fetch the 'trend' data for the current candle
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            candle_time = self.convert_candle_time(current_time=current_time)
            candle_trend = dataframe.loc[dataframe['date'] == candle_time].squeeze()['trend']
            for mgm_trend in self.mgm_trends:
                roi_when_trend = getattr(self, f'roi_when_{mgm_trend}')
                if (mgm_trend == candle_trend) and (roi_when_trend is False):
                    return False

        return True  # By default we want the sell signal to go through

    def mgm_logger(self, message_type: str, code_section: str, message: str):
        """
        MoniGoMani Logger
        -----------------
        When passing a type and a message to this function it will log:
        - The timestamp of logging + the message_type provided + the message provided
        - To the console & To "./user_data/logs/freqtrade.log"

        :param message_type: The type of the message (INFO, DEBUG, WARNING, ERROR, CUSTOM)
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
            elif (self.mgm_log_levels_enabled['custom'] is True) and (message_type.upper() == 'CUSTOM'):
                logger.setLevel(logging.DEBUG)
                logger.debug(f'CUSTOM - {code_section} - {message}')

    def _generate_weight_condition(self, dataframe: DataFrame, space: str) -> DataFrame:
        """
        Generates the final condition that checks the weights per trend

        :param dataframe: DataFrame populated with indicators
        :param space: buy or sell space
        :return: Lambda conditions
        """

        number_of_weighted_signals = int(getattr(self, f'number_of_weighted_{space}_signals'))

        conditions_weight = []
        # If TimeFrame-Zooming => Only use 'informative_timeframe' data
        for trend in self.mgm_trends:
            if self.mgm_config['trading_during_trends'][f'{space}_trades_when_{trend}'] is True:
                corrected_totals = self.get_corrected_totals_needed(
                    space=space, trend=trend, number_of_weighted_signals=number_of_weighted_signals)

                conditions_weight.append(
                    (dataframe['trend'] == trend) &
                    (dataframe[f'total_{space}_signal_strength'] >= corrected_totals['signal_needed']) &
                    (dataframe[f'{space}_signals_triggered'] >= corrected_totals['triggers_needed']))

        return reduce(lambda x, y: x | y, conditions_weight)

    def get_corrected_totals_needed(self, space: str, trend: str, number_of_weighted_signals: int) -> dict:
        """
        Fetches a dictionary containing
        - Total Signal Weight Needed
        - Total Signal Triggers Needed
        for a given space and trend, these are the results of weak/strong overrides & dividing by precision

        :param space: (str) The 'buy' or 'sell' space
        :param trend: (str) 'upwards', 'sideways', 'downwards'
        :param number_of_weighted_signals: Number of signals for the given space
        :return: (dict) {'signal_needed', 'triggers_needed'}
        """
        total_signal_needed = getattr(self, f'{space}__{trend}_trend_total_signal_needed')
        total_triggers_needed = getattr(self, f'{space}__{trend}_trend_signal_triggers_needed')

        corrected_total_signal_needed = self.apply_weak_strong_overrides(
            parameter_value=total_signal_needed.value,
            parameter_min_value=self.min_trend_total_signal_needed_value,
            parameter_max_value=self.max_weighted_signal_value * number_of_weighted_signals,
            parameter_threshold=self.search_threshold_weighted_signal_values
        ) / self.precision

        corrected_total_triggers_needed = self.apply_weak_strong_overrides(
            parameter_value=total_triggers_needed.value,
            parameter_min_value=self.min_trend_signal_triggers_needed_value,
            parameter_max_value=number_of_weighted_signals,
            parameter_threshold=self.search_threshold_trend_signal_triggers_needed
        ) / self.precision

        return {'signal_needed': corrected_total_signal_needed, 'triggers_needed': corrected_total_triggers_needed}

    def apply_weak_strong_overrides(self, parameter_value,
                                    parameter_min_value, parameter_max_value, parameter_threshold):
        """
        Applies HyperOptable parameter overrides to weak and strong signals
        at the outer bounds of the search space or below/above it

        :param parameter_value: Value used for the parameter
        :param parameter_min_value: Minimum value used in the HyperOpt space of the parameter
        :param parameter_max_value: Maximum value used in the HyperOpt space of the parameter
        :param parameter_threshold: Threshold value used for the parameter
        :return: parameter_value if no override was needed, otherwise overridden weak/strong parameter value
        """

        # Apply parameter overrides to weak and strong signals where needed
        if parameter_value <= parameter_min_value + parameter_threshold:
            return parameter_min_value
        elif parameter_value >= parameter_max_value - parameter_threshold:
            return parameter_max_value
        else:
            return parameter_value

    def _add_signal(self, signal_name: str, signal_min_value: int, signal_max_value: int, signal_threshold: int,
                    space: str, dataframe: DataFrame, condition: Any):
        """
        # Weighted Variables
        # ------------------
        Calculates the weight of each signal, also adds the signal to the dataframe if debugging is enabled.
        :param signal_name: Name of the signal to be added
        :param signal_min_value: Minimal search space value to use during
            the 1st HyperOpt Run and override value for weak signals
        :param signal_max_value: Maximum search space value to use during
            the 1st HyperOpt Run and override value for weak signals
        :param signal_threshold: Threshold to use for overriding weak/strong signals
            and setting up refined search spaces
        :param space: buy or sell
        :param dataframe: DataFrame populated with indicators
        :param condition: A valid condition to evaluate the signal
        :return: DataFrame with debug signals
        """

        # If TimeFrame-Zooming => Only use 'informative_timeframe' data
        has_multiplier = ((self.is_dry_live_run_detected is False) and
                          (self.informative_timeframe != self.backtest_timeframe))
        for trend in self.mgm_trends:
            if self.mgm_config['trading_during_trends'][f'{space}_trades_when_{trend}'] is True:
                parameter_name = f'{space}_{trend}_trend_{signal_name}_weight'
                signal_weight = getattr(self, parameter_name)

                # Apply signal overrides to weak and strong signals where needed
                signal_weight_value = self.apply_weak_strong_overrides(
                    signal_weight.value, signal_min_value, signal_max_value, signal_threshold)

                rolling_needed = getattr(self, f'{space}__{trend}_trend_total_signal_needed_candles_lookback_window')
                rolling_needed_value = (rolling_needed.value * self.timeframe_multiplier if has_multiplier
                                        else rolling_needed.value)

                # If debuggable weighted signal dataframe => Add individual per signal rows in the dataframe
                if self.debuggable_weighted_signal_dataframe:
                    if parameter_name not in dataframe.columns:
                        dataframe[parameter_name] = 0

                    dataframe.loc[((dataframe['trend'] == trend) & (condition.rolling(rolling_needed_value).sum() > 0)),
                                  parameter_name] = signal_weight_value / self.precision

                # If the weighted signal triggered => Add the weight to the totals needed in the dataframe
                dataframe.loc[((dataframe['trend'] == trend) & (condition.rolling(rolling_needed_value).sum() > 0)),
                              f'total_{space}_signal_strength'] += signal_weight_value / self.precision

                # If the weighted signal is bigger then 0 and triggered => Add up the amount of signals that triggered
                if signal_weight_value > 0:
                    dataframe.loc[((dataframe['trend'] == trend) & (condition.rolling(rolling_needed_value).sum() > 0)),
                                  f'{space}_signals_triggered'] += 1

                # Add found weights to comparison values to check if total signals utilized by HyperOpt are possible
                self.total_signals_possible[f'{space}_{trend}'] += signal_weight_value
                # Add a signal trigger if it is possible to compare if total triggers needed by HyperOpt are possible
                if signal_weight_value > 0:
                    self.total_triggers_possible[f'{space}_{trend}'] += 1

            # Override Signals: When configured sell/buy signals can be completely turned off for each kind of trend
            else:
                dataframe.loc[dataframe['trend'] == trend, space] = 0

        return dataframe

    @classmethod
    def register_signal_attr(cls, base_cls, name: str, space: str = 'buy') -> None:
        """
        Defines the optimizable parameters of each signal
        :param base_cls: The inheritor class of the MGM where the attributes will be added
        :param space: buy or sell
        :param name: Signal name
        :return: None
        """

        # Generating the attributes for each signal trend
        for trend in cls.mgm_trends:
            parameter_name = f'{trend}_trend_{name}_weight'
            if cls.mgm_config['trading_during_trends'][f'{space}_trades_when_{trend}'] is True:
                cls._init_vars(base_cls, space=space, parameter_name=parameter_name,
                               parameter_min_value=cls.min_weighted_signal_value,
                               parameter_max_value=cls.max_weighted_signal_value,
                               parameter_threshold=cls.search_threshold_weighted_signal_values,
                               precision=cls.precision, overrideable=True)

    @classmethod
    def _init_vars(cls, base_cls, space: str, parameter_name: str, parameter_min_value: int,
                   parameter_max_value: int, parameter_threshold: int, precision: float, overrideable: bool = True):
        """
        Function to automatically initialize MoniGoMani's HyperOptable parameter values for both HyperOpt Runs.
        :param base_cls: The inheritor class of the MGM where the attributes will be added
        :param space: Buy or Sell params dictionary
        :param parameter_name: Name of the signal in the dictionary
        :param parameter_min_value: Minimal search space value to use during
            the 1st HyperOpt Run and override value for weak signals
        :param parameter_max_value: Maximum search space value to use during
            the 1st HyperOpt Run and override value for weak signals
        :param parameter_threshold: Threshold to use for overriding weak/strong signals
            and setting up refined search spaces after the 1st HyperOpt Run
        :param precision: Precision used while HyperOpting
        :param overrideable: Allow value to be overrideable or not (defaults to 'True')
        :return: None
        """

        # Narrow the search spaces for overrideable parameters by default
        override_parameter_min_value = parameter_min_value
        override_parameter_max_value = parameter_max_value
        if overrideable is True:
            parameter_min_value = parameter_min_value + parameter_threshold
            parameter_max_value = parameter_max_value - parameter_threshold

        parameter_dictionary = getattr(cls, f'{space}_params')
        parameter_key = f'{space}_{parameter_name}'
        parameter_value = parameter_dictionary.get(parameter_key)
        # 1st HyperOpt Run: Use provided min/max values for the search spaces
        if parameter_value is None:
            min_value = parameter_min_value
            max_value = parameter_max_value
        # 2nd HyperOpt Run: Use refined search spaces where needed
        else:
            if overrideable is False:
                min_value = (parameter_min_value if parameter_value <= (parameter_min_value + parameter_threshold)
                             else parameter_value - parameter_threshold)
                max_value = (parameter_max_value if parameter_value >= (parameter_max_value - parameter_threshold)
                             else parameter_value + parameter_threshold)
            # Apply different logic for overridable signals
            else:
                # Override search space min_value bounds if value is going to be overridden
                if parameter_value <= parameter_min_value:
                    min_value = override_parameter_min_value
                # Limit search space min_value to not go too low
                elif (parameter_value - parameter_threshold) < parameter_min_value:
                    min_value = parameter_min_value
                # Otherwise just refine the search space
                else:
                    min_value = parameter_value - parameter_threshold

                # Override search space max_value bounds if value is going to be overridden
                if parameter_value >= parameter_max_value:
                    max_value = override_parameter_max_value
                # Limit search space max_value to not go too high
                elif (parameter_value + parameter_threshold) > parameter_max_value:
                    max_value = parameter_max_value
                # Otherwise just refine the search space
                else:
                    max_value = parameter_value + parameter_threshold

        # 1st HyperOpt Run: Use middle of min/max values as default value
        if parameter_value is None:
            default_value = int((parameter_min_value + parameter_max_value) / 2)
        # 2nd HyperOpt Run: Use Overrides where needed for default value
        elif (max_value == parameter_max_value) and (overrideable is True) and (parameter_value >= parameter_max_value):
            default_value = override_parameter_max_value
        elif (min_value == parameter_min_value) and (overrideable is True) and (parameter_value <= parameter_min_value):
            default_value = override_parameter_min_value
        # 2nd HyperOpt Run: Use values found in Run 1 for the remaining default values
        else:
            default_value = parameter_value

        # 2nd HyperOpt Run: Apply Overrides where needed
        if (parameter_value is not None) and (overrideable is True):
            if default_value == override_parameter_min_value or default_value == override_parameter_max_value:
                optimize = False
            else:
                optimize = True
        # 1st HyperOpt Run or not overridable, just optimize without overrides
        else:
            optimize = True

        parameter_config = {
            'min_value': int(min_value * precision),
            'max_value': int(max_value * precision),
            'default_value': int(default_value * precision),
            # 1st HyperOpt Run: No overrides, 2nd HyperOpt Run: Apply Overrides where needed
            'optimize': optimize
        }

        parameter_dictionary[parameter_key] = parameter_config['default_value']
        param = IntParameter(low=parameter_config['min_value'], high=parameter_config['max_value'],
                             default=parameter_config['default_value'], space=space,
                             optimize=parameter_config['optimize'], load=True)
        setattr(base_cls, parameter_key, param)

    @classmethod
    def init_util_params(cls, base_cls):
        """
         Generates custom utility parameters used by:
         - trading_during_trends
         - weighted_signal_spaces
         - unclogger_spaces
         :param base_cls: The inheritor class of the MGM where the attributes will be added
        """

        # Generates the utility attributes for the unclogger_spaces
        for param_key in cls.mgm_unclogger_add_params:
            parameter_name = '__' + param_key
            param_config = cls.mgm_unclogger_add_params[param_key]
            if isinstance(param_config, dict) is True:
                param_config['threshold'] = (param_config['threshold'] if 'threshold' in param_config
                                             else cls.search_threshold_weighted_signal_values)

                cls._init_vars(base_cls=base_cls, space='sell', parameter_name=parameter_name,
                               parameter_min_value=param_config['min'], parameter_max_value=param_config['max'],
                               parameter_threshold=param_config['threshold'],
                               precision=cls.precision, overrideable=False)

        # Generate the utility attributes for the logic of the weighted_signal_spaces
        for trend in cls.mgm_trends:
            for space in ['buy', 'sell']:
                if cls.mgm_config['trading_during_trends'][f'{space}_trades_when_{trend}'] is True:
                    param_total_signal_needed = f'_{trend}_trend_total_signal_needed'
                    number_of_weighted_signals = int(getattr(cls, f'number_of_weighted_{space}_signals'))
                    cls._init_vars(base_cls=base_cls, space=space, parameter_name=param_total_signal_needed,
                                   parameter_min_value=cls.min_trend_total_signal_needed_value,
                                   parameter_max_value=int(cls.max_weighted_signal_value * number_of_weighted_signals),
                                   parameter_threshold=cls.search_threshold_weighted_signal_values,
                                   precision=cls.precision, overrideable=True)

                    param_needed_candles_lookback_window = f'_{trend}_trend_total_signal_needed_candles_lookback_window'
                    cls._init_vars(base_cls=base_cls, space=space, parameter_name=param_needed_candles_lookback_window,
                                   parameter_min_value=cls.min_trend_total_signal_needed_candles_lookback_window_value,
                                   parameter_max_value=cls.max_trend_total_signal_needed_candles_lookback_window_value,
                                   parameter_threshold=
                                   cls.search_threshold_trend_total_signal_needed_candles_lookback_window_value,
                                   precision=cls.precision, overrideable=False)

                    param_signal_triggers_needed = f'_{trend}_trend_signal_triggers_needed'
                    cls._init_vars(base_cls=base_cls, space=space, parameter_name=param_signal_triggers_needed,
                                   parameter_min_value=cls.min_trend_signal_triggers_needed_value,
                                   parameter_max_value=number_of_weighted_signals,
                                   parameter_threshold=cls.search_threshold_trend_signal_triggers_needed,
                                   precision=cls.precision, overrideable=True)

    @staticmethod
    def generate_mgm_attributes(buy_signals, sell_signals):
        """
        Method used to generate the decorator for the MoniGoMani Framework,
        responsible for adding attributes at the class level

        :param buy_signals: Dictionary consisting of key as signal name and value containing
            the function that will generate the condition in the dataframe.
        :param sell_signals: Dictionary consisting of key as signal name and value containing
            the function that will generate the condition in the dataframe.
        :return: A function that will be used in the class that inherits the MGM to decorate it
        """

        # The method responsible for decorating the base class, receives the class itself as a parameter.
        # It will be set as the decorator of the base class
        def apply_attributes(base_cls):

            # Set all signs in the class for later use.
            setattr(base_cls, 'buy_signals', buy_signals)
            setattr(base_cls, 'sell_signals', sell_signals)

            # Set number of weighted buy/sell signals for later use.
            setattr(base_cls, 'number_of_weighted_buy_signals', len(buy_signals))
            setattr(base_cls, 'number_of_weighted_sell_signals', len(sell_signals))

            # Sets the useful parameters of the MGM, such as unclogger and etc
            base_cls.init_util_params(base_cls)

            # Registering signals attributes on class
            for name in buy_signals:
                base_cls.register_signal_attr(base_cls, name, 'buy')

            for name in sell_signals:
                base_cls.register_signal_attr(base_cls, name, 'sell')

            return base_cls

        return apply_attributes

    def _populate_trend(self, space: str, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the trend dataframe with the conditional that checks the weights
        :param space: buy or sell
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with debug signals
        """

        # Reset some parameters when a new BackTest starts (during HyperOpting)
        if (self.is_dry_live_run_detected is False) and (space == 'buy'):
            self.init_hyperopt_epoch()

        # Initialize total signal and signals triggered columns (should be 0 = false by default)
        if 'total_buy_signal_strength' not in dataframe.columns:
            dataframe['total_buy_signal_strength'] = dataframe['total_sell_signal_strength'] = 0
        if f'{space}_signals_triggered' not in dataframe.columns:
            dataframe[f'{space}_signals_triggered'] = 0

        # Fetch the weighted signals used + their min/max search space values and threshold used
        signals = getattr(self, f'{space}_signals')
        signal_min_value = self.mgm_config['weighted_signal_spaces']['min_weighted_signal_value']
        signal_max_value = self.mgm_config['weighted_signal_spaces']['max_weighted_signal_value']
        signal_threshold = self.mgm_config['weighted_signal_spaces']['search_threshold_weighted_signal_values']

        # Calculates the weight and/or generates the debug column for each signal
        for signal_name, condition_func in signals.items():
            self._add_signal(signal_name=signal_name, signal_min_value=signal_min_value,
                             signal_max_value=signal_max_value, signal_threshold=signal_threshold,
                             space=space, dataframe=dataframe, condition=condition_func(dataframe))

        # Generates the conditions responsible for searching and comparing the weights needed to activate a buy or sell
        dataframe.loc[self._generate_weight_condition(dataframe=dataframe, space=space), space] = 1

        # Check if total signals needed & triggers needed are possible, if not force the bot to do nothing
        number_of_weighted_signals = int(getattr(self, f'number_of_weighted_{space}_signals'))
        if self.is_dry_live_run_detected is False:
            for trend in self.mgm_trends:
                if self.mgm_config['trading_during_trends'][f'{space}_trades_when_{trend}'] is True:
                    corrected_totals = self.get_corrected_totals_needed(
                        space=space, trend=trend, number_of_weighted_signals=number_of_weighted_signals)

                    if ((self.total_signals_possible[f'{space}_{trend}'] < corrected_totals['signal_needed']) or
                        (self.total_triggers_possible[f'{space}_{trend}'] < corrected_totals['triggers_needed'])):
                        dataframe['buy'] = dataframe['sell'] = 0

        return dataframe

    def init_hyperopt_epoch(self) -> None:
        """
        Re-Initialize some parameters specifically for a new HyperOpt epoch

        Necessary because 'joblib' will only do a clean initialization
        of the MGM framework during the first iteration/batch of epochs.
        """

        # Reset the total signals and triggers possible
        for trend in self.mgm_trends:
            for space in ['buy', 'sell']:
                self.total_signals_possible[f'{space}_{trend}'] = 0
                self.total_triggers_possible[f'{space}_{trend}'] = 0

        # Reset the custom_info dictionary when a new BackTest starts (during HyperOpting) if needed
        if self.custom_info != self.initial_custom_info:
            self.custom_info = copy.deepcopy(self.initial_custom_info)

        # Re-calculate the 'separator_candle_weight_reducer' if the unclogger is enabled
        if self.mgm_config['unclogger_spaces']['unclogger_enabled'] is True:
            self.separator = self.mgm_config['unclogger_spaces'][
                'unclogger_trend_lookback_candles_window_recent_past_weight_separator']
            separator_window = (self.separator / 1) - (1 / self.separator)
            self.separator_candle_weight_reducer = separator_window / self.get_param_value(
                'sell___unclogger_trend_lookback_candles_window')
