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

import json
import os
import shutil
import sys
from operator import xor

import yaml

from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger


# --- ↑ Do not remove these libs ↑ ---------------------------------------------------------------


class MoniGoManiConfig(object):
    """
    MoniGoManiConfig is responsible for all MoniGoMani Config related tasks.

    Attributes:
        __config            Dictionary containing the configuration parameters.
        __basedir           The basedir where the monigomani install lives.
        __full_path_config  Absolute path to .hurry config file.
        __mgm_logger        The logger function of the MoniGoManiCli module.
    """
    __config: dict
    __basedir: str
    __full_path_config: str
    __mgm_logger: MoniGoManiLogger

    def __init__(self, basedir: str):
        """
        MoniGoMani has configuration.

        :param basedir: (str) The base directory where Freqtrade & MoniGoMani are installed
        """
        self.__basedir = basedir
        self.__mgm_logger = MoniGoManiLogger(basedir).get_logger()
        self.__full_path_config = '{0}/.hurry'.format(self.__basedir)

        # if .hurry file does not exist
        if self.valid_hurry_dotfile_present() is False:
            self.__create_default_config()

        self.__config = self.read_hurry_config()

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
        """
        Reload config file and store as property in current object.

        :return bool: True if config is read, False if config could not be read.
        """
        if self.valid_hurry_dotfile_present() is not True:
            self.logger.error('Failed to reload config. No valid hurry dotfile present.')
            return False

        self.config = self.read_hurry_config()

        return True

    def valid_hurry_dotfile_present(self) -> bool:
        """
        Check if the .hurry config file exists on disk.

        :return bool: Return true if the config files exist, false if not
        """
        if os.path.isfile(self.__full_path_config) is not True:
            self.logger.warning('Could not find .hurry config file at {0}'.format(self.__full_path_config))
            return False

        with open(self.__full_path_config, 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        # Check if all required config keys are present in config file
        for key in ['exchange', 'install_type', 'timerange']:
            if not config['config'][key]:
                return False

        return True

    def create_config_files(self, target_dir: str) -> bool:
        """
        Copy example files as def files.

        :param target_dir: (str) The target dir where the "mgm-config.example.json" exists.
        :return bool: True if files are created successfully, false if something failed.
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
            src_file = target_dir + '/monigomani/user_data/' + example_file['src']

            if not os.path.isfile(src_file):
                self.logger.error('❌ Bummer. Cannot find the example file "{0}" '
                                  'to copy from.'.format(example_file['src']))
                return False

            dest_file = target_dir + '/user_data/' + example_file['dest']

            if os.path.isfile(dest_file):
                self.logger.warning('⚠️ The target file "{0}" already exists. Is cool.'.format(example_file['dest']))
                continue

            shutil.copyfile(src_file, dest_file)

        self.logger.info('👉 MoniGoMani config files prepared √')
        return True

    def load_config_files(self) -> dict:
        """
        Load & Return all the MoniGoMani Configuration files.

        Including:
            - mgm-config
            - mgm-config-private
            - mgm-config-hyperopt

        :return dict: Dictionary containing all the MoniGoMani Configuration files in format
            {mgm-config: dict, mgm-config-private: dict, mgm-config-hyperopt: dict}
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
                self.logger.critical('🤷 No "{0}" filename found in the ".hurry" config file. '
                                     'Please run: mgm-hurry setup'.format(mgm_config_filename))
                sys.exit(1)

            # Full path to current config file
            mgm_config_filepath = self._get_full_path_for_config_name(hurry_config, mgm_config_filename)

            # Read config file contents
            mgm_config_files[mgm_config_filename] = self.load_config_file(mgm_config_filepath)

        return mgm_config_files

    def read_hurry_config(self) -> dict:
        """
        Read .hurry configuration dotfile and return its yaml contents as dict.

        :return dict: Dictionary containing the config section of .hurry file. None if failed.
        """
        with open('{0}/.hurry'.format(self.basedir), 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        hurry_config = config['config'] if 'config' in config else None

        return hurry_config

    def get_config_filename(self, cfg_key: str) -> str:
        """
        Transforms given cfg_key into the corresponding config filename.

        :param cfg_key: (str) The config name (key) to parse.
        :return str: The absolute path to the asked config file.
        """
        hurry_config = self.read_hurry_config()
        return self._get_full_path_for_config_name(hurry_config, cfg_key)

    def load_config_file(self, filename: str) -> dict:
        """
        Read json-file contents and return its data.

        :param filename: (str) The absolute path + filename to the json config file.
        :return dict: The json content of the file. json.load() return. None if failed.
        """
        if os.path.isfile(filename) is False:
            self.logger.error('🤷 No "{0}" file found in the "user_data" directory. '
                              'Please run: mgm-hurry setup'.format(filename))
            return None

        # Load the MoniGoMani config file as an object and parse it as a dictionary
        with open(filename, ) as file_object:
            json_data = json.load(file_object)
            return json_data

    def write_hurry_dotfile(self, config: dict = None):
        """
        Write config-array to ".hurry" config file and load its contents into config-property.
        Writes the passed config dictionary or if nothing passed, it will write default values.

        :param config: (dict, Optional) The config values to store. Defaults to None.
        """
        if config is None:
            config = {
                'config': {
                    'install_type': 'source',
                    'ft_binary': 'freqtrade',
                    'timerange': '20210501-20210616',
                    'exchange': 'binance',
                    'hyperopt': {
                        'strategy': 'MoniGoManiHyperStrategy',
                        'loss': 'MGM_WinRatioAndProfitRatioHyperOptLoss',
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

        # Protection to prevent from writing no data at all to mgm-config.
        if len(config) == 0 or 'config' not in config or 'mgm_config_names' not in config['config']:
            self.logger.error('🤯 Sorry, but looks like no configuration data would have been written, '
                              'resulting in an empty config file. I quit.')
            sys.exit(1)

        with open(self.__full_path_config, 'w+') as cfg_file:
            yaml.dump(config, cfg_file)

        self.reload()

        self.logger.info('🍺 Configuration data written to ".hurry" file')

    def cleanup_hyperopt_files(self, strategy: str = 'MoniGoManiHyperStrategy') -> bool:
        """
        Cleanup leftover strategy HyperOpt files.

        - mgm-config-hyperopt.json (applied results file)
        - {strategy}.json (intermediate results file)

        :param strategy: (str) The strategy used to find the corresponding files. Defaults to 'MoniGoManiHyperStrategy'.
        :return bool: True if one of these files is cleaned up with success. False if no file was cleaned up.
        """
        cleaned_up_cfg = False
        if strategy == 'MoniGoManiHyperStrategy':
            file_abspath = self._get_full_path_for_config_name(self.read_hurry_config(), 'mgm-config-hyperopt')
            cleaned_up_cfg = self._remove_file(file_abspath)

        # Remove the intermediate ho results file if exists
        strategy_ho_intermediate_path = '{0}/user_data/strategies/{1}.json'.format(self.basedir, strategy)
        cleaned_up_intermediate = self._remove_file(strategy_ho_intermediate_path)

        # return true if one of these is true
        return xor(bool(cleaned_up_cfg), bool(cleaned_up_intermediate))

    def _remove_file(self, fil: str) -> bool:
        if os.path.exists(fil) is False:
            return False

        self.logger.info('👉 Removing "{0}"'.format(os.path.basename(fil)))
        os.remove(fil)

        return True

    def _get_full_path_for_config_name(self, hurry_config: dict, cfg_name: str) -> str:
        """
        Parses the full path to given config file based on settings in .hurry.

        :param hurry_config (dict): The dictionary containing the hurry dotfile yaml config.
        :return abs_path: The absolute path to the asked config file.
        """
        # Full path to current config file
        mgm_config_filepath = '{0}/user_data/{1}'.format(self.basedir, hurry_config['mgm_config_names'][cfg_name])

        return mgm_config_filepath

    def __create_default_config(self):
        """
        Creates default .hurry config file with default values.
        """
        self.write_hurry_dotfile()

    def save_exchange_credentials(self, cred: dict):
        """
        Save exchange credentials to "mgm-config-private.json"

        :param cred: (dict) List containing values for [exchange,api_key,api_secret]
        """
        if len(cred) == 0:
            self.logger.warning('Did not write exchange credentials to "mgm-config-private.json" '
                                'because no data was passed.')
            return False

        try:
            with open(self.basedir + '/user_data/mgm-config-private.json', 'a+') as file:
                data = json.load(file)
        except Exception:
            data = {}

        data['exchange'] = {'name': cred['exchange'], 'key': cred['api_key'], 'secret': cred['api_secret']}

        with open(f'{self.basedir}/user_data/mgm-config-private.json', 'w+') as outfile:
            json.dump(data, outfile, indent=4)

        self.logger.info('🍺 Exchange settings written to "mgm-config-private.json"')

    def save_telegram_credentials(self, opt: dict) -> bool:
        """
        Save Telegram bot settings

        :param opt: (dict) Dictionary containing values for [enable_telegram,telegram_token,telegram_chat_id]
        :return bool: True if json data is written. False otherwise.
        """
        if len(opt) == 0:
            self.logger.warning('Did not write telegram credentials to "mgm-config-private.json" '
                                'because no data was passed.')
            return False

        with open(f'{self.basedir}/user_data/mgm-config-private.json', ) as file:
            data = json.load(file)

        data['telegram'] = {
            'enabled': opt['enable_telegram'], 'token': opt['telegram_token'], 'chat_id': opt['telegram_chat_id']
        }

        with open(f'{self.basedir}/user_data/mgm-config-private.json', 'w+') as outfile:
            json.dump(data, outfile, indent=4)

        self.logger.info('🍺 Telegram bot settings written to "mgm-config-private.json"')

        return True

    def get_preset_timerange(self, timerange: str) -> str:
        """
        Parses given timerange-string into according timerange dates

        :param timerange: (str) The timerange-string to parse [up, down, side]
        :return str: The parsed timerange string in yyyymmdd-yyyymmdd format
        """

        tr_input = timerange

        if timerange is None:
            timerange = self.config['timerange']
        if timerange == 'down':
            timerange = '20210509-20210524'
        if timerange == 'side':
            timerange = '20210518-20210610'
        if timerange == 'up':
            timerange = '20210127-20210221'

        tr_output = timerange

        self.logger.debug(f'☀️ Timerange string parsed from "{tr_input}" to "{tr_output}"')

        return timerange
