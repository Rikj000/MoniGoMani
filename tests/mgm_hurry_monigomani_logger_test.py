# -*- coding: utf-8 -*-
from logging import Logger
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import get_logger

import sys

sys.path.append('.')
sys.path.append('..')


def test_initialisation_logger():
    logger = get_logger()
    assert type(logger) is Logger
