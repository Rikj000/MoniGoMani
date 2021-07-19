from logging import Logger
import pytest
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli


def test_initialisation():
    cli = __get_instance()
    assert type(cli) is MoniGoManiCli


def test_installation_exists_without_installation():
    cli = __get_instance('.', __get_logger())
    result = cli.installation_exists()
    assert result is False


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


"""
Private helper methods
"""
def __get_instance(basedir='.', logger=None):
    cli = MoniGoManiCli(basedir, logger)
    return cli

def __get_logger() -> Logger:
    '''
    Todo:
        - Implement a mock-object.
    '''
    logger = Logger(name='mockme')
    return logger
