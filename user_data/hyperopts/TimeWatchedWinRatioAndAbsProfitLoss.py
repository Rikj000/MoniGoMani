__author__ = "PoCk3T"
__copyright__ = "The GNU General Public License v3.0"

from datetime import datetime
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss


class TimeWatchedWinRatioAndAbsProfitLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int,
                               min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame],
                               *args, **kwargs) -> float:
        """
        Custom objective function, returns smaller number for better results
        """

        # results DataFrame: pair, profit_ratio, profit_abs, open_date,
        # open_rate, fee_open, close_date, close_rate, fee_close, amount,
        # trade_duration, is_open, sell_reason, stake_amount, min_rate, max_rate,
        # stop_loss_ratio, stop_loss_abs

        wins = len(results[results['profit_ratio'] > 0])
        abs_profit = results['profit_abs'].sum()
        trade_duration = results['trade_duration'].mean()

        win_ratio = wins / trade_count
        return -abs_profit * win_ratio / trade_duration * 10000
