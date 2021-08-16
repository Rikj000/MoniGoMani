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

import os
import logging

from logging import Formatter
from Logging.handlers import RotatingFileHandler
from datetime import datetime

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

class mgmConsoleFormatter(Formatter):
    def __init__(self):
        log_file_format = "[%(levelname)s] - : %(message)s"
        datefmt = '%F %A %T' # in fact this is not used if no %(asctime)s exists in log_file_format
        super(mgmConsoleFormatter, self).__init__(log_file_format, datefmt)
        

class mgmFileFormatter(Formatter):
    def __init__(self):
        log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"
        datefmt = '%F %A %T'
        super(mgmFileFormatter, self).__init__(log_file_format, datefmt)


class MGMLogger(logging.Logger):
    def makeRecord(self, *args, **kwargs):
        rv = super(MGMLogger, self).makeRecord(*args, **kwargs)
        
        # TODO Filter as we like it
        rv.__dict__['message'] = self.clean_line(rv.__dict__['message'])
        
        return rv

    def clean_line(self, line: str) -> str:
        # Split off the Datetime + Code Sections if needed to keep things clean
        if line.count(' - ') >= 3:
            second_splitter = line.find(' - ', line.find(' - ') + 1) + 3
            final_line = line[second_splitter:len(line)]
        else:
            final_line = line

        # Filter out unwanted - unneeded - double lines
        if self.filter_line(final_line) is False:
            # Modify line output to MoniGoMani's preferred format
            final_line = self.modify_line(final_line)

        return final_line
    
    @staticmethod
    def filter_line(line: str) -> bool:
        """
        Checks if line needs to be filtered out.

        :param line: Line to check if it needs to be filtered out
        :return bool: True if line needs to be filtered out. False if it's allowed to be printed out
        """

        ignored_lines = {
            'INFO - Verbosity set to',
            'INFO - Using user-data directory:',
            'INFO - Using data directory:',
            'INFO - Parameter -j/--job-workers detected:',
            'INFO - Parameter --random-state detected:',
            'INFO - Checking exchange...',
            'INFO - Exchange "',
            'INFO - Using pairlist from configuration.',
            'INFO - Validating configuration ...',
            'INFO - Starting freqtrade in',
            'INFO - Lock',
            'INFO - Instance is running with',
            'INFO - Using CCXT',
            'INFO - Applying additional ccxt config:',
            'INFO - Using Exchange',
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
            'INFO - Using resolved hyperoptloss',
            'INFO - Removing `',
            'INFO - Using indicator startup period:',
            'INFO - Note: NumExpr detected',
            'INFO - NumExpr defaulting to',
            'INFO - Dataload complete. Calculating indicators',
            'INFO - Found',
            'INFO - Number of parallel jobs set as:',
            'INFO - Effective number of parallel workers used:',
            'user_data.mgm_tools.mgm_hurry.LeetLogger['
        }

        matches = '\n'.join(ignored_line for ignored_line in ignored_lines if ignored_line.lower() in line.lower())
        if len(matches) > 0:
            return True

        return False

    @staticmethod
    def modify_line(line: str) -> str:
        """
        Modifies passed line if needed

        :param line: Line to check if it needs to be modified
        :return str: Returns modified string
        """

        # Remove weird unicode characters
        remove_substrings = {'[32m', '[39m'}

        for remove_substring in remove_substrings:
            if remove_substring in line:
                line = line.replace(remove_substring, '')

        # Add in newline pre/suf-fixes where needed
        prefix_newlines = {'Avg profit', 'Median profit', 'Total profit', 'Avg duration', 'Objective'}
        if 'Wins/Draws/Losses. Avg profit' in line:
            line = line.replace(':', ':\n', 1)

            for prefix_newline in prefix_newlines:
                if prefix_newline in line:
                    line = line.replace(prefix_newline, f'\n     {prefix_newline}')

            if 'trades. ' in line:
                line = line.replace('trades. ', f'trades. \n     ')

        prefix_other_newlines = {'Elapsed Time:', 'Best result:', '# Buy hyperspace params:',
                                 '# Sell hyperspace params:', '# ROI table:', '# Stoploss:', '# Trailing stop:'}

        for prefix_other_newline in prefix_other_newlines:
            if prefix_other_newline in line:
                line = line.replace(line, f'\n{line}')
                line = line[1: len(line)]

        if ' (100%)] ||       | [Time:  ' in line:
            line = line[line.index(', ') + 2: len(line)].replace(']', '')
            line = line.replace(line, f'\n{line}')

        return line


class MoniGoManiLogger():
    """
    Let's Log and Roll.

    More information at https://docs.python.org/3/howto/logging.html

    Attributes:
        basedir             The basedir where the monigomani install lives.
        logger              The logger function of the MoniGoManiCli module.
        output_path         Absolute path to the directory where logs are stored.
        output_file_name    The logfile name.log
    """
    basedir: str
    logger: logging
    output_path: str
    output_file_name: str

    def __init__(self, basedir: str, print_output: bool = True):
        """
        Wrapper object around the logger function that logs messages like we want.

        :param basedir (str): The basedir of MGM
        :param print_output (bool, optional): Print output or log to file. Defaults to True (so, printing output)
        """
        self.basedir = basedir
        self.output_path = '{0}/Some Test Results/'.format(self.basedir)
        self.output_file_name = 'MGM-Hurry-Command-Results-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
        
        # TODO is this switch still needed?
        # if print_output is True:

        self._setup_logging()

    def _setup_logging(self):
        # Use our own Logging setup to log what we want. 
        # And probably more important: how we want it!

        logging_file_debug = os.path.join(self.output_path, 'MGM-Hurry-Command-Debug-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S')))
        logging_file_error = os.path.join(self.output_path, 'MGM-Hurry-Command-Error-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S')))

        # Here is configured how log lines are formatted for each Handler.
        logging.setLoggerClass(MGMLogger)

        mgm_logger = logging.getLogger()
        mgm_logger.setLevel(logging.INFO)

        # How to log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(mgmConsoleFormatter())

        # How to log to log file (debug)
        exp_file_handler = RotatingFileHandler(logging_file_debug, maxBytes=10**6, backupCount=5)
        exp_file_handler.setLevel(logging.DEBUG)
        exp_file_handler.setFormatter(mgmFileFormatter())

        # How to log to log file (error)
        exp_errors_file_handler = RotatingFileHandler(logging_file_error, maxBytes=10**6, backupCount=5)
        exp_errors_file_handler.setLevel(logging.WARNING)
        exp_errors_file_handler.setFormatter(mgmFileFormatter())

        mgm_logger.addHandler(console_handler)
        mgm_logger.addHandler(exp_file_handler)
        mgm_logger.addHandler(exp_errors_file_handler)

        self.logger = mgm_logger

    def get_logger(self) -> logging:
        """Return the logging object."""
        return self.logger

    @staticmethod
    def store_hyperopt_results(hyperopt_results: list, line: str) -> dict:
        """
        Filters out and stores HyperOpt Results line

        :param hyperopt_results: List to which the HyperOpt Result will be appended
        :param line: String to check if it needs to be appended to the hyperopt_results
        :return dict: Response dictionary containing:
            - 'hyperopt_results': The updated hyperopt_results list
            - 'results_updated': Boolean stating if the results got updated or not
        """

        response = {
            'hyperopt_results': hyperopt_results,
            'results_updated': False
        }

        for hyperopt_results_detector in {'+-----------+', '|   Best |'}:
            if hyperopt_results_detector in line:
                response['hyperopt_results'].append(line)
                response['results_updated'] = True

        return response

    
