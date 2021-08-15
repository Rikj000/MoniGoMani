# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import os
from datetime import datetime
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss

from user_data.mgm_tools.mgm_hurry.LeetLogger import get_logger
from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli

logger = get_logger()
# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------

# Load the MoniGoMani config files and MGM_UncloggedWinRatioAndProfitRatioLoss Setting
mgm_config_files = MoniGoManiCli(os.getcwd(), logger).load_config_files()
# Percentage of loss to ignore while HyperOpting: -0.01 = Ignore trades with less then -1% loss
unclogger_profit_ratio_loss_tolerance = mgm_config_files['mgm-config']['monigomani_hyperoptloss_settings'][
    'MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss']['unclogger_profit_ratio_loss_tolerance']


class MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame], *args, **kwargs) -> float:
        """
        MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss Customizable HyperOpt Objective function.
        Returns smaller number for better results.

        This function optimizes for both: best profit & stability. On stability, the final score has an incentive,
        through 'win_ratio', to make more winning deals out of all deals done.
        This might prove to be more reliable for dry and live runs of FreqTrade
        and prevent over-fitting on best profit only.

        NOTE: Trades with losses between the 'unclogger_profit_ratio_loss_tolerance' are ignored,
        as those are considered to be a by-product of the MoniGoMani Unclogger. (Examples: 0% - 2%)
        This setting can be found in MoniGoMani's 'mgm-config' under the
        ['monigomani_hyperoptloss_settings']['MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss'] section.

        :param results: DataFrame containing the resulting trades. The following columns are available in results
            (corresponds to the output-file of backtesting when used with --export trades):
            pair, profit_ratio, profit_abs, open_date, open_rate, fee_open, close_date, close_rate, fee_close, amount,
            trade_duration, is_open, sell_reason, stake_amount, min_rate, max_rate, stop_loss_ratio, stop_loss_abs
        :param trade_count: Amount of trades that occurred during the current epoch (Identical to 'len(results)')
        :param min_date: Start date of the timerange used
        :param max_date: End date of the timerange used
        :param config: Config object used
            (Note: Not all strategy-related parameters will be updated here if they are part of a hyperopt space).
        :param processed: Dict of Dataframes with the pair as keys containing the data used for backtesting.
        :param args: Ensure to keep this here so updates to this won't break MoniGoMani.
        :param kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return float: HyperOpt Objective Value for the current epoch. The lower / more negative the better!
        ToDo: After Freqtrade Update, Add: backtest_stats: Dict[str, Any],
            :param backtest_stats: Backtesting statistics using the same format as the backtesting file 'strategy'
                substructure. Available fields can be seen in generate_strategy_stats() in optimize_reports.py
        """

        wins = len(results[results['profit_ratio'] > 0])
        draws = len(results[results['profit_ratio'] == 0])
        losing_trades_excluding_unclogger_ones = \
            len(results[results['profit_ratio'] < unclogger_profit_ratio_loss_tolerance])
        avg_profit = results['profit_ratio'].sum() * 100.0

        denominator = draws + losing_trades_excluding_unclogger_ones
        win_ratio = wins / denominator if denominator != 0 else 0
        return -avg_profit * win_ratio * 100
