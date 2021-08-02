# -*- coding: utf-8 -*-
# --- ↓ Do not remove these libs ↓ -------------------------------------------------------------------------------------
from datetime import datetime
from pandas import DataFrame

from freqtrade.data.btanalysis import calculate_max_drawdown
from freqtrade.optimize.hyperopt import IHyperOptLoss
from freqtrade.optimize.hyperopt_loss_sortino_daily import SortinoHyperOptLossDaily
# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------

# Sortino Settings
# ----------------
TARGET_TRADES = 4000
EXPECTED_MAX_PROFIT = 3.0
MAX_ACCEPTED_TRADE_DURATION = 1800
MIN_ACCEPTED_TRADE_DURATION = 2

# Loss settings
# -------------
AVERAGE_PROFIT_THRESHOLD = 1  # 2%

# Weight Settings
# ---------------
TOTAL_PROFIT_WEIGHT = 100
DRAWDOWN_WEIGHT = 75
WIN_LOSS_WEIGHT = 50
AVERAGE_PROFIT_WEIGHT = 20
DURATION_WEIGHT = 1
SORTINO_WEIGHT = 0.02

# Other Settings
# --------------
IGNORE_SMALL_PROFITS = False
SMALL_PROFITS_THRESHOLD = 0.001  # 0.1%


class GeniusLoss(IHyperOptLoss):
    """
    Defines custom loss function which consider various metrics to make more robust strategy.
    Adjust those weights to get more suitable results for your strategy

    WIN_LOSS_WEIGHT
    AVERAGE_PROFIT_WEIGHT
    AVERAGE_PROFIT_THRESHOLD - upper threshold of average profit to rely on (cut off crazy av.profits like 10%+)
    SORTINO_WEIGHT
    TOTAL_PROFIT_WEIGHT

    IGNORE_SMALL_PROFITS - this param allow to filter small profits (to take into consideration possible spread)
    """

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, min_date: datetime,
                               max_date: datetime, *args, **kwargs) -> float:
        """
        GeniusLoss Customizable HyperOpt Objective function. Tweak me to perfection!
        The smaller & more negative the returned Objective goes, the better your found results are.

        :param results: (DataFrame)
        :param trade_count: (int)
        :param min_date: (datetime)
        :param max_date: (datetime)
        :param max_date: (datetime)
        :param *args: Ensure to keep this here so updates to this won't break MoniGoMani.
        :param **kwargs: Ensure to keep this here so updates to this won't break MoniGoMani.
        :return success: (bool) True if files are created, false if something failed.
        Todo: Check if the example files exist
        """
        profit_threshold = 0

        if IGNORE_SMALL_PROFITS:
            profit_threshold = SMALL_PROFITS_THRESHOLD

        total_profit = results['profit_ratio'].sum()
        total_win = len(results[(results['profit_ratio'] > profit_threshold)])
        total_lose = len(results[(results['profit_ratio'] <= 0)])
        average_profit = results['profit_ratio'].mean() * 100
        sortino_ratio = SortinoHyperOptLossDaily.hyperopt_loss_function(results, trade_count, min_date,
                                                                        max_date, *args, **kwargs)
        trade_duration = results['trade_duration'].mean()

        max_drawdown = 100
        try:
            max_drawdown, _, _, _, _ = calculate_max_drawdown(results, value_col='profit_ratio')
        except:
            pass

        if total_lose == 0:
            total_lose = 1

        profit_loss = (1 - total_profit / EXPECTED_MAX_PROFIT) * TOTAL_PROFIT_WEIGHT
        win_lose_loss = (1 - (total_win / total_lose)) * WIN_LOSS_WEIGHT
        average_profit_loss = 1 - (min(average_profit, AVERAGE_PROFIT_THRESHOLD) * AVERAGE_PROFIT_WEIGHT)
        sortino_ratio_loss = SORTINO_WEIGHT * sortino_ratio
        drawdown_loss = max_drawdown * DRAWDOWN_WEIGHT
        duration_loss = DURATION_WEIGHT * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)

        result = profit_loss + win_lose_loss + average_profit_loss + sortino_ratio_loss + drawdown_loss + duration_loss

        return result
