# -*- coding: utf-8 -*-
from logging import Logger
import pytest
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger

def test_initialisation():
    cli = __get_instance()
    assert isinstance(cli, MoniGoManiCli)

@pytest.mark.skip(reason='Test not implemented. Mocking needed.')
def test_installation_exists_without_installation():
    assert NotImplemented

@pytest.mark.skip(reason='Test not implemented. Mocking needed.')
def test_installation_exists_with_config_without_strategy():
    assert NotImplemented

@pytest.mark.skip(reason='Test not implemented. Mocking needed.')
def test_installation_exists_without_config_with_strategy():
    assert NotImplemented

@pytest.mark.skip(reason='Test not implemented. Mocking needed.')
def test_installation_exists_with_valid_installation():
    assert NotImplemented

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
