# -*- coding: utf-8 -*-
import sys
import logging

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger

def test_initialisation_logger():
    logger = MoniGoManiLogger('.', print_output=True)
    assert isinstance(logger, MoniGoManiLogger)

def test_get_logger_method():
    logger = MoniGoManiLogger('.', print_output=True).get_logger()
    assert logger is not None
