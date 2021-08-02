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
from shell_command import shell_call
from git import Repo
import tempfile
from shutil import copytree
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

    def download_setup_mgm(self, branch: str = 'develop', target_dir: str = None):
        """
        Install Freqtrade using a git clone to target_dir.

        Args:
            branch (str): Checkout a specific branch. Defaults to 'develop'.
            target_dir (str): Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        """
        with tempfile.TemporaryDirectory() as temp_dirname:

            repo = Repo.clone_from('https://github.com/Rikj000/MoniGoMani.git',
                                   temp_dirname,
                                   branch=branch)

            if not isinstance(repo, Repo):
                self.logger.critical('Failed to clone MoniGoMani repo. I quit!')
                os.sys.exit(1)

            try:
                copytree(f'cp -rf {temp_dirname}/user_data/',
                         f'{target_dir}/user_data/')
            except OSError as e:
                if e.errno != 17:
                    self.logger.error(e)
                else:
                    self.logger.warning(e)

    def run_command(self, command: str) -> int:
        """Execute shell command and log output to mgm logfile.

        :param command (str): Shell command to execute.
        :return int: return code zero (0) if all went ok. > 0 if there's an issue.
        """
        if command is None or command == '':
            self.logger.error(
                '🤷 Please pass a command through. Without command no objective, sir!'
            )
            sys.exit(1)

        return shell_call(command)
