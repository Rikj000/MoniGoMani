# -*- coding: utf-8 -*-
import sys

import pytest

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig


def test_initialisation():
    cfg = __get_instance()
    assert isinstance(cfg, MoniGoManiConfig)


@pytest.mark.skip(reason='Test not implemented.')
def test_reload_with_valid_config_file():
    """
    ↓ Unit Testing .reload(self) -> bool
    """
    assert NotImplemented


def test_valid_hurry_dotfile_present_should_return_true():
    """
    ↓ Unit Testing .valid_hurry_dotfile_present(self) -> bool
    """
    obj = __get_instance()
    assert obj.valid_hurry_dotfile_present() is True


@pytest.mark.skip(reason='Test not implemented.')
def test_create_config_files_faulty_target_dir():
    """
    ↓ Unit Testing .create_config_files(self) -> bool
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_create_config_files_faulty_example_file():
    """
    ↓ Unit Testing .create_config_files(self) faulty example file
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_load_config_files():
    """
    ↓ Unit Testing .load_config_files() -> dict
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_read_hurry_config():
    """
    ↓ Unit Testing .read_hurry_config() -> dict:
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_get_config_filename():
    """
    ↓ Unit Testing "get_config_filename"
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_load_config_file():
    """
    ↓ Unit Testing "load_config_file"
    """
    assert NotImplemented


@pytest.mark.skip(reason='Test not implemented.')
def test_write():
    """
    ↓ Unit Testing "write"
    """
    assert NotImplemented


# ---
# --- ↓
def __get_instance():
    """
    ↓ Helper method: Create and get instance of MoniGoManiConfig
    :return MoniGoManiConfig:
    """
    basedir = '.'
    obj = MoniGoManiConfig(basedir)
    return obj
