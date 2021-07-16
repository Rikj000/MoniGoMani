from logging import Logger
import sys
sys.path.append(".")
sys.path.append("..")

from user_data.mgm_tools.mgm_hurry.leet_logger import get_logger

def test_initialisation_logger():
  logger = get_logger()
  assert type(logger) is Logger
