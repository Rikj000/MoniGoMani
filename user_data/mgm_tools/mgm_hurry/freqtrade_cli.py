# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

import os, sys

class FreqtradeCli:
    '''
    FreqtradeCli is responsible for all Freqtrade (installation) related tasks.
    '''

    def __init__(self, basedir, logger):
        '''
        Initializes the Freqtrade binary

        Returns:
            results (bool): True if freqtrade installation is found. False otherwise.
        '''
        self.basedir = basedir
        self.install_type = None
        self.freqtrade_binary = None

        if logger is None:
            return None

        self.logger = logger

        if os.path.exists(f"{self.basedir}/.env/bin/freqtrade") is False:
            logger.warning('🤷‍♂️ No Freqtrade installation found.')
            return None

        if self.install_type is None:
            return None

        if self.install_type == "source":
            self.freqtrade_binary = f"source {self.basedir}/.env/bin/activate; freqtrade"
        else:
            self.freqtrade_binary = "docker-compose run --rm freqtrade"

        logger.debug(f"👉 Freqtrade binary: `{self.freqtrade_binary}`")

        return self

    @property
    def basedir(self):
        return self.__basedir

    @basedir.setter
    def basedir(self, basedir):
        self.__basedir = basedir

    @property
    def install_type(self):
        return self.__install_type

    @install_type.setter
    def install_type(self, install_type):
        self.__install_type = install_type

    @property
    def freqtrade_binary(self):
        return self.__freqtrade_binary

    @freqtrade_binary.setter
    def freqtrade_binary(self, freqtrade_binary):
        self.__freqtrade_binary = freqtrade_binary

    def installation_exists(self) -> bool:
        if self.__install_type is None:
            return False

        if self.__freqtrade_binary is None:
            return False

        # well if install_type is docker, we return True
        # because we don't verify if docker is installed
        if self.__install_type == 'docker':
            return True

        if self.__install_type == 'source' and os.path.exists(f"{self.basedir}/.env/bin/freqtrade"):
            return True

        return False
