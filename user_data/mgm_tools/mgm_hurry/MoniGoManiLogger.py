# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------

"""MoniGoManiLogger is the module responsible for all logging related tasks.."""

# ___  ___               _  _____        ___  ___               _  _
# |  \/  |              (_)|  __ \       |  \/  |              (_)| |
# | .  . |  ___   _ __   _ | |  \/  ___  | .  . |  __ _  _ __   _ | |      ___    __ _   __ _   ___  _ __
# | |\/| | / _ \ | '_ \ | || | __  / _ \ | |\/| | / _` || '_ \ | || |     / _ \  / _` | / _` | / _ \| '__|
# | |  | || (_) || | | || || |_\ \| (_) || |  | || (_| || | | || || |____| (_) || (_| || (_| ||  __/| |
# \_|  |_/ \___/ |_| |_||_| \____/ \___/ \_|  |_/ \__,_||_| |_||_|\_____/ \___/  \__, | \__, | \___||_|
#                                                                                 __/ |  __/ |
#                                                                                |___/  |___/
#
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------

import logging
import os
from datetime import datetime

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

class MoniGoManiLogger():
    """
    Let's Log and Roll.

    More information at https://docs.python.org/3/howto/logging.html
    """

    basedir: str
    logger: logging
    output_path: str
    output_file_name: str

    def __init__(self, basedir: str, print_output: bool = True):
        """
        :param basedir (str): The basedir of MGM
        :param print_output (bool, optional): Print output or log fo file. Defaults to True (so, printing output)
        """
        self.basedir = basedir

        self.output_path = '{0}/Some Test Results/'.format(self.basedir)
        self.output_file_name = 'MGM-Hurry-Command-Results-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))

        logging_format = '%(asctime)s = MGM-HURRY = %(levelname)s: %(message)s'
        logging_file = os.path.join(self.output_path, self.output_file_name)

        print_output = False  # FIXME remove, as this is for debugging purposes

        if print_output is True:
            logging.basicConfig(
                format=logging_format,
                datefmt='%F %A %T',
                level=logging.DEBUG)
        else:
            logging.basicConfig(
                handlers=[logging.FileHandler(filename=logging_file,encoding='utf-8',mode='a+')],
                format=logging_format,
                datefmt='%F %A %T',
                level=logging.DEBUG)

        self.logger = logging

        # if print_output is True:
        #     self.logger.basicConfig(format=logging_format,
        #                             encoding='utf-8',
        #                             level=logging.DEBUG)
        # else:
        #     self.logger.basicConfig(filename=logging_file,
        #                             format=logging_format,
        #                             encoding='utf-8',
        #                             level=logging.DEBUG)

    def get_logger(self) -> logging:
        """Return the logging object."""
        return self.logger

    # def _write_log_line(self, log_file, line):
    #     """Writes clean log line to file.

    #     :param log_file (file.open()): The log file to write to.
    #     :param line (str): The data to log.

    #     :todo integrate in self.logger to avoid duplicate functionality
    #     """

    # second_splitter = line.find(' - ', line.find(' - ') + 1) + 3
    # trimmed_line = line[second_splitter:len(line)]
    # if self.filter_line(trimmed_line) is False:
    #     log_file.write(trimmed_line)

    @staticmethod
    def filter_line(line: str) -> bool:
        """
        Checks if line needs to be filtered out.

        :param line: Line to check if it needs to be filtered out
        :return bool: True if line needs to be filtered out. False if it's allowed to be printed out
        """

        ignored_lines = {
            'INFO - Verbosity set to', 'INFO - Using user-data directory:',
            'INFO - Using data directory:',
            'INFO - Parameter -j/--job-workers detected:',
            'INFO - Parameter --random-state detected:',
            'INFO - Checking exchange...', 'INFO - Exchange "',
            'INFO - Using pairlist from configuration.',
            'INFO - Validating configuration ...',
            'INFO - Starting freqtrade in', 'INFO - Lock',
            'INFO - Instance is running with', 'INFO - Using CCXT',
            'INFO - Applying additional ccxt config:', 'INFO - Using Exchange',
            'INFO - Using resolved exchange',
            'INFO - Found no parameter file.',
            'INFO - Strategy using order_types:',
            'INFO - Strategy using order_time_in_force:',
            'INFO - Strategy using stake_currency:',
            'INFO - Strategy using stake_amount:',
            'INFO - Strategy using protections:',
            'INFO - Strategy using unfilledtimeout:',
            'INFO - Strategy using use_sell_signal:',
            'INFO - Strategy using sell_profit_only:',
            'INFO - Strategy using ignore_roi_if_buy_signal:',
            'INFO - Strategy using sell_profit_offset:',
            'INFO - Strategy using disable_dataframe_checks:',
            'INFO - Using resolved pairlist StaticPairList from',
            'INFO - Using resolved hyperoptloss', 'INFO - Removing `',
            'INFO - Using indicator startup period:',
            'INFO - Note: NumExpr detected', 'INFO - NumExpr defaulting to',
            'INFO - Dataload complete. Calculating indicators', 'INFO - Found',
            'INFO - Number of parallel jobs set as:',
            'INFO - Effective number of parallel workers used:'
        }

        matches = '\n'.join(ignored_line for ignored_line in ignored_lines
                            if ignored_line.lower() in line.lower())
        if len(matches) > 0:
            return True

        return False
