# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------

"""FreqtradeCli is the module responsible for all Freqtrade related tasks."""

# ______                     _                     _        _____  _  _
# |  ___|                   | |                   | |      /  __ \| |(_)
# | |_    _ __   ___   __ _ | |_  _ __   __ _   __| |  ___ | /  \/| | _
# |  _|  | '__| / _ \ / _` || __|| '__| / _` | / _` | / _ \| |    | || |
# | |    | |   |  __/| (_| || |_ | |   | (_| || (_| ||  __/| \__/\| || |
# \_|    |_|    \___| \__, | \__||_|    \__,_| \__,_| \___| \____/|_||_|
#                        | |
#                        |_|

import os
import tempfile

import logger

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli

# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------


class FreqtradeCli(object):
    """FreqtradeCli is responsible for all Freqtrade (installation) related tasks."""

    basedir: os.strerror
    freqtrade_binary: str
    cli_logger: logger
    monigomani_cli: MoniGoManiCli
    _install_type: str

    def __init__(self, basedir: str, cli_logger: logger):
        """Initialize the Freqtrade binary.

        Args:
            basedir (str): The basedir to be used as our root directory.
            cli_logger (logger): The mgmlogger object to be used to log.

        Returns:
            None if no freqtrade installation is found.
        """
        self.basedir = basedir
        self._install_type = None
        self.freqtrade_binary = None

        if cli_logger is None:
            return None

        self.cli_logger = cli_logger

        self.monigomani_cli = MoniGoManiCli(self.basedir, self.logger)

        if os.path.exists('{0}/.env/bin/freqtrade'.format(self.basedir)) is False:
            self.cli_logger.warning('🤷♂️ No Freqtrade installation found.')
            return None

        if self.install_type is None:
            return None

        self.freqtrade_binary = self._get_freqtrade_binary_path(self.basedir, self.install_type)

        self.cli_logger.debug('👉 Freqtrade binary: `{0}`'.format(self.freqtrade_binary))

    @property
    def install_type(self) -> str:
        """Return property install_type.

        Returns:
            str: the install type. either source, docker or None.
        """
        return self._install_type

    @install_type.setter
    def install_type(self, p_install_type):
        if p_install_type in {'source', 'docker'}:
            self._install_type = p_install_type

    def logger(self) -> logger:
        """Access the internal logger.

        Returns:
            logger: Current internal logger.
        """
        return self.cli_logger

    def installation_exists(self) -> bool:
        """Return true if all is setup correctly.

        Returns:
            bool: True if install_type is docker or freqtrade is found. False otherwise.

                source:
                    And after all the freqtrade binary is found
                    in the .env subdirectory.
                docker:
                    Does not check for physical existence of Docker.
                    But returns True.
        """
        if self.install_type is None:
            self.cli_logger.warning('FreqtradeCli::installation_exists() failed. No install_type.')
            return False

        if self.freqtrade_binary is None:
            self.cli_logger.warning('FreqtradeCli::installation_exists() failed. No freqtrade_binary.')
            return False

        # Well if install_type is docker, we return True because we don't verify if docker is installed
        if self.install_type == 'docker':
            self.cli_logger.info(
                'FreqtradeCli::installation_exists() succeeded because install_type is set to docker.',
            )
            return True

        if self.install_type == 'source':
            self.cli_logger.info('FreqtradeCli::installation_exists() install_type is "source".')
            if os.path.exists('{0}/.env/bin/freqtrade'.format(self.basedir)):
                return True
            else:
                self.cli_logger.error(
                    'FreqtradeCli::installation_exists() failed. freqtrade binary not found in {0}/.env/bin/freqtrade.'.format(self.basedir),
                )

        return False

    def download_setup_freqtrade(self, branch: str = 'develop', target_dir: str = None):
        """
        Install Freqtrade using a git clone to target_dir.

        Args:
            branch (str): Checkout a specific branch. Defaults to 'develop'.
            target_dir (str): Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        """
        with tempfile.TemporaryDirectory() as temp_dirname:
            self.monigomani_cli.run_command('git clone -b {0} https://github.com/freqtrade/freqtrade.git {1}'.format(branch, temp_dirname))
            self.monigomani_cli.run_command('cp -r {0}/* {1}'.format(temp_dirname, target_dir))
            self.monigomani_cli.run_command('deactivate; bash {0}/setup.sh --install'.format(target_dir))

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
            freqtrade_binary = 'source {0}/.env/bin/activate; freqtrade'.format(basedir)

        return freqtrade_binary
