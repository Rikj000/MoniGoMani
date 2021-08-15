# -*- coding: utf-8 -*-
import os
from logging import Logger
from unittest.mock import MagicMock, patch
import pytest
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger


def test_initialisation():
    cli = __get_instance()
    assert isinstance(cli, MoniGoManiCli)


# --- ↓
# --- ↓ Unit Testing .installation_exists(self) -> bool
# --- ↓

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

# --- ↑


# --- ↓
# --- ↓ Unit Testing .download_setup_mgm(branch:str = 'develop', target_dir:str = None)
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_download_setup_mgm():
    assert NotImplemented
# --- ↑


# --- ↓
# --- ↓ Unit Testing .apply_best_results(self, strategy: str) -> bool
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_apply_best_results():
    assert NotImplemented

def test_apply_best_results_should_return_false_without_ho_json():
    mgm_cli = __get_instance()
    assert mgm_cli.apply_best_results('foobar-non-existing-strat') is False

# --- ↑


# --- ↓
# --- ↓ Unit Testing .run_command(self, command: str, output_file_name: str = None)
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_run_command():
    assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Helper methods
# --- ↓
@patch('MoniGoManiLogger.logging')
@patch('MoniGoManiLogger.logger')
def __get_instance(basedir='.'):
    cli = MoniGoManiCli(basedir)
    return cli

@patch('MoniGoManiLogger.logging')
@patch('MoniGoManiLogger.logger')
def __get_logger(basedir='.') -> Logger:
    return MoniGoManiLogger(basedir).get_logger()
