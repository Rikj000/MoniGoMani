# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

# --- ↑↓ Do not remove these libs ↑↓ ---------------------------------------------------------------

"""MoniGoManiConfig is the module responsible for all MGM Config related tasks."""

# ___  ___               _  _____        ___  ___               _  _____                 __  _
# |  \/  |              (_)|  __ \       |  \/  |              (_)/  __ \               / _|(_)
# | .  . |  ___   _ __   _ | |  \/  ___  | .  . |  __ _  _ __   _ | /  \/  ___   _ __  | |_  _   __ _
# | |\/| | / _ \ | '_ \ | || | __  / _ \ | |\/| | / _` || '_ \ | || |     / _ \ | '_ \ |  _|| | / _` |
# | |  | || (_) || | | || || |_\ \| (_) || |  | || (_| || | | || || \__/\| (_) || | | || |  | || (_| |
# \_|  |_/ \___/ |_| |_||_| \____/ \___/ \_|  |_/ \__,_||_| |_||_| \____/ \___/ |_| |_||_|  |_| \__, |
#                                                                                                __/ |
#                                                                                               |___/

import os
import json
import sys
import shutil
import yaml

from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger

# --- ↑ Do not remove these libs ↑ ---------------------------------------------------------------


class MoniGoManiConfig(object):
    """MoniGoManiConfig is responsible for all MGM Config related tasks."""

    __config: dict
    __basedir: str
    __full_path_config: str
    __mgm_logger: MoniGoManiLogger

    def __init__(self, basedir: str):
        self.__basedir = basedir
        self.__mgm_logger = MoniGoManiLogger(basedir).get_logger()
        self.__full_path_config = '{0}/.hurry'.format(self.__basedir)

        # if .hurry file exists
        if self.valid_config_file_present() is False:
            self.__create_default_config()

        self.__config = self.__read_config()

    @property
    def config(self) -> dict:
        return self.__config

    @config.setter
    def config(self, data: dict):
        self.__config = data

    def get(self, element: str):
        if element not in self.__config:
            return False

        return self.__config[element]

    @property
    def logger(self) -> MoniGoManiLogger:
        return self.__mgm_logger

    @property
    def basedir(self) -> str:
        return self.__basedir

    def reload(self) -> bool:
        """Reload config file and store as property in current object.

        :return bool: True if config is read, False if config could not be read.
        """
        if self.valid_config_file_present() is not True:
            self.logger.error('Failed to reload config. No valid config file present.')
            return False

        self.config = self.__read_config()

        return True

    def valid_config_file_present(self) -> bool:
        """Check if the .hurry config file exists on disk."""
        if os.path.isfile(self.__full_path_config) is not True:
            self.logger.warning(
                'Could not find .hurry config file at {0}'.format(
                    self.__full_path_config))
            return False

        with open(self.__full_path_config, 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        # Check if all required config keys
        # are present in config file
        for key in ['exchange', 'install_type', 'timerange']:
            if not config['config'][key]:
                return False

        return True

    def create_config_files(self, target_dir: str) -> bool:
        """Copy example files as def files.

        :param target_dir (str): The target dir where the "mgm-config.example.json" exists.
        :return success (bool): True if files are created, false if something failed.
        """
        example_files = [
            {
                'src': 'mgm-config.example.json',
                'dest': 'mgm-config.json',
            },
            {
                'src': 'mgm-config-private.example.json',
                'dest': 'mgm-config-private.json',
            },
        ]

        for example_file in example_files:
            src_file = target_dir + '/user_data/' + example_file['src']

            if not os.path.isfile(src_file):
                self.logger.error('❌ Bummer. Cannot find the example file "{0}" to copy from.'.format(example_file['src']))
                return False

            dest_file = target_dir + '/user_data/' + example_file['dest']

            if os.path.isfile(dest_file):
                self.logger.warning('⚠️ The target file "{0}" already exists. Is cool.'.format(example_file['dest']))
                continue

            shutil.copyfile(src_file, dest_file)

        self.logger.info('👉 MoniGoMani config files prepared √')
        return True

    def load_config_files(self) -> dict:
        """Load & Return all the MoniGoMani Configuration files.

        Including:
            - mgm-config
            - mgm-config-private
            - mgm-config-hyperopt

        :return dict: Dictionary containing all the MoniGoMani Configuration files in format
                      { mgm-config: dict, mgm-config-private: dict, mgm-config-hyperopt: dict }
        """

        hurry_config = self.read_hurry_config()

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
                self.logger.critical(
                    '🤷 No "{0}" filename found in the ".hurry" config file. Please run: mgm-hurry setup'
                    .format(mgm_config_filename))
                sys.exit(1)

            # Full path to current config file
            mgm_config_filepath = self._get_full_path_for_config_name(hurry_config, mgm_config_filename)

            # Read config file contents
            mgm_config_files[mgm_config_filename] = self.load_config_file(mgm_config_filepath)

        return mgm_config_files

    def read_hurry_config(self) -> dict:
        """Read .hurry configuration dotfile and return its yaml contents as dict.

        TODO: move to module MoniGoManiHurry.py as this is more .hurry specific

        :return dictionary containing the config section of .hurry file. None if failed.
        """
        with open('{0}/.hurry'.format(self.basedir), 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        hurry_config = config['config'] if 'config' in config else None

        return hurry_config

    def get_config_filename(self, cfg_key: str) -> str:
        """Transforms given cfg_key into the corresponding config filename.

        TODO: move along with read_hurry_config to hurry config module.

        :param cfg_key (str): the config name (key) to parse.
        :return abs_path (str): the absolute path to the asked config file.
        """
        hurry_config = self.read_hurry_config()
        return self._get_full_path_for_config_name(hurry_config, cfg_key)

    def load_config_file(self, filename: str) -> dict:
        """Read json-file contents and return its data.

        :param filename (str): The absolute path + filename to the json config file.
        :return dict: The json content of the file. json.load() return. None if failed.
        """
        if os.path.isfile(filename) is False:
            self.logger.error('🤷 No "{0}" file found in the "user_data" directory. Please run: mgm-hurry setup'.format(filename))
            return None

        # Load the MoniGoMani config file as an object and parse it as a dictionary
        with open(filename, ) as file_object:
            json_data = json.load(file_object)
            return json_data

    def write(self, config: dict = None):
        """ Write config-array to ".hurry" config file and load its contents into config-property.

        Writes the passed config dictionary or if nothing passed, it will write default values.

        :param config: (dict, Optional) The config values to store. Defaults to None.
        """
        if config is None:
            config = {
                'config': {
                    'install_type': 'docker',
                    'ft_binary': 'freqtrade',
                    'timerange': '20210501-20210616',
                    'exchange': 'binance',
                    'hyperopt': {
                        'strategy': 'MoniGoManiHyperStrategy',
                        'loss': 'WinRatioAndProfitRatioLoss',
                        'spaces': 'buy sell',
                        'quote': 'USDT',
                        'epochs': 1000
                    },
                    'mgm_config_names': {
                        'mgm-config': 'mgm-config.json',
                        'mgm-config-private': 'mgm-config-private.json',
                        'mgm-config-hyperopt': 'mgm-config-hyperopt.json'
                    }
                }
            }

        # Protection to prevent from writing
        # no data at all to mgm-config.
        if len(config) == 0 or 'config' not in config or 'mgm_config_names' not in config['config']:
            self.logger.error(
                '🤯 Sorry, but looks like no configuration data would have been written, '
                'resulting in an empty config file I quit.')
            sys.exit(1)

        with open(self.__full_path_config, 'w+') as cfg_file:
            yaml.dump(config, cfg_file)

        self.reload()

        self.logger.info('🍺 Configuration data written to ".hurry" file')

    def _get_full_path_for_config_name(self, hurry_config: dict,
                                       cfg_name: str) -> str:
        """Parses the full path to given config file based on settings in .hurry.

        TODO: Move along with read_hurry_config to module MoniGoManiHurry.py

        :param hurry_config (dict): The dictionary containing the hurry dotfile yaml config.
        :return abs_path: The absolute path to the asked config file.
        """
        # Full path to current config file
        mgm_config_filepath = '{0}/user_data/{1}'.format(
            self.basedir,
            hurry_config['mgm_config_names'][cfg_name],
        )

        return mgm_config_filepath

    def __read_config(self) -> dict:
        """Reads config values out of ".hurry" config file.

        :return config (dict) Dictionary containing all config key/value pairs. Or returns None.
        """
        with open(self.__full_path_config, 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        if 'config' in config:
            return config['config']

        # Something happened on the way to heaven.

        return None

    def __create_default_config(self):
        """ Creates default .hurry config file with default values. """
        self.write()