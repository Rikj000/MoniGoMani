# -*- coding: utf-8 -*-
import os
import sys
from logging import Logger
from unittest.mock import MagicMock

import pytest

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli


def test_initialisation():
    cli = __get_instance()
    assert isinstance(cli, MoniGoManiCli)


def test_installation_exists_without_installation():
    """
    ↓ Unit Testing .installation_exists(self) -> bool
    """
    os.path.exists = MagicMock(return_value=False)
    mgm_cli = __get_instance()
    assert mgm_cli.installation_exists() is False


def test_installation_exists_with_config_without_strategy():
    """
    ↓ Unit Testing .installation_exists(self) -> bool
    """
    mgm_cli = __get_instance()
    mgm_cli._mgm_config_json_exists = MagicMock(return_value=True)
    mgm_cli._mgm_hyperstrategy_file_exists = MagicMock(return_value=False)
    assert mgm_cli.installation_exists() is False


def test_installation_exists_without_config_with_strategy():
    mgm_cli = __get_instance()
    mgm_cli._mgm_hyperstrategy_file_exists = MagicMock(return_value=True)
    mgm_cli._mgm_config_json_exists = MagicMock(return_value=False)
    assert mgm_cli.installation_exists() is False


def test_installation_exists_with_valid_installation():
    mgm_cli = __get_instance()
    mgm_cli._mgm_hyperstrategy_file_exists = MagicMock(return_value=True)
    mgm_cli._mgm_config_json_exists = MagicMock(return_value=True)
    assert mgm_cli.installation_exists() is True


@pytest.mark.skip(reason='Test not implemented.')
def test_download_setup_mgm():
    """
    ↓ Unit Testing .download_setup_mgm(branch:str = 'develop', target_dir:str = None)
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_apply_best_results():
    """
    ↓ Unit Testing .apply_best_results(self, strategy: str) -> bool
    """
    assert NotImplemented


def test_apply_best_results_should_return_false_without_ho_json():
    mgm_cli = __get_instance()
    assert mgm_cli.apply_mgm_results('foobar-non-existing-strat') is False


@pytest.mark.skip(reason='Test not implemented.')
def test_run_command():
    """
    ↓ Unit Testing .run_command(self, command: str, output_file_name: str = None)
    """
    assert NotImplemented


def __get_instance(basedir='.'):
    """
    ↓ Helper method: Create and get instance of MoniGoManiCli
    :return MoniGoManiCli:
    """
    cli = MoniGoManiCli(basedir)
    cli.cli_logger = MagicMock()
    return cli


def __get_logger(basedir='.') -> Logger:
    return MagicMock()
