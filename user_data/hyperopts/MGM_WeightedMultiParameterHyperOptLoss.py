# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
from datetime import datetime
from typing import Any, Dict

from pandas import DataFrame

from freqtrade.data.btanalysis import calculate_max_drawdown
from freqtrade.optimize.hyperopt import IHyperOptLoss


# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------


class MGM_WeightedMultiParameterHyperOptLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame], backtest_stats: Dict[str, Any],
                               *args, **kwargs) -> float:
        """
        MGM_WeightedMultiParameterHyperOptLoss Customizable HyperOpt Objective function.
        Returns smaller number for better results.

        Considers various metrics from the HyperOpt output table to fine-tune for a more robust strategy configuration!
        All configurable setting sections: (total_trades, win_ratio, average_profit,
        total_profit, average_duration, max_drawdown) can be found in MoniGoMani's
        'mgm-config' under the ['monigomani_hyperoptloss_settings']['MGM_WeightedMultiParameterHyperOptLoss'] section.

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

        # Load the MoniGoMani config files and MGM_WeightedMultiParameterHyperOptLoss Settings
        weighted_hyperopt_loss_settings = config['monigomani_hyperoptloss_settings']

        # Calculate the Win Ratio
        win_ratio = (len(results[results['profit_ratio'] > 0]) / trade_count) * 100
        # Calculate the Average Profit
        average_profit = results['profit_ratio'].mean() * 100
        # Calculate the Total Profit
        total_profit = (results['profit_abs'].sum() / config['dry_run_wallet']) * 100
        # Calculate the Average Trade Duration
        average_trade_duration = results['trade_duration'].mean()
        if average_trade_duration is None:
            average_trade_duration = 0
        # Calculate the Max DrawDown
        try:
            max_drawdown, _, _, _, _ = calculate_max_drawdown(results, value_col='profit_ratio')
            max_drawdown *= 100
        except ValueError:
            max_drawdown = 0

        # Calculates Current Amount of Trades Weight - Lower is better
        total_trades_objective = MGM_WeightedMultiParameterHyperOptLoss.calculate_current_weight(
            parameter_name='total_trades', parameter_settings=weighted_hyperopt_loss_settings['total_trades'],
            parameter_value=trade_count, optimize_direction='lower')

        # Calculates Current Win Ratio Weight - Higher is better
        win_ratio_objective = MGM_WeightedMultiParameterHyperOptLoss.calculate_current_weight(
            parameter_name='win_ratio', parameter_settings=weighted_hyperopt_loss_settings['win_ratio'],
            parameter_value=win_ratio, optimize_direction='higher')

        # Calculates Current Average Profit Weight - Higher is better
        average_profit_objective = MGM_WeightedMultiParameterHyperOptLoss.calculate_current_weight(
            parameter_name='average_profit', parameter_settings=weighted_hyperopt_loss_settings['average_profit'],
            parameter_value=average_profit, optimize_direction='higher')

        # Calculates Current Profit Weight - Higher is better
        total_profit_objective = MGM_WeightedMultiParameterHyperOptLoss.calculate_current_weight(
            parameter_name='total_profit', parameter_settings=weighted_hyperopt_loss_settings['total_profit'],
            parameter_value=total_profit, optimize_direction='higher')

        # Calculates Current Average Trade Duration Weight - Lower is better
        average_duration_objective = MGM_WeightedMultiParameterHyperOptLoss.calculate_current_weight(
            parameter_name='average_duration', parameter_settings=weighted_hyperopt_loss_settings['average_duration'],
            parameter_value=average_trade_duration, optimize_direction='lower')

        # Calculates Current Max DrawDown Weight - Lower is better
        max_drawdown_objective = MGM_WeightedMultiParameterHyperOptLoss.calculate_current_weight(
            parameter_name='max_drawdown', parameter_settings=weighted_hyperopt_loss_settings['max_drawdown'],
            parameter_value=max_drawdown, optimize_direction='lower')

        # Calculate the Total Objective used by HyperOpt
        total_objective = (total_trades_objective + win_ratio_objective + average_profit_objective +
                           total_profit_objective + average_duration_objective + max_drawdown_objective)

        # If enabled, log the found values to the console
        if (config['monigomani_settings']['use_mgm_logging'] is True) and (config['monigomani_settings']
                                                                           ['mgm_log_levels_enabled']['info'] is True):
            rnd = lambda parameter: str(round(parameter, 2))
            line = '\n    {:<35s} | Weighted Objective: {:<30s}'
            total_line = '\n    {:<35s} | Total Objective: {:<30s}'

            print(
                f'INFO - MGM_WeightedMultiParameterHyperOptLoss Values Found:'
                f'{line.format(f"Total Trades: {trade_count}", rnd(total_trades_objective))}'
                f'{line.format(f"Win Ratio: {rnd(win_ratio)}%", rnd(win_ratio_objective))}'
                f'{line.format(f"Average Profit: {rnd(average_profit)}%", rnd(average_profit_objective))}'
                f'{line.format(f"Total Profit: {rnd(total_profit)}%", rnd(total_profit_objective))}'
                f'{line.format(f"Average Duration: {rnd(average_trade_duration)}%", rnd(average_duration_objective))}'
                f'{line.format(f"Max DrawDown: {rnd(max_drawdown)}%", rnd(max_drawdown_objective))}'
                f'{total_line.format("", rnd(total_objective))}')

        # Return the Total Objective found
        return total_objective

    @staticmethod
    def calculate_current_weight(parameter_name: str, parameter_settings: dict,
                                 parameter_value: float, optimize_direction: str) -> float:
        """
        Calculates the Objective Weight for the Current Parameter (Lower - More negative objective is better)

        HyperOpt is punished if the found parameter value is not in between the defined low/high threshold values,
        the farther off the expected value, the harder the punishment.
        HyperOpt is rewarded if the found parameter value is between the defined low/high threshold values,
        giving more rewards regarding the optimize direction.

        :param parameter_name: Name of the current parameter
        :param parameter_settings: Dictionary with settings for the parameter loaded from 'mgm-config'.
        :param parameter_value: Current Base Value used in the calculation of the Objective Weight for the Parameter.
        :param optimize_direction: The direction in which reward optimization is preferred ('lower' or 'higher')
        :return: The Objective Weight for the parameter defined in the class from where the function was called.
        """

        # Ignore the parameter value if it's found value or if it's weight is zero
        if (parameter_value == 0) or (parameter_settings[f'{parameter_name}_weight'] == 0):
            return 0

        # Append '_minutes' to the expected_parameter for the 'duration' parameter
        expected_parameter = (parameter_settings[f'expected_{parameter_name}'] if parameter_name != 'average_duration'
                              else parameter_settings[f'expected_{parameter_name}_minutes'])

        # Fetch the lower & upper bound of the reward/punishment window
        lower_bound = parameter_settings[f'{parameter_name}_threshold_low']
        upper_bound = parameter_settings[f'{parameter_name}_threshold_high']

        # Punish HyperOpt if the parameter value is way below or way above the expected parameter threshold values
        if (parameter_value < lower_bound) or (parameter_value > upper_bound):
            # Calculate the percentage off from the expected parameter
            parameter_objective_weight = (abs(expected_parameter - parameter_value) / expected_parameter) * 100
        # Reward the HyperOpt if the parameter is between the configured objective threshold low/high values
        else:
            # Calculate the window in which rewards are possible
            reward_window = upper_bound - lower_bound

            # Calculate the percentage of the reward window that is fulfilled (Max reward being 100, min 0)
            if optimize_direction == 'lower':
                parameter_objective_weight = - (abs(upper_bound - parameter_value) * 100) / reward_window
            else:  # 'higher'
                parameter_objective_weight = - (abs(lower_bound - parameter_value) * 100) / reward_window

        # Multiply with the weight of the objective to influence the HyperOpt more or less
        return parameter_objective_weight * (parameter_settings[f'{parameter_name}_weight'] / 100)
