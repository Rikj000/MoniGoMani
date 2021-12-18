# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
from datetime import datetime
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss
# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------


class MGM_WinRatioAndProfitRatioHyperOptLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame], backtest_stats: Dict[str, Any],
                               *args, **kwargs) -> float:
        """
        MGM_WinRatioAndProfitRatioHyperOptLoss HyperOpt Objective function. Returns smaller number for better results.

        This function optimizes for both: best profit & stability. On stability, the final score has an incentive,
        through 'win_ratio', to make more winning deals out of all deals done.
        This might prove to be more reliable for dry and live runs of FreqTrade
        and prevent over-fitting on best profit only.

        It will also punish the HyperOpt if the trades found in an epoch are below the configured
        'total_trades_threshold_low' as a way to prevent over-fitting on too low trades with too high average duration.

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
        :param backtest_stats: Backtesting statistics using the same format as the backtesting file 'strategy'
            substructure. Available fields can be seen in generate_strategy_stats() in optimize_reports.py
        :param args: Ensure to keep this here so updates to this won't break MoniGoMani.
        :param kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return float: HyperOpt Objective Value for the current epoch. The lower / more negative the better!
        """

        if trade_count >= config['monigomani_hyperoptloss_settings']['total_trades']['total_trades_threshold_low']:
            wins = len(results[results['profit_ratio'] > 0])
            avg_profit = results['profit_ratio'].sum() * 100.0

            win_ratio = wins / trade_count
            return -avg_profit * win_ratio * 100
        else:
            # Punish HyperOpt if the total trade count is under the threshold_low value
            return 10000
