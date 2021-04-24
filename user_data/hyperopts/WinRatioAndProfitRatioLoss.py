__author__ = "PoCk3T"
__copyright__ = "The GNU General Public License v3.0"

from datetime import datetime
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss


class WinRatioAndProfitRatioLoss(IHyperOptLoss):

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
        """        

        wins = len(results[results['profit_ratio'] > 0])
        avg_profit = results['profit_ratio'].sum() * 100.0

        win_ratio = wins / trade_count
        return -avg_profit * win_ratio * 100
