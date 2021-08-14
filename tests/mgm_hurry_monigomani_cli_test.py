# -*- coding: utf-8 -*-
import os
from logging import Logger
from unittest.mock import MagicMock
import pytest
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger

def test_initialisation():
    cli = __get_instance()
    assert isinstance(cli, MoniGoManiCli)

def test_installation_exists_without_installation():
    os.path.exists = MagicMock(return_value=False)
    mgm_cli = __get_instance()
    assert mgm_cli.installation_exists() == False

def test_installation_exists_with_config_without_strategy():
    mgm_cli = __get_instance()
    mgm_cli._mgm_config_json_exists = MagicMock(return_value=True)
    mgm_cli._mgm_hyperstrategy_file_exists = MagicMock(return_value=False)
    assert mgm_cli.installation_exists() == False

def test_installation_exists_without_config_with_strategy():
    mgm_cli = __get_instance()
    mgm_cli._mgm_hyperstrategy_file_exists = MagicMock(return_value=True)
    mgm_cli._mgm_config_json_exists = MagicMock(return_value=False)
    assert mgm_cli.installation_exists() == False

def test_installation_exists_with_valid_installation():
    mgm_cli = __get_instance()
    mgm_cli._mgm_hyperstrategy_file_exists = MagicMock(return_value=True)
    mgm_cli._mgm_config_json_exists = MagicMock(return_value=True)
    assert mgm_cli.installation_exists() == True

@pytest.mark.skip(reason='Test not implemented. Mocking needed.')
def test_create_config_files_faulty_target_dir():
    assert NotImplemented

@pytest.mark.skip(reason='Test not implemented. Mocking needed.')
def test_create_config_files_faulty_example_file():
    assert NotImplemented

def __get_instance(basedir='.'):
    cli = MoniGoManiCli(basedir)
    return cli

def __get_logger(basedir='.') -> Logger:
    '''
    Todo:
        - Implement a mock-object.
    '''
    return MoniGoManiLogger(basedir).get_logger()
