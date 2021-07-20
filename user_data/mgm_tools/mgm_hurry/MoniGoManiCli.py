# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
#
# ___  ___               _  _____        ___  ___               _  _____  _  _
# |  \/  |              (_)|  __ \       |  \/  |              (_)/  __ \| |(_)
# | .  . |  ___   _ __   _ | |  \/  ___  | .  . |  __ _  _ __   _ | /  \/| | _
# | |\/| | / _ \ | '_ \ | || | __  / _ \ | |\/| | / _` || '_ \ | || |    | || |
# | |  | || (_) || | | || || |_\ \| (_) || |  | || (_| || | | || || \__/\| || |
# \_|  |_/ \___/ |_| |_||_| \____/ \___/ \_|  |_/ \__,_||_| |_||_| \____/|_||_|
#
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import datetime
import json
import os
import shutil
import subprocess
import sys
import yaml
# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class MoniGoManiCli:
    """
    MoniGoManiCli is responsible for all MGM related tasks.
    """

    def __init__(self, basedir, logger):
        self.basedir = basedir
        self.logger = logger

    def installation_exists(self) -> bool:
        """
        Checks if the MGM Hyper Strategy installation exists

        :return success: (bool)
        """
        if os.path.exists(f'{self.basedir}/user_data/mgm-config.json') is False:
            self.logger.warning('🤷♂️ No "mgm-config.json" file found.')
            return False

        if os.path.exists(f'{self.basedir}/user_data/strategies/MoniGoManiHyperStrategy.py') is False:
            self.logger.warning('🤷♂️ No "MoniGoManiHyperStrategy.py" file found.')
            return False

        self.logger.debug('👉 MoniGoManiHyperStrategy and configuration found √')
        return True

    def create_config_files(self, target_dir: str) -> bool:
        """
        Copy example files as def files.

        :param target_dir: (string) The target dir where the "mgm-config.example.json" exists.
        :return success: (bool) True if files are created, false if something failed.
        Todo: Check if the example files exist
        """
        if os.path.exists(f'{target_dir}/user_data/mgm-config.json') is False:
            shutil.copyfile(f'{target_dir}/user_data/mgm-config.example.json',
                            f'{target_dir}/user_data/mgm-config.json')

        if os.path.exists(f'{target_dir}/user_data/mgm-config-private.json') is False:
            shutil.copyfile(f'{target_dir}/user_data/mgm-config-private.example.json',
                            f'{target_dir}/user_data/mgm-config-private.json')

        self.logger.info('👉 MoniGoMani config files prepared √')
        return True

    def load_config_files(self) -> dict:
        """
        Loads & Returns all the MoniGoMani Configuration files including:
        - mgm-config
        - mgm-config-private
        - mgm-config-hyperopt
        - mgm-config-hurry

        :return dict: Dictionary containing all the MoniGoMani Configuration files
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
            'mgm-config-hyperopt': {}
        }

        for mgm_config_filename in mgm_config_files:
            # Check if the MoniGoMani config filename exist in the ".hurry" config file
            if ('mgm_config_names' not in hurry_config) or \
                    (mgm_config_filename not in hurry_config['mgm_config_names']):
                self.logger.error(f'🤷 No "{mgm_config_filename}" filename found in the ".hurry" \
                                  config file. Please run: mgm-hurry setup')
                sys.exit(1)

            mgm_config_filepath = f'{self.basedir}/user_data/{hurry_config["mgm_config_names"][mgm_config_filename]}'

            # Check if the mandatory MoniGoMani config files exist
            if (os.path.isfile(mgm_config_filepath) is False) and \
                    (mgm_config_filename in ['mgm-config', 'mgm-config-private']):
                self.logger.error(f'🤷 No "{mgm_config_filename}" file found in the "user_data" \
                                  directory. Please run: mgm-hurry setup')
                sys.exit(1)

            elif (os.path.isfile(mgm_config_filepath) is False) and (mgm_config_filename == 'mgm-config-hyperopt'):
                self.logger.info(f'No "{mgm_config_filename}" file found in the "user_data" directory.')

            # Load the MoniGoMani config file as an object and parse it as a dictionary
            else:
                file_object = open(mgm_config_filepath, )
                json_data = json.load(file_object)
                mgm_config_files[mgm_config_filename] = json_data

        # Append the previously loaded MGM-Hurry config file
        mgm_config_files['mgm-config-hurry'] = hurry_config

        return mgm_config_files

    def _exec_cmd(self, cmd: str, save_output: bool = False, output_path: str = None, output_file_name: str = None) -> int:
        """
        Executes shell command and logs output as debug output.

        :param cmd: (str) The command, sir
        :param save_output: (bool) Save the output to a '.log' file. Defaults to False
        :param output_path: (str) Path to the output of the '.log' file.
            Defaults to 'Some Test Results/MoniGoMani_version_number/'
        :param output_file_name: (str) Name of the '.log' file. Defaults to 'Results-<Current-DateTime>.log'
        :return returncode: (int) The returncode of the subprocess
        """

        if cmd is None or cmd == '':
            self.logger.error('🤷 Please pass a command through. Without command no objective, sir!')
            sys.exit(1)

        return_code = 1

        if save_output is True:
            if output_path is None:
                output_path = f'{self.basedir}/Some Test Results/'
                if not os.path.isdir(output_path):
                    os.mkdir(output_path)

                mgm_config_files = self.load_config_files()
                output_path = f'{output_path}{mgm_config_files["mgm-config-private"]["bot_name"]}/'

            if output_file_name is None:
                output_file_name = f'MGM-Hurry-Command-Results-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.log'

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
