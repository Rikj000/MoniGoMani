# -*- coding: utf-8 -*-
# --- ↓ Do not remove these libs ↓ -------------------------------------------------------------------------------------
from datetime import datetime
from pandas import DataFrame
from typing import Dict

from freqtrade.data.btanalysis import calculate_max_drawdown
from freqtrade.optimize.hyperopt import IHyperOptLoss
from freqtrade.optimize.hyperopt_loss_sortino_daily import SortinoHyperOptLossDaily
# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------


class MGM_GeniusHyperOptLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame], *args, **kwargs) -> float:
        """
        MGM_GeniusHyperOptLoss Customizable HyperOpt Objective function. Returns smaller number for better results.

        Considers various metrics to fine-tune for a more robust strategy configuration!
        All configurable Sortino, Weight & Other settings can be found in MoniGoMani's 'mgm-config' under
        the ['monigomani_hyperoptloss_settings']['MGM_GeniusHyperOptLoss'] section.

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
        Todo: Check if the example files exist
        ToDo: Implement
            - sortino_settings['target_trades']
            - sortino_settings['min_accepted_trade_duration']
        ToDo: After Freqtrade Update, Add: backtest_stats: Dict[str, Any],
            :param backtest_stats: Backtesting statistics using the same format as the backtesting file 'strategy'
                substructure. Available fields can be seen in generate_strategy_stats() in optimize_reports.py
        """

        # Load the MoniGoMani config files and MGM_GeniusHyperOptLoss Settings
        hyperopt_loss_settings = config['monigomani_hyperoptloss_settings']['MGM_GeniusHyperOptLoss']
        sortino_settings = hyperopt_loss_settings['sortino']
        weight_settings = hyperopt_loss_settings['weight']
        other_settings = hyperopt_loss_settings['other']

        # Calculate the Sortino Ratio & Try to calculate the Max DrawDown
        sortino_ratio = \
            SortinoHyperOptLossDaily.hyperopt_loss_function(results, trade_count, min_date, max_date, *args, **kwargs)

        try:
            max_drawdown, _, _, _, _ = calculate_max_drawdown(results, value_col='profit_ratio')
        except ValueError:
            max_drawdown = 0

        # Calculate the Average & Total Profit, Profit Threshold, Total Lose & Win, Average Trade Duration
        average_profit = results['profit_ratio'].mean() * 100
        profit_threshold = \
            other_settings['small_profits_threshold'] if other_settings['ignore_small_profits'] is True else 0
        total_profit = results['profit_ratio'].sum()
        total_lose = len(results[results['profit_ratio'] <= 0])
        total_lose = 1 if total_lose == 0 else total_lose
        total_win = len(results[results['profit_ratio'] > profit_threshold])
        trade_duration = results['trade_duration'].mean()

        # Calculate all of the individual weighted objectives depending on the configuration in 'mgm-config'
        average_profit_objective = 1 - (min(average_profit, other_settings[
            'average_profit_threshold']) * weight_settings['average_profit_weight'])
        drawdown_objective = max_drawdown * weight_settings['drawdown_weight']
        duration_objective = weight_settings['duration_weight'] * min(
            trade_duration / sortino_settings['max_accepted_trade_duration'], 1)
        profit_objective = (1 - total_profit / sortino_settings[
            'expected_max_profit']) * weight_settings['total_profit_weight']
        sortino_ratio_objective = weight_settings['sortino_weight'] * sortino_ratio
        win_lose_objective = (1 - (total_win / total_lose)) * weight_settings['win_loss_weight']

        total_objective = (average_profit_objective + drawdown_objective + duration_objective +
                           profit_objective + sortino_ratio_objective + win_lose_objective)

        # If enabled, log the found values to the console
        if (config['monigomani_settings']['use_mgm_logging'] is True) and \
                (config['monigomani_settings']['mgm_log_levels_enabled']['info'] is True):
            print(f'INFO - MGM_GeniusHyperOptLoss Values Found:\n'
                  f'    Average Profit: {average_profit} (Objective: {average_profit_objective})\n'
                  f'    Average Duration: {trade_duration} (Objective: {duration_objective})\n'
                  f'    DrawDown: {max_drawdown} (Objective: {drawdown_objective})\n'
                  f'    Sortino Ratio: {sortino_ratio} (Objective: {sortino_ratio_objective})\n'
                  f'    Total Profit: {total_profit} (Objective: {profit_objective})\n'
                  f'    Total Win/Lose: {total_win}/{total_lose} (Objective: {win_lose_objective})\n'
                  f'    Total Objective: {total_objective}')

        return total_objective
