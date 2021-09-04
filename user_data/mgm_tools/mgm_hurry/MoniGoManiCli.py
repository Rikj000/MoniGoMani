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

import glob
import os
import subprocess
import sys
import tempfile
from shutil import copy2, copytree

import logger
import pygit2
from pygit2 import Repository, clone_repository
from yaspin import yaspin

from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger, MGMLogger

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

GIT_URL_MONIGOMANI: str = 'https://github.com/Rikj000/MoniGoMani.git'


class MoniGoManiCli(object):
    """
    Use this module to communicate with the MoniGoMani HyperStrategy.

    Attributes:
        logger              The logger function of the MoniGoManiCli module.
        monigomani_config   The MoniGoManiConfig object.
    """
    logger: MoniGoManiLogger
    monigomani_config: MoniGoManiConfig

    def __init__(self, basedir):
        """
        Let's talk command-line-ish.

        :param basedir (str): The base directory of your Freqtrade & MoniGoMani installation
        """
        self.basedir = basedir
        self.logger = MoniGoManiLogger(self.basedir).get_logger()
        self.monigomani_config = MoniGoManiConfig(self.basedir)

    def installation_exists(self) -> bool:
        """
        Check if the MGM Hyper Strategy installation exists.

        :return success (bool): Whether or not the config and strategy files are found.
        """
        with yaspin(text='', color='cyan') as sp:

            if self._mgm_config_json_exists() is False:
                mgm_config_name = self.monigomani_config.config['mgm_config_names']['mgm-config']
                sp.red.write(f'🤷 No "{mgm_config_name}" file found.')
                self.logger.warning(f'🤷 No "{mgm_config_name}" file found.')
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
        Checks if `mgm-config` exists

        :return bool: Returns true if `mgm-config` exists, returns false if not.
        """
        mgm_config_name = self.monigomani_config.config['mgm_config_names']['mgm-config']
        return os.path.exists(f'{self.basedir}/user_data/{mgm_config_name}')

    def _mgm_hyperstrategy_file_exists(self) -> bool:
        """
        Checks if `MoniGoManiHyperStrategy.py` exists

        :return bool: Returns true if `MoniGoManiHyperStrategy.py` exists, returns false if not.
        """
        return os.path.exists(f'{self.basedir}/user_data/strategies/MoniGoManiHyperStrategy.py')

    def download_setup_mgm(self, target_dir: str = None, branch: str = 'develop', commit: str = None):
        """
        Install MoniGoMani using a git clone to target_dir.

        :param target_dir: (str) Specify a target_dir to install MoniGoMani. Defaults to 'os.getcwd()'.
        :param branch: (str) Checkout a specific branch. Defaults to 'develop'.
        :param commit: (str) Checkout a specific commit. Defaults to None aka latest.
        """
        with tempfile.TemporaryDirectory() as temp_dirname:
            if target_dir is None:
                target_dir = os.getcwd()

            text = '👉  Clone MoniGoMani repository'
            text = text if commit is None else f'{text} and resetting to commit {commit}'
            with yaspin(text=text, color='cyan') as sp:
                repo = clone_repository(GIT_URL_MONIGOMANI, temp_dirname, checkout_branch=branch)
                if commit is not None:
                    repo.reset(commit, pygit2.GIT_RESET_HARD)

                if not isinstance(repo, Repository):
                    sp.red.write('Failed to download MoniGoMani repo. I quit!')
                    self.logger.critical('Failed to clone MoniGoMani repo. I quit!')
                    sys.exit(1)

                sp.green.ok('✔')

            with yaspin(text='👉  Copy MoniGoMani to the monigomani folder in the target directory and '
                             'symbolic linking files', color='cyan') as sp:
                try:
                    if self.copy_and_link_installation_files(temp_dirname, target_dir):
                        sp.green.ok('✔ Downloading & Installing MoniGoMani completed!')
                    else:
                        sp.red.write('😕 MoniGoMani installation failed')
                        sys.exit(1)
                except Exception as e:
                    sp.red.write(str(e))
                    sp.red.write('😕 MoniGoMani installation failed')
                    sys.exit(1)

    def copy_and_link_installation_files(self, temp_dirname: str, target_dir: str) -> bool:
        """
        Copy the installation files to the target directory and symbolic link them.

        :param temp_dirname: (str) The source directory where installation files exist.
        :param target_dir: (str) The target directory where the installation files should be copied to.
        :return bool: True if copying and symbolic linking was executed successfully, False if failed.
        """
        try:
            mgm_folder = '/monigomani'
            if not os.path.exists(target_dir + mgm_folder):
                os.makedirs(target_dir + mgm_folder, exist_ok=True)

            if os.path.isfile(f'{target_dir + mgm_folder}/setup.exp'):
                os.remove(f'{target_dir + mgm_folder}/setup.exp')

            os.chmod(f'{temp_dirname}/setup.exp', 0o444)
            copytree(temp_dirname, target_dir + mgm_folder, dirs_exist_ok=True)

            if os.path.isfile(f'{target_dir}/docker-compose.yml'):
                os.remove(f'{target_dir}/docker-compose.yml')

            # Symlink separate files and whole directories
            symlink_objects = {
                'Documentation',
                'Some Test Results',
                'docker/Dockerfile.MoniGoMani',
                'user_data/logs/freqtrade.log',
                'user_data/mgm_pair_lists',
                'user_data/mgm_tools',
                'user_data/__init__.py',
                'docker-compose.yml',
                'mgm-hurry',
                'requirements-mgm.txt'
            }

            for symlink_object in symlink_objects:
                os.symlink(f'{target_dir + mgm_folder}/{symlink_object}', f'{target_dir}/{symlink_object}')
            os.symlink(f'{target_dir + mgm_folder}/README.md', f'{target_dir}/README-MGM.md')

            # Symlink all files inside the given directories separately
            symlink_directory_contents = {
                'tests',
                'user_data/hyperopts',
                'user_data/strategies'
            }

            for directory in symlink_directory_contents:
                for symlink_object in glob.glob(f'{target_dir + mgm_folder}/{directory}/*'):
                    if os.path.isfile(symlink_object):
                        os.symlink(symlink_object, symlink_object.replace(mgm_folder, ''))

            return True
        except Exception as e:
            self.logger.critical(str(e))
            return False

    def apply_mgm_results(self, strategy: str = 'MoniGoManiHyperStrategy') -> bool:
        """
        Apply MoniGoMani HyperOpt results to the `mgm-config-hyperopt` file.

        :param strategy: (str) The name of the strategy. Is used to determine ho-results file.
        :return bool: True if ho-results file was successfully applied. False otherwise.
        """
        strategy_ho_json_name = f'{strategy}.json'
        strategy_ho_json_path = f'{self.basedir}/user_data/strategies/{strategy_ho_json_name}'

        if os.path.isfile(strategy_ho_json_path) is False:
            self.logger.error(f'🤷 Failed applying best results because the HyperOpt results file '
                              f'"{strategy_ho_json_name}" does not exist.')
            return False

        # Apply best results from `MoniGoManiHyperStrategy.json` to `mgm-config-hyperopt`
        if strategy == 'MoniGoManiHyperStrategy':
            mgm_ho_json_name = self.monigomani_config.config['mgm_config_names']['mgm-config-hyperopt']
            mgm_ho_json_path = f'{self.basedir}/user_data/{mgm_ho_json_name}'

            copy2(strategy_ho_json_path, mgm_ho_json_path)
            # Cleanup leftover file `MoniGoManiHyperStrategy.json`
            os.remove(strategy_ho_json_path)
        else:
            self.logger.debug(f'Freqtrade already automatically applied the results '
                              f'for {strategy} at {strategy_ho_json_path}, all good!')

        return True

    def run_command(self, command: str, output_file_name: str = None):
        """
        Execute shell command and log output to mgm logfile.

        :param command: (str) Shell command to execute, sir!
        :param output_file_name: (str) Name of the absolute path to the '.log' file.
        :return returncode: (int) The returncode of the subprocess
        """

        if command is None or command == '':
            self.logger.error('🤷 Please pass a command through. Without command no objective, sir!')
            sys.exit(1)
        return_code = 1

        if output_file_name is not None:
            output_file = open(output_file_name, 'w')
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, encoding='utf-8')

        hyperopt_results = []
        mgm_logger = MGMLogger(logger.logger)
        monigomani_logger = MoniGoManiLogger(self.basedir)
        elapsed_time = 'Elapsed Time:'
        eta = '| [ETA:'

        for line in process.stdout:
            final_line = mgm_logger.clean_line(line)

            # Save the output to a '.log' file if enabled
            if (mgm_logger.filter_line(final_line) is False) and \
                (output_file_name is not None) and (eta not in final_line):
                output_file.write(final_line)

            # Check if a new HyperOpt Results line is found, store it in RAM and re-print the whole HyperOpt Table if so
            response = monigomani_logger.store_hyperopt_results(hyperopt_results, final_line)
            if (response['results_updated'] is True) or (eta not in final_line) and (elapsed_time in final_line):
                hyperopt_results = response['hyperopt_results']
                # Skip the initial header
                if len(hyperopt_results) > 3:
                    for hyperopt_results_line in hyperopt_results:
                        sys.stdout.write(hyperopt_results_line)
                if (eta not in final_line) and (elapsed_time in final_line):
                    sys.stdout.write(final_line)
            else:
                sys.stdout.write(final_line)

        process.wait()
        return return_code

    @staticmethod
    def timeframe_to_minutes(timeframe):
        amount = int(timeframe[0:-1])
        unit = timeframe[-1]
        if 'y' == unit:
            scale = 60 * 60 * 24 * 365
        elif 'M' == unit:
            scale = 60 * 60 * 24 * 30
        elif 'w' == unit:
            scale = 60 * 60 * 24 * 7
        elif 'd' == unit:
            scale = 60 * 60 * 24
        elif 'h' == unit:
            scale = 60 * 60
        elif 'm' == unit:
            scale = 60
        elif 's' == unit:
            scale = 1
        else:
            raise TypeError(f'timeframe unit {unit} is not supported')
        return (amount * scale) // 60
