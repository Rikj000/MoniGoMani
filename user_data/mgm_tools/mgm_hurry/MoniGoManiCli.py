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

    def run_command(self, command: str) -> int:
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

        with subprocess.Popen(shlex.split(command),
                              shell=True,
                              stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:

            while process.poll() is None:
                stdout = self.non_blocking_read(process.stdout)
                if stdout:
                    self.logger.info(stdout)

        return 0

    def non_blocking_read(self, output):
        """Read shell stdout in a non-blocking way.

        :param output (stdout)
        :return output.read (str)
        """
        file_descriptor = output.fileno()
        file_control = fcntl.fcntl(file_descriptor, fcntl.F_GETFL)
        fcntl.fcntl(file_descriptor, fcntl.F_SETFL,
                    file_control | os.O_NONBLOCK)
        try:
            return output.read()
        except Exception:
            return ''
