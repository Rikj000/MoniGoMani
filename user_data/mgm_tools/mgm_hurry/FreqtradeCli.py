# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import os
import tempfile
from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli
# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------


class FreqtradeCli:
    """
    FreqtradeCli is responsible for all Freqtrade (installation) related tasks.
    """

    def __init__(self, basedir, logger):
        """
        Initializes the Freqtrade binary

        :return results: (bool) True if freqtrade installation is found. False otherwise.
        """
        self.basedir = basedir
        self.install_type = None
        self.freqtrade_binary = None

        if logger is None:
            return None

        self.logger = logger

        self.monigomani_cli = MoniGoManiCli(self.basedir, self.logger)

        if os.path.exists(f"{self.basedir}/.env/bin/freqtrade") is False:
            logger.warning('🤷♂️ No Freqtrade installation found.')
            return None

        if self.install_type is None:
            return None

        self.freqtrade_binary = self._get_freqtrade_binary_path(self.basedir, self.install_type)

        logger.debug(f'👉 Freqtrade binary: `{self.freqtrade_binary}`')

        return self


    def _get_freqtrade_binary_path(self, basedir: str, install_type: str):
        """Determine the freqtrade binary path based on install_type.

        Args:
            basedir (str): basedir is used in case of source installation
            install_type (str): Either docker or source.

        Returns:
            str: command to run freqtrade. defaults to docker.
        """
        freqtrade_binary = 'docker-compose run --rm freqtrade'

        if install_type == 'source':
            freqtrade_binary = f'source {basedir}/.env/bin/activate; freqtrade'

        return freqtrade_binary


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
    def install_type(self, p_install_type):
        if p_install_type in ['source', 'docker']:
            self.__install_type = p_install_type
        else:
            self.__install_type = None


    @property
    def freqtrade_binary(self):
        return self.__freqtrade_binary

    @freqtrade_binary.setter
    def freqtrade_binary(self, freqtrade_binary):
        self.__freqtrade_binary = freqtrade_binary


    def installation_exists(self) -> bool:
        """
        Returns true if all is setup correctly
        source:
            And after all the freqtrade binary is found
            in the .env subdirectory.
        docker:
            Does not check for physic existence of Docker.
            But returns True.
        """
        if self.__install_type is None:
            return False

        if self.__freqtrade_binary is None:
            return False

        # Well if install_type is docker, we return True because we don't verify if docker is installed
        if self.__install_type == 'docker':
            return True

        if (self.__install_type == 'source') and os.path.exists(f'{self.basedir}/.env/bin/freqtrade'):
            return True

        return False


    def download_setup_freqtrade(self, branch: str = 'develop', target_dir: str = None):
        """
        Install Freqtrade using a git clone to target_dir.

        :param branch: (string, optional) Checkout a specific branch. Defaults to 'develop'.
        :param target_dir: (string, optional) Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        """
        with tempfile.TemporaryDirectory() as temp_dirname:
            self.monigomani_cli._exec_cmd(f'git clone -b {branch} https://github.com/freqtrade/freqtrade.git {temp_dirname}')
            self.monigomani_cli._exec_cmd(f'cp -rf {temp_dirname}/* {target_dir}')
            self.monigomani_cli._exec_cmd(f'deactivate; bash {target_dir}/setup.sh --install')
