# -*- coding: utf-8 -*-
# from logging import Logger
# import pytest
import sys

sys.path.append('.')
sys.path.append('..')

from pytest import mark
from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import get_logger


def test_initialisation():
    cfg = __get_instance('.', get_logger())
    assert type(cfg) is MoniGoManiConfig

def test_valid_config_file_present_should_return_false_without_hurry_config():
    obj = __get_instance('.', get_logger())
    assert obj.valid_config_file_present() is False


@mark.notimplemented
def test_config_getter_method_should_return_dict():
    # TODO use mock / stub to create .hurry file
    assert True is True

def __get_instance(basedir='.', logger=None):
    return MoniGoManiConfig(basedir, logger)
