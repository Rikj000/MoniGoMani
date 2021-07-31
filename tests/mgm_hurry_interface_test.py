# -*- coding: utf-8 -*-
import pytest

# This unit test file will help while splitting mgm-hurry
# into more modular code.
#
#   1. Create unit test for specific functionality
#      - Verify unit test succeeds
#   2. Split and modularize code. The interface should remain unchanged.
#   3. Run unit test
#      - Verify unit test still succeeds
#
# Also be aware to unit test on code and cli level if differences could occur.
#
# Interface mgm-hurry:
#    MGMHurry.
#       up
#       install_freqtrade
#       install_mgm
#       setup
#       cleanup
#       download_candle_data
#       hyperopt
#       hyperopt_show_results
#       hyperopt_show_epoch
#       hyperopt_apply_epoch
#       backtest
#       start_trader

def test_basic_usage():
    assert True is True
