# -*- coding: utf-8 -*-
import sys
import pytest

from unittest.mock import patch

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger


def test_initialisation():
    cfg = __get_instance()
    assert isinstance(cfg, MoniGoManiConfig)

# --- ↓
# --- ↓ Unit Testing .reload(self) -> bool
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_reload_with_valid_config_file():
    assert NotImplemented

# --- ↑

# --- ↓
# --- ↓ Unit Testing .valid_config_file_present(self) -> bool
# --- ↓

def test_valid_config_file_present_should_return_true():
    obj = __get_instance()
    assert obj.valid_config_file_present() is True

# --- ↑


# --- ↓
# --- ↓ Unit Testing .create_config_files(self) -> bool
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_create_config_files_faulty_target_dir():
    assert NotImplemented

@pytest.mark.skip(reason='Test not implemented.')
def test_create_config_files_faulty_example_file():
    assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing .load_config_files() -> dict
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_load_config_files():
    assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing .read_hurry_config() -> dict
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_read_hurry_config():
    assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing "get_config_filename"
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_get_config_filename():
	assert NotImplemented

# --- ↑

# --- ↓
# --- ↓ Unit Testing "load_config_files"
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_load_config_files():
	assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing "read_hurry_config"
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_read_hurry_config():
	assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing "get_config_filename"
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_get_config_filename():
	assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing "load_config_file"
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_load_config_file():
	assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Unit Testing "write"
# --- ↓

@pytest.mark.skip(reason='Test not implemented.')
def test_write():
	assert NotImplemented

# --- ↑


# --- ↓
# --- ↓ Helper methods
# --- ↓
@patch('MoniGoManiLogger.logging')
@patch('MoniGoManiLogger.logger')
def __get_instance():
    basedir = '.'
    obj = MoniGoManiConfig(basedir)
    return obj

