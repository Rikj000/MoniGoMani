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

import logging
import os
from datetime import datetime

from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook
from logging import FileHandler, Formatter

from user_data.mgm_tools.mgm_hurry.CliColor import Color

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class MgmConsoleFormatter(Formatter):
    def __init__(self):
        log_file_format = '%(levelname)s - %(message)s'
        date_format = '%F %A %T'  # In fact this is not used if no %(asctime)s exists in log_file_format
        super(MgmConsoleFormatter, self).__init__(log_file_format, date_format)


class MgmFileFormatter(Formatter):
    def __init__(self):
        log_file_format = '%(levelname)s - %(asctime)s - %(name)s - %(message)s in %(pathname)s:%(lineno)d'
        date_format = '%F %A %T'
        super(MgmFileFormatter, self).__init__(log_file_format, date_format)


class MGMLogger(logging.Logger):

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in SubClasses to create specialized LogRecords.
        """
        log_record = super(MGMLogger, self).makeRecord(name, level, fn, lno, msg, args, exc_info,
                                                       func=None, extra=None, sinfo=None)

        # The magic filtering happens right here!
        log_record.__dict__['msg'] = self.clean_line(log_record.__dict__['msg'])

        return log_record

    def clean_line(self, line: str) -> str:
        """
        Scrubs unwanted information out of a given line to match the preferred MoniGoMani format

        :param line: (str) Line to clean up
        :return str: Cleaned up line
        """
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

        :param line: (str) Line to check if it needs to be filtered out
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
            'user_data.mgm_tools.mgm_hurry.MoniGoManiLogger['
        }

        matches = '\n'.join(ignored_line for ignored_line in ignored_lines if ignored_line.lower() in line.lower())
        if len(matches) > 0:
            return True

        return False

    @staticmethod
    def modify_line(line: str) -> str:
        """
        Modifies passed line if needed

        :param line: (str) Line to check if it needs to be modified
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
                line = line.replace('trades. ', 'trades. \n     ')

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


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
class MoniGoManiLogger:
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
        self.output_path = f'{self.basedir}/user_data/logs/'

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)

        self.date_format = '%d-%m-%Y-%H-%M-%S'
        self.output_file_name = f'MGM-Hurry-Command-Results-{datetime.now().strftime(self.date_format)}.log'

        self._setup_logging()

    def _setup_logging(self):
        """
        Use our own Logging setup to log what we want, and more importantly, how we want it!
        """

        logging_file_debug = os.path.join(self.output_path,
                                          f'MGM-Hurry-Command-Debug-{datetime.now().strftime(self.date_format)}.log')
        logging_file_error = os.path.join(self.output_path,
                                          f'MGM-Hurry-Command-Error-{datetime.now().strftime(self.date_format)}.log')

        # Here is configured how log lines are formatted for each Handler.
        logging.setLoggerClass(MGMLogger)

        mgm_logger = logging.getLogger()
        mgm_logger.setLevel(logging.INFO)

        while mgm_logger.handlers:
            mgm_logger.handlers.pop()

        # How to log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(MgmConsoleFormatter())

        # How to log to log file (debug)
        exp_file_handler = FileHandler(logging_file_debug, mode='a')
        exp_file_handler.setLevel(logging.DEBUG)
        exp_file_handler.setFormatter(MgmFileFormatter())

        # How to log to log file (error)
        exp_errors_file_handler = FileHandler(logging_file_error, mode='a')
        exp_errors_file_handler.setLevel(logging.WARNING)
        exp_errors_file_handler.setFormatter(MgmFileFormatter())

        mgm_logger.addHandler(console_handler)
        mgm_logger.addHandler(exp_file_handler)
        mgm_logger.addHandler(exp_errors_file_handler)

        self.logger = mgm_logger

    def get_logger(self) -> logging:
        """
        Return the logging object.

        :return logging: Logging object
        """
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

        response = {'hyperopt_results': hyperopt_results, 'results_updated': False}

        for hyperopt_results_detector in {'+---------', '| * Best |', '|   Best |'}:
            if hyperopt_results_detector in line:
                # Remove the Epoch/ETA if it got added
                if ' [Epoch ' in line:
                    line = line[: line.index(' [Epoch ')]
                # Split and add the HyperOpt Results lines if multiple got added
                if ' || ' in line:
                    line_nr = 0
                    split_lines = line.split(' || ')
                    for split_line in split_lines:
                        if (line_nr % 2) == 0:
                            adjusted_split_line = f'{split_line} |'
                        else:
                            adjusted_split_line = f'| {split_line}'

                        response['hyperopt_results'].append(adjusted_split_line)
                        line_nr += 1
                # Append the HyperOpt Results line if only a single one got added
                else:
                    response['hyperopt_results'].append(line)
                response['results_updated'] = True

        return response

    @staticmethod
    def post_message(username: str = 'MoniGoMani Community', message: str = None, results_paths: list = None) -> None:
        """
        Posts Results location to the console & the result files to the MoniGoMani Community

        :param username: (str, Optional) Username that will be used. Defaults to 'MoniGoMani Community'
        :param message: (str, Optional) The message that will be passed. Defaults to None
        :param results_paths: (str, Optional) List of paths to the results files that will be shared, defaults to None
        """
        try:
            logger = MoniGoManiLogger(os.getcwd()).get_logger()
            hook = False
            format_message = message.replace('⬇️', f'by **{username}** ⬇️')
            if len(results_paths) in [1, 2]:
                if len(results_paths) == 1:
                    if str(results_paths[0]).endswith('.zip'):
                        hook = str(Fernet(b'WcPNekDZ8uM8ScnAWSxLrkD7fILk5TgNmSrS0suk_dw=').decrypt(
                        b'gAAAAABh0R9_9ct3sXFnrCM35lV7GHZVD3Ow02tQcJoXvzqfjuxhi5ot3wSWGVvWp61TUmmV3EctXKa56kb'
                        b'SZ3AXIKNS8E8uKBknZTjUKMdTfGwkcyB8Q9OQvmj3-ziAgXjzXsUBDeQvMBThOU5TlOE_idXPHE5Ft6qTun'
                        b'r1tIkm3YA0r8OcogCsqn2B9T6qT20pIrXT1FKGsyLAU3cwLYNhX_lS6p8iLU-ES1CcRvA3thUllOppnb8='), 'utf-8')
                format_message = format_message.replace(
                    '⬇️', f'⬇️\nFilename: **{results_paths[len(results_paths) - 1].split("/")[-1]}**')
            if not hook:
                hook = str(Fernet(b'cFiOvKaA39G8si5_fM9RdFPU5kK_Oc5yx2C7-fI5As0=').decrypt(
                b'gAAAAABhMP-sTHDmuR5vT8lKXrzbWcW7ZNa8uqV7ClhzW57PHpsSoyJFBS8JTgiky4bxEAKHiW_F5s9zGyQ'
                b'gEeUbL4dxOtonvvWZccjzZg4fzRglIxgg4BE9ijLMvIdOa8Y7Vw_vYyqdg5sqdeQCScDqbA2R4tmpU1cCfB'
                b'3pNIYmJXJqi714RUwwganfcjiv81x5-VTs6_5QD3OFYz3Nu9RwIzxKIgsc1ug2q8jMfr7Aggl09Tn2hLw='), 'utf-8')
            wh = DiscordWebhook(hook, username=username, content=format_message)

            if (results_paths is not None) and (len(results_paths) > 0):
                split_message = message.split('**')
                if len(split_message) == 3:
                    message = (Color.green(split_message[0]) + Color.green(Color.bold(split_message[1])) +
                               Color.green(split_message[2]))
                logger.info(Color.green(message))
                for results_path in results_paths:
                    if (results_path is not None) and os.path.isfile(results_path):
                        with open(results_path, 'rb') as f:
                            wh.add_file(file=f.read(), filename=os.path.basename(results_path))
                        logger.info(results_path)
            wh.execute()
        except Exception:
            pass

    @staticmethod
    def post_setup(config: dict, strategy: str, basedir: str) -> None:
        """
        Post the 'mgm-config' and 'Strategy' used to the MoniGoMani Community

        :param config: (dict) '.hurry' Config dictionary
        :param strategy: (str) Name of the strategy used
        :param basedir: (str) Base directory of command execution
        """
        logger = MoniGoManiLogger(basedir)
        mgm_config_hyperopt = f'{basedir}/user_data/{config["mgm_config_names"]["mgm-config-hyperopt"]}'
        setup_file_paths = [f'{basedir}/user_data/{config["mgm_config_names"]["mgm-config"]}',
                            mgm_config_hyperopt, f'{basedir}/user_data/strategies/{strategy}.py']

        if (strategy == 'MoniGoManiHyperStrategy') and os.path.isfile(mgm_config_hyperopt):
            message = f'👀 Corresponding **{strategy}** mgm-config, mgm-config-hyperopt & strategy files ⬇️'
        else:
            message = f'👀 Corresponding **{strategy}** mgm-config & strategy files ⬇️'
        logger.post_message(username=config['username'], message=message, results_paths=setup_file_paths)
