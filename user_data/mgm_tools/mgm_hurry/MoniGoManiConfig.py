# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

# --- ↑↓ Do not remove these libs ↑↓ ---------------------------------------------------------------

"""MoniGoManiConfig is the module responsible for all MGM Config related tasks."""

# ______                     _                     _        _____  _  _
# |  ___|                   | |                   | |      /  __ \| |(_)
# | |_    _ __   ___   __ _ | |_  _ __   __ _   __| |  ___ | /  \/| | _
# |  _|  | '__| / _ \ / _` || __|| '__| / _` | / _` | / _ \| |    | || |
# | |    | |   |  __/| (_| || |_ | |   | (_| || (_| ||  __/| \__/\| || |
# \_|    |_|    \___| \__, | \__||_|    \__,_| \__,_| \___| \____/|_||_|
#                        | |
#                        |_|

import os
import yaml
import logger

# --- ↑ Do not remove these libs ↑ ---------------------------------------------------------------


class MoniGoManiConfig(object):
    """MoniGoManiConfig is responsible for all MGM Config related tasks."""

    __config: dict
    __basedir: str
    __full_path_config: str
    __mgm_logger: logger

    def __init__(self, basedir: str, cli_logger: logger):
        self.__basedir = basedir
        self.__mgm_logger = cli_logger

        self.__full_path_config = '{0}/.hurry'.format(self.__basedir)

        # if .hurry file exists
        if self.valid_config_file_present():
            # yes: read and load config
            self.config = self.__read_config()
        else:
            # no: create basic config + file
            self.config = self.__create_default_config()

        self.__reload()

    def valid_config_file_present(self) -> bool:
        """Check if the .hurry config file exists on disk."""
        if not os.path.isdir(self.__full_path_config) is True:
            self.__mgm_logger.warning(
                'Could not find .hurry config file at {0}'.format(self.__full_path_config)
            )
            return False

        with open(self.__full_path_config, 'r') as yml_file:
            config = yaml.full_load(yml_file) or {}

        # Check if all required config keys
        # are present in config file
        for key in ['exchange', 'install_type', 'timerange']:
            if not config['config'][key]:
                return False

        return True

    @property
    def config(self) -> dict:
        return self.config

    @config.setter
    def config(self, data: dict):
        self.__config = data

    def __reload(self) -> bool:
        """ Reloads config file and stores in property of this object.

        Returns:
            bool: True if config is read, False if config could not be read.
        """
        if not self.valid_config_file_present() is True:
            self.__mgm_logger.error('Failed to reload config. No valid config file present.')
            return False

        self.config = self.__read_config()

        return True

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
        self.__write_config(None)

    def __write_config(self, config: dict = None):
        """ Write config-array to ".hurry" config file and load its contents into config-property.

        Writes the passed config dictionary or if nothing passed, it will write default values.

        :param config: (dict, Optional) The config values to store. Defaults to None.
        """
        if config is None:
            config = {
                'config': {
                    'install_type': 'docker',
                    'timerange': '20210501-20210616',
                    'exchange': 'binance',
                    'hyperopt': {
                        'strategy': 'MoniGoManiHyperStrategy',
                        'loss': 'WinRatioAndProfitRatioLoss',
                        'spaces': 'buy sell',
                        'quote': 'USDT',
                        'epochs': 1000
                    }
                }
            }

        with open(self.__full_path_config, 'w+') as file:
            yaml.dump(config, file)

        self.__reload()

        self.__mgm_logger.info('🍺 Configuration data written to ".hurry" file')
