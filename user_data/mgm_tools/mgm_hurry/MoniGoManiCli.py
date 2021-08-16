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
from shell_command import shell_call, shell_output
from git import Repo
import tempfile

import shlex
from shutil import copytree, copy2
import sys

from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

GIT_URL_MONIGOMANI: str = 'https://github.com/Rikj000/MoniGoMani.git'


class MoniGoManiCli(object):
    """Use this module to communicate with the mgm hyperstrategy.

    Attributes:
        logger      The logger function of the MoniGoManiCli module.
    """
    logger: MoniGoManiLogger

    def __init__(self, basedir):
        """Let's talk command-line-ish.

        :param basedir (str): The directory
        """
        self.basedir = basedir
        self.logger = MoniGoManiLogger(self.basedir).get_logger()

    def installation_exists(self) -> bool:
        """Check if the MGM Hyper Strategy installation exists.

        :return success (bool): Whether or not the config and strategy files are found.
        """
        if self._mgm_config_json_exists() is False:
            self.logger.warning('🤷♂️ No "mgm-config.json" file found.')
            return False

        if self._mgm_hyperstrategy_file_exists() is False:
            self.logger.warning('🤷♂️ No "MoniGoManiHyperStrategy.py" file found.')
            return False

        self.logger.debug('👉 MoniGoManiHyperStrategy and configuration found √')
        return True

    def _mgm_config_json_exists(self) -> bool:
        return os.path.exists('{0}/user_data/mgm-config.json'.format(self.basedir))

    def _mgm_hyperstrategy_file_exists(self) -> bool:
        return os.path.exists('{0}/user_data/strategies/MoniGoManiHyperStrategy.py'.format(self.basedir))

    def download_setup_mgm(self, branch: str = 'develop', target_dir: str = None):
        """
        Install Freqtrade using a git clone to target_dir.

        :param branch (str): Checkout a specific branch. Defaults to 'develop'.
        :param target_dir (str): Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        """
        with tempfile.TemporaryDirectory() as temp_dirname:

            repo = Repo.clone_from(GIT_URL_MONIGOMANI, temp_dirname, branch=branch)

            if not isinstance(repo, Repo):
                self.logger.critical('Failed to clone MoniGoMani repo. I quit!')
                os.sys.exit(1)

            try:
                copytree(f'cp -rf {temp_dirname}/user_data/', f'{target_dir}/user_data/')
            except Exception:
                pass

    def apply_best_results(self, strategy: str) -> bool:
        """Apply HO results to the hyperopt.json file.

        :param strategy (str): The name of the strategy. Is used to determine ho-results file.
        :return bool: True if ho-results file was successfully applied. False otherwise.
        """
        ho_json = '{0}/user_data/strategies/{1}.json'.format(self.basedir, strategy)
        # TODO use the filename as specified in configuration
        ho_config = '{0}/user_data/mgm-config-hyperopt.json'.format(self.basedir)

        if os.path.isfile(ho_json) is False:
            self.logger.error('🤷 Failed applying best results because the results file {} does not exist.'.format(ho_json))
            return False

        # Apply best results from MoniGoManiHyperStrategy.json to mgm-config-hyperopt.json
        if strategy == 'MoniGoManiHyperStrategy':
            copy2(ho_json, ho_config)

        # Cleanup leftover file
        if os.path.isfile(ho_json) is True:
            os.remove(ho_json)

        return True

    def run_command(self, command: str, output_file_name: str = None):
        """Execute shell command and log output to mgm logfile.

        :param command (str): Shell command to execute, sir!
        :param output_file_name: (str) Name of the '.log' file.
            Defaults to 'Results-<Current-DateTime>.log'
        :return returncode: (int) The returncode of the subprocess
        """
        if command is None or command == '':
            self.logger.error(
                '🤷 Please pass a command through. Without command no objective, sir!'
            )
            sys.exit(1)

        cmd = shlex.split(command)
        cmd = ' '.join(cmd)

        if output_file_name is not None:
            output = shell_output(cmd, universal_newlines=True)
            with open(output_file_name, 'w+') as output_file:
                output_file.write(output)
                output_file.close()

            self.logger.debug(output)
            return 0

        return shell_call(cmd, shell=True)
