__author__ = "PoCk3T"
__copyright__ = "The GNU General Public License v3.0"

import pdb
from datetime import datetime
from math import exp
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
    """

    # results DataFrame: pair, profit_ratio, profit_abs, open_date,
    # open_rate, fee_open, close_date, close_rate, fee_close, amount,
    # trade_duration, is_open, sell_reason, stake_amount, min_rate, max_rate,
    # stop_loss_ratio, stop_loss_abs

    wins = len(results[results['profit_ratio'] > 0])
    avg_profit = results['profit_ratio'].mean() * 100.0

    win_ratio = wins/trade_count
    return -avg_profit*win_ratio*100