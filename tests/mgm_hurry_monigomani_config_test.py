# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig

def test_initialisation():
    cfg = __get_instance()
    assert isinstance(cfg, MoniGoManiConfig)

def test_valid_config_file_present_should_return_true():
    obj = __get_instance()
    assert obj.valid_config_file_present() is True

def __get_instance():
    basedir = '.'
    return MoniGoManiConfig(basedir)
