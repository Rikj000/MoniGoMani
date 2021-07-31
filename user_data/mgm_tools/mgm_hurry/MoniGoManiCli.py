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
import json
import os
import subprocess  # noqa: S404 (skip security check)
import shlex
import sys

import yaml

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
        :param output_path (str, optional): Path to the output of the '.log' file. Defaults to 'Some Test Results/MoniGoMani_version_number/'
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

        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                if log_output is True:
                    self._write_log_line(output_file, output.strip())
        rc = process.poll()
        return rc

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
        #self.monigomani_config.bot_name

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

    def exec_cmd(self, cmd: str, save_output: bool = False) -> int:
        self.logger.deprecated('Calling exec_cmd is deprecated. Please switch to public method run_command()')
        return self.run_command(cmd, log_output=save_output)

    def _exec_cmd(self, cmd: str, save_output: bool = False, output_path: str = None, output_file_name: str = None) -> int:
        self.logger.deprecated('Calling _exec_cmd is deprecated. Please switch to public method run_command()')
        return self.run_command(cmd, save_output, output_path, output_file_name)
