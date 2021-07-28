# -*- coding: utf-8 -*-
# from logging import Logger
# import pytest
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import get_logger


def test_initialisation():
    cfg = __get_instance('.', get_logger())
    assert type(cfg) is MoniGoManiConfig

def __get_instance(basedir='.', logger=None):
    return MoniGoManiConfig(basedir, logger)
