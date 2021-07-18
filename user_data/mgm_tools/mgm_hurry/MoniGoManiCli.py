# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import json
import os
import shutil
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
            sys.exit(0)

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
                sys.exit(0)

            mgm_config_filepath = f'{self.basedir}/user_data/{hurry_config["mgm_config_names"][mgm_config_filename]}'

            # Check if the mandatory MoniGoMani config files exist
            if (os.path.isfile(mgm_config_filepath) is False) and \
                    (mgm_config_filename in ['mgm-config', 'mgm-config-private']):
                self.logger.error(f'🤷 No "{mgm_config_filename}" file found in the "user_data" \
                                  directory. Please run: mgm-hurry setup')
                sys.exit(0)

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
