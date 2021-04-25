__author__ = "PoCk3T"
__copyright__ = "The GNU General Public License v3.0"

from datetime import datetime
from typing import Dict

from freqtrade.optimize.hyperopt import IHyperOptLoss
from pandas import DataFrame


class UncloggedWinRatioAndProfitRatioLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int,
                               min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame],
                               *args, **kwargs) -> float:
        """
        Custom objective function, returns smaller number for better results

        This function optimizes for both: best profit AND stability

        On stability, the final score has an incentive, through 'win_ratio',
        to make more winning deals out of all deals done

        This might prove to be more reliable for dry and live runs of FreqTrade
        and prevent over-fitting on best profit only

        PLEASE NOTE: trades with losses between 0% to 1% (UNCLOGGER_PROFIT_RATIO_LOSS_TOLERANCE) 
        are ignored, as those are considered to be a by-product of the MGM un-clogger
        """

        UNCLOGGER_PROFIT_RATIO_LOSS_TOLERANCE = -1/100 # -1%

        wins = len(results[results['profit_ratio'] > 0])
        draws = len(results[results['profit_ratio'] == 0])
        losts_excluding_unclogger_ones = len(results[results['profit_ratio'] < UNCLOGGER_PROFIT_RATIO_LOSS_TOLERANCE])
        avg_profit = results['profit_ratio'].sum() * 100.0

        win_ratio = wins / (draws + losts_excluding_unclogger_ones)
        return -avg_profit * win_ratio * 100
