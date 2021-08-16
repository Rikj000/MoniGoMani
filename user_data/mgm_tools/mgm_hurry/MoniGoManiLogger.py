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

        logging_format = '%(asctime)s = %(levelname)s: %(message)s'
        logging_file = os.path.join(self.output_path, self.output_file_name)

        if print_output is True:
            logging.basicConfig(
                format=logging_format,
                datefmt='%F %A %T',
                level=logging.DEBUG)
        else:
            logging.basicConfig(
                handlers=[logging.FileHandler(filename=logging_file, encoding='utf-8', mode='a+')],
                format=logging_format,
                datefmt='%F %A %T',
                level=logging.DEBUG)

        self.logger = logging

    def get_logger(self) -> logging:
        """Return the logging object."""
        return self.logger

    # FIXME this method needs to find its place in here.
    # It's copied from mgm-hurry (Rikj000/MoniGoMani:development)
    def _parse_line(self, line: str) -> str:
        hyperopt_results = []

        for line in process.stdout:
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

                # Save the output to a '.log' file if enabled
                if (save_output is True) and ('| [ETA:' not in final_line):
                    output_file.write(final_line)

            # Check if a new HyperOpt Results line is found, store it in RAM and re-print the whole HyperOpt Table if so
            response = self.store_hyperopt_results(hyperopt_results, final_line)
            if (response['results_updated'] is True) or \
                    ('| [ETA:' not in final_line) and ('Elapsed Time:' in final_line):
                hyperopt_results = response['hyperopt_results']
                # Skip the initial header
                if len(hyperopt_results) > 3:
                    for hyperopt_results_line in hyperopt_results:
                        sys.stdout.write(hyperopt_results_line)
                if ('| [ETA:' not in final_line) and ('Elapsed Time:' in final_line):
                    sys.stdout.write(final_line)
            else:
                sys.stdout.write(final_line)

        process.wait()

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

    # FIXME; apply next methods to self.monigomani_config
    # rikj000 made changes to these methods, but topscoder
    # already moved these to monigomani_config.
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
