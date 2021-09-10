# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger  # noqa: E402


def test_initialisation_logger():
    """
    ↓ Unit Testing "__init__":
    """
    logger = MoniGoManiLogger('.', print_output=True)
    assert logger is not None


def test_get_logger():
    """
    ↓ Unit Testing "get_logger"
    """
    logger = MoniGoManiLogger('.', print_output=True).get_logger()
    assert logger is not None
