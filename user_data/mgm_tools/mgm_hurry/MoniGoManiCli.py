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

import os
import subprocess  # noqa: S404 (skip security check)
import fcntl
import shlex
import sys

from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class MoniGoManiCli(object):
    """Use this module to communicate with the mgm hyperstrategy,."""

    log_output: bool = False
    output_path: str = None
    output_file_name: str = None
    logger: MoniGoManiLogger

    def __init__(self, basedir):
        """Instantiate a new object of mgm cli.

        Args:
            basedir (str): The directory
        """
        self.basedir = basedir
        self.logger = MoniGoManiLogger(self.basedir).get_logger()

        # :todo move to mgm logger?
        # self.log_output = True
        # self.output_path = '{0}/Some Test Results/'.format(self.basedir)
        # self.output_file_name = 'MGM-Hurry-Command-Results-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))

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
                self.logger.info(stdout)

        return 0

    def nonBlockRead(self, output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return ''
