# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------

"""MoniGoManiCli is the responsible module to communicate with the mgm strategy."""

# ___  ___               _  _____        ___  ___               _  _____  _  _
# |  \/  |              (_)|  __ \       |  \/  |              (_)/  __ \| |(_)
# | .  . |  ___   _ __   _ | |  \/  ___  | .  . |  __ _  _ __   _ | /  \/| | _
# | |\/| | / _ \ | '_ \ | || | __  / _ \ | |\/| | / _` || '_ \ | || |    | || |
# | |  | || (_) || | | || || |_\ \| (_) || |  | || (_| || | | || || \__/\| || |
# \_|  |_/ \___/ |_| |_||_| \____/ \___/ \_|  |_/ \__,_||_| |_||_| \____/|_||_|

from datetime import datetime
import os
import subprocess  # noqa: S404 (skip security check)
import fcntl
import shlex
import sys

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class MoniGoManiCli(object):
    """Use this module to communicate with the mgm hyperstrategy,."""

    log_output: bool = False
    output_path: str = None
    output_file_name: str = None

    def __init__(self, basedir, logger):
        """Instantiate a new object of mgm cli.

        Args:
            basedir (str): The directory
            logger (logger): The logger
        """
        self.basedir = basedir
        self.logger = logger

        # :todo move to mgm logger?
        self.log_output = True
        self.output_path = '{0}/Some Test Results/'.format(self.basedir)
        self.output_file_name = 'MGM-Hurry-Command-Results-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))

    def installation_exists(self) -> bool:
        """Check if the MGM Hyper Strategy installation exists.

        Returns:
            success (bool): Whether or not the config and strategy files are found.
        """
        if os.path.exists('{0}/user_data/mgm-config.json'.format(self.basedir)) is False:
            self.logger.warning('🤷♂️ No "mgm-config.json" file found.')
            return False

        if os.path.exists('{0}/user_data/strategies/MoniGoManiHyperStrategy.py'.format(self.basedir)) is False:
            self.logger.warning('🤷♂️ No "MoniGoManiHyperStrategy.py" file found.')
            return False

        self.logger.debug('👉 MoniGoManiHyperStrategy and configuration found √')
        return True

    def run_command(self,
                    command: str,
                    log_output: bool = None,
                    output_path: str = None,
                    output_file_name: str = None) -> int:
        """Execute shell command and log output to mgm logfile.

        :param command (str): Shell command to execute.
        :param log_output (bool, optional): Whether or not to log the output to mgm-logfile. Defaults to False.
        :param output_path (str, optional): Path to the output of the '.log' file.
                                            Defaults to 'Some Test Results/MoniGoMani_version_number/'
        :param output_file_name (str, optional): Name of the '.log' file. Defaults to 'Results-<Current-DateTime>.log'.
        :return int: return code zero (0) if all went ok. > 0 if there's an issue.
        """
        if command is None or command == '':
            self.logger.error(
                '🤷 Please pass a command through. Without command no objective, sir!'
            )
            sys.exit(1)

        if output_path is None:
            output_path = self.output_path

        if output_file_name is None:
            output_file_name = self.output_file_name

        if log_output is not None:
            self.log_output = log_output

        if self.log_output is True:
            output_file = open(self._get_logfile(output_path=output_path, output_file_name=output_file_name), 'w')

        process = subprocess.Popen(shlex.split(command),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        while process.poll() is None:
            stdout = self.nonBlockRead(process.stdout)
            if stdout:
                if self.log_output is True:
                    self._write_log_line(output_file, stdout)
                else:
                    print(stdout)

        return 0

    def nonBlockRead(self, output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return ''

    def _get_logfile(self,
                     output_path: str,
                     output_file_name: str) -> str:
        """Get the full path to log file.

        Creates the output path directory if it not exists.
        Also creates the output file name if it not exists.

        :param output_path (str): The full path to the output log file. Defaults to None.
        :param output_file_name (str): The filename of the output log file. Defaults to None.
        :return str: full path to log file (including logfile name)

        :todo integrate in self.logger to avoid duplicate functionality
        """

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        # FIXME – fix that the bot name from the config file will be used

        # monigomani_config = MoniGoManiConfig(self.basedir, self.logger)
        # mgm_config_files = monigomani_config.load_config_files()
        # self.monigomani_config.bot_name

        bot_name = 'Unnamed Bot'

        bot_log_dir = os.path.join(output_path, bot_name)
        if not os.path.isdir(bot_log_dir):
            os.mkdir(bot_log_dir)

        # create path like foo/bar/
        # and be sure only 1 repeating / is used
        output_path = os.path.normpath(
            os.path.join(
                output_path,
                bot_name
            ), )

        return os.path.join(output_path, output_file_name)

    def _write_log_line(self, log_file, line):
        """Writes clean log line to file.

        :param log_file (file.open()): The log file to write to.
        :param line (str): The data to log.

        :todo integrate in self.logger to avoid duplicate functionality
        """

        second_splitter = line.find(' - ', line.find(' - ') + 1) + 3
        trimmed_line = line[second_splitter:len(line)]
        if self.filter_line(trimmed_line) is False:
            log_file.write(trimmed_line)

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
