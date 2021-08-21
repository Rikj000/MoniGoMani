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
import shlex
import sys
import tempfile
from shutil import copy2, copytree

from pygit2 import Repository, clone_repository
from shell_command import shell_call, shell_output
from yaspin import yaspin

from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger


# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

GIT_URL_MONIGOMANI: str = 'https://github.com/Rikj000/MoniGoMani.git'


class MoniGoManiCli(object):
    """
    Use this module to communicate with the MoniGoMani HyperStrategy.

    Attributes:
        logger      The logger function of the MoniGoManiCli module.
    """
    logger: MoniGoManiLogger

    def __init__(self, basedir):
        """
        Let's talk command-line-ish.

        :param basedir (str): The base directory of your Freqtrade & MoniGoMani installation
        """
        self.basedir = basedir
        self.logger = MoniGoManiLogger(self.basedir).get_logger()

    def installation_exists(self) -> bool:
        """
        Check if the MGM Hyper Strategy installation exists.

        :return success (bool): Whether or not the config and strategy files are found.
        """
        with yaspin(text='', color='cyan') as sp:

            if self._mgm_config_json_exists() is False:
                sp.red.write('🤷 No "mgm-config.json" file found.')
                self.logger.warning('🤷 No "mgm-config.json" file found.')
                return False

            if self._mgm_hyperstrategy_file_exists() is False:
                sp.red.write('🤷 No "MoniGoManiHyperStrategy.py" file found.')
                self.logger.warning('🤷 No "MoniGoManiHyperStrategy.py" file found.')
                return False

            sp.green.ok('✔ MoniGoManiHyperStrategy and configuration found')

        self.logger.debug('MoniGoManiHyperStrategy and configuration found √')

        return True

    def _mgm_config_json_exists(self) -> bool:
        """
        Checks if `mgm-config.json` exists

        :return bool: Returns true if `mgm-config.json` exists, returns false if not.
        """
        return os.path.exists('{0}/user_data/mgm-config.json'.format(self.basedir))

    def _mgm_hyperstrategy_file_exists(self) -> bool:
        """
        Checks if `MoniGoManiHyperStrategy.py` exists

        :return bool: Returns true if `MoniGoManiHyperStrategy.py` exists, returns false if not.
        """
        return os.path.exists('{0}/user_data/strategies/MoniGoManiHyperStrategy.py'.format(self.basedir))

    def download_setup_mgm(self, branch: str = 'develop', target_dir: str = None):
        """
        Install MoniGoMani using a git clone to target_dir.

        :param branch: (str) Checkout a specific branch. Defaults to 'develop'.
        :param target_dir: (str) Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        """
        with tempfile.TemporaryDirectory() as temp_dirname:
            with yaspin(text='👉  Downloading MoniGoMani repository', color='cyan') as sp:
                repo = clone_repository(GIT_URL_MONIGOMANI, temp_dirname, checkout_branch=branch)
            if not isinstance(repo, Repository):
                sp.red.write('Failed to download MoniGoMani repo. I quit!')
                self.logger.critical('Failed to clone MoniGoMani repo. I quit!')
                sys.exit(1)

            try:
                sp.write('Copy MoniGoMani to target directory')
                copytree(f'cp -rf {temp_dirname}/user_data/', f'{target_dir}/user_data/')
            except Exception:
                pass

            sp.green.ok('✔ Downloading MoniGoMani completed')

    def apply_best_results(self, strategy: str, config: MoniGoManiConfig = None) -> bool:
        """
        Apply HyperOpt results to the `mgm-config-hyperopt.json` file.

        :param strategy: (str) The name of the strategy. Is used to determine ho-results file.
        :param config: (MoniGoManiConfig, optional) Use the `mgm-config-hyperopt path` from config.
        :return bool: True if ho-results file was successfully applied. False otherwise.
        """
        ho_json = '{0}/user_data/strategies/{1}.json'.format(self.basedir, strategy)
        # ToDo: Use the filename as specified in configuration
        ho_config = '{0}/user_data/mgm-config-hyperopt.json'.format(self.basedir)

        if os.path.isfile(ho_json) is False:
            self.logger.error('🤷 Failed applying best results because the results file {} does not exist.'
                              .format(ho_json))
            return False

        # Apply best results from `MoniGoManiHyperStrategy.json` to `mgm-config-hyperopt.json`
        if strategy == 'MoniGoManiHyperStrategy':
            copy2(ho_json, ho_config)

        # Cleanup leftover file
        if os.path.isfile(ho_json) is True:
            os.remove(ho_json)

        return True

    def run_command(self, command: str, output_file_name: str = None):
        """
        Execute shell command and log output to mgm logfile.

        :param command: (str) Shell command to execute, sir!
        :param output_file_name: (str) Name of the '.log' file. Defaults to 'Results-<Current-DateTime>.log'
        :return returncode: (int) The returncode of the subprocess
        """
        if command is None or command == '':
            self.logger.error('🤷 Please pass a command through. Without command no objective, sir!')
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
