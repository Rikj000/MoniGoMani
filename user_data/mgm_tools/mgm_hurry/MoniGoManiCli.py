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

import datetime
import json
import os
import shutil
import subprocess  # noqa: S404 (skip security check)
import sys

import yaml

# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class MoniGoManiCli(object):
    """Use this module to communicate with the mgm hyperstrategy,."""

    def __init__(self, basedir, logger):
        """Instantiate a new object of mgm cli.

        Args:
            basedir (str): The directory
            logger (logger): The logger
        """
        self.basedir = basedir
        self.logger = logger

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

    def create_config_files(self, target_dir: str) -> bool:
        """Copy example files as def files.

        Args:
            target_dir (str): The target dir where the "mgm-config.example.json" exists.

        Returns:
            success (bool): True if files are created, false if something failed.
        """
        example_files = [
            {
                'src': 'mgm-config.example.json',
                'dest': 'mgm-config.json',
            },
            {
                'src': 'mgm-config.example.json',
                'dest': 'mgm-config.json',
            },
        ]

        for example_file in example_files:
            src_file = target_dir + '/user_data/' + example_file['src']

            if not os.path.isfile(src_file):
                self.logger.error('❌ Bummer. Cannot find the example file "{0}" to copy from.'.format(example_file['src']))
                return False

            dest_file = target_dir + '/user_data/' + example_file['dest']

            if os.path.isfile(dest_file):
                self.logger.warning('⚠️ The target file "{0}" already exists. Would be overwritten.'.format(example_file['dest']))
                return False

            shutil.copyfile(src_file, dest_file)

        self.logger.info('👉 MoniGoMani config files prepared √')
        return True

    def load_config_files(self) -> dict:
        """Load & Return all the MoniGoMani Configuration files.

        Including:
            - mgm-config
            - mgm-config-private
            - mgm-config-hyperopt
            - mgm-config-hurry

        Returns:
            dict: Dictionary containing all the MoniGoMani Configuration files
        """

        # Load the MGM-Hurry Config file if it exists
        with open('.hurry', 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        hurry_config = config['config'] if 'config' in config else None

        if hurry_config is None:
            self.logger.error('🤷 No Hurry config file found. Please run: mgm-hurry setup')
            sys.exit(1)

        # Start loading the MoniGoMani config files
        mgm_config_files = {
            'mgm-config': {},
            'mgm-config-private': {},
            'mgm-config-hyperopt': {},
        }

        for mgm_config_filename in mgm_config_files:
            # Check if the MoniGoMani config filename exist in the ".hurry" config file
            if 'mgm_config_names' not in hurry_config or mgm_config_filename not in hurry_config['mgm_config_names']:
                self.logger.error('🤷 No "{0}" filename found in the ".hurry" config file. Please run: mgm-hurry setup'.format(mgm_config_filename))
                sys.exit(1)

            mgm_config_filepath = '{0}/user_data/{1}'.format(
                self.basedir,
                hurry_config['mgm_config_names'][mgm_config_filename],
            )

            # Check if the mandatory MoniGoMani config files exist
            if os.path.isfile(mgm_config_filepath) is False:
                if mgm_config_filename in ['mgm-config', 'mgm-config-private']:
                    self.logger.error('🤷 No "{0}" file found in the "user_data" directory. Please run: mgm-hurry setup'.format(mgm_config_filename))
                    sys.exit(1)

            elif (os.path.isfile(mgm_config_filepath) is False) and (mgm_config_filename == 'mgm-config-hyperopt'):
                self.logger.info('No "{0}" file found in the "user_data" directory.'.format(mgm_config_filename))

            # Load the MoniGoMani config file as an object and parse it as a dictionary
            else:
                file_object = open(mgm_config_filepath, )
                json_data = json.load(file_object)
                mgm_config_files[mgm_config_filename] = json_data

        # Append the previously loaded MGM-Hurry config file
        mgm_config_files['mgm-config-hurry'] = hurry_config

        return mgm_config_files

    def exec_cmd(self, cmd: str, save_output: bool = False, output_path: str = None, output_file_name: str = None) -> int:
        """Execute shell command and logs output as debug output.

        Args:
            cmd (str): The command, sir
            save_output (bool): Save the output to a '.log' file. Defaults to False
            output_path (str): Path to the output of the '.log' file. Defaults to 'Some Test Results/MoniGoMani_version_number/'
            output_file_name (str): Name of the '.log' file. Defaults to 'Results-<Current-DateTime>.log'

        Returns:
            returncode (int): The returncode of the subprocess
        """
        if cmd is None or cmd == '':
            self.logger.error('🤷 Please pass a command through. Without command no objective, sir!')
            sys.exit(1)

        return_code = 1

        if save_output is True:
            if output_path is None:
                output_path = '{0}/Some Test Results/'.format(self.basedir)

            if not os.path.isdir(output_path):
                os.mkdir(output_path)

            mgm_config_files = self.load_config_files()

            # create path like foo/bar/
            # and be sure only 1 repeating / is used
            output_path = os.path.normpath(
                os.path.join(
                    output_path,
                    mgm_config_files['mgm-config-private']['bot_name'],
                    '/',
                ),
            )

            if output_file_name is None:
                output_file_name = 'MGM-Hurry-Command-Results-{0}.log'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))

            if not os.path.isdir(output_path):
                os.mkdir(output_path)

            output_file = open(output_path + output_file_name, 'w')

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, encoding='utf-8')

        for line in process.stdout:
            if save_output is True:
                second_splitter = line.find(' - ', line.find(' - ') + 1) + 3
                trimmed_line = line[second_splitter:len(line)]
                if self.filter_line(trimmed_line) is False:
                    output_file.write(trimmed_line)
            sys.stdout.write(line)
        process.wait()

        return return_code

    def _exec_cmd(self, cmd: str, save_output: bool = False, output_path: str = None, output_file_name: str = None) -> int:
        self.logger.deprecated('Calling _exec_cmd is deprecated. Please switch to public method exec_cmd()')
        return self.exec_cmd(cmd, save_output, output_path, output_file_name)
