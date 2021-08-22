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

import json
import os
import subprocess
import sys
import tempfile

from pygit2 import Repository, clone_repository
from yaspin import yaspin

from user_data.mgm_tools.mgm_hurry.MoniGoManiCli import MoniGoManiCli
from user_data.mgm_tools.mgm_hurry.MoniGoManiConfig import MoniGoManiConfig
from user_data.mgm_tools.mgm_hurry.MoniGoManiLogger import MoniGoManiLogger


# --- ↑ Do not remove these libs ↑ -------------------------------------------------------------------------------------

YASPIN_INSTANCE: yaspin = None  # Global scope for a reason
GIT_URL_FREQTRADE: str = 'https://github.com/freqtrade/freqtrade'


class FreqtradeCli:
    """
    FreqtradeCli is responsible for all Freqtrade (installation) related tasks.

    Attributes:
        basedir             The basedir where the monigomani install lives.
        freqtrade_binary    The abs path to the Freqtrade executable.
        cli_logger          The logger function of the MoniGoManiCli module.
        monigomani_cli      The MoniGoManiCli object.
        monigomani_config   The MoniGoManiConfig object.
        _install_type       The current install type of Freqtrade. Either 'source' or default 'docker'
    """
    basedir: str
    freqtrade_binary: str
    cli_logger: MoniGoManiLogger
    monigomani_cli: MoniGoManiCli
    monigomani_config: MoniGoManiConfig
    _install_type: str

    def __init__(self, basedir: str):
        """Initialize the Freqtrade binary.

        :param basedir: (str) The basedir to be used as our root directory.
        """
        self.basedir = basedir

        self.cli_logger = MoniGoManiLogger(self.basedir).get_logger()
        self.monigomani_config = MoniGoManiConfig(self.basedir)

        self._install_type = self.monigomani_config.get('install_type') or None
        self.freqtrade_binary = self.monigomani_config.get('ft_binary') or None

        self._init_freqtrade()

        self.monigomani_cli = MoniGoManiCli(self.basedir)

    def _init_freqtrade(self) -> bool:
        """
        Initialize self.freqtrade_binary property.

        :return bool: True if Freqtrade installation is found and property is set. False otherwise.
        """
        if self.installation_exists() is False:
            self.cli_logger.warning('🤷 No Freqtrade installation found.')
            # ToDo
            return False

        self.freqtrade_binary = self._get_freqtrade_binary_path(self.basedir, self.install_type)

        self.cli_logger.debug('👉 Freqtrade binary: `{0}`'.format(self.freqtrade_binary))

        return True

    @property
    def install_type(self) -> str:
        """
        Return property install_type.

        :return str: The install type. either source, docker or None.
        """
        return self._install_type

    @install_type.setter
    def install_type(self, p_install_type):
        if p_install_type in {'source', 'docker'}:
            self._install_type = p_install_type

    def logger(self) -> MoniGoManiLogger:
        """
        Access the internal logger.

        :return logger: (MoniGoManiLogger) Current internal logger.
        """
        return self.cli_logger

    def installation_exists(self) -> bool:
        """Return true if all is setup correctly.

        :return bool: True if install_type is docker or Freqtrade is found. False otherwise.
        """
        if self.install_type is None:
            self.cli_logger.warning('FreqtradeCli - installation_exists() failed. No install_type.')
            return False

        # Well if install_type is docker, we return True because we don't verify if docker is installed
        if self.install_type == 'docker':
            self.cli_logger.debug(
                'FreqtradeCli - installation_exists() succeeded because install_type is set to docker.')
            return True

        if self.freqtrade_binary is None:
            self.cli_logger.warning('FreqtradeCli - installation_exists() failed. No freqtrade_binary.')
            return False

        if self.install_type == 'source':
            self.cli_logger.debug('FreqtradeCli - installation_exists() install_type is "source".')
            if os.path.exists('{0}/.env/bin/freqtrade'.format(self.basedir)):
                return True

            self.cli_logger.warning('FreqtradeCli - installation_exists() failed. '
                                    'Freqtrade binary not found in {0}/.env/bin/freqtrade.'.format(self.basedir))

        return False

    def download_setup_freqtrade(self, branch: str = 'develop', target_dir: str = None) -> bool:
        """
        Install Freqtrade using a git clone to target_dir.

        :param branch: (str) Checkout a specific branch. Defaults to 'develop'.
        :param target_dir: (str) Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        :return bool: True if setup completed without errors, else False.
        """
        with tempfile.TemporaryDirectory() as temp_dirname:
            with yaspin(text='👉  Clone Freqtrade repository', color='cyan') as sp:
                repo = clone_repository(GIT_URL_FREQTRADE, temp_dirname, checkout_branch=branch)

                if not isinstance(repo, Repository):
                    sp.red.write('😕  Failed to clone Freqtrade repo. I quit!')
                    self.cli_logger.critical('😕  Failed to clone Freqtrade repo. I quit!')
                    sys.exit(1)

                sp.green.ok('✔')

            with yaspin(text='👉  Copy Freqtrade installation', color='cyan') as sp:
                self.copy_installation_files(temp_dirname, target_dir)
                sp.green.ok('✔')

            with yaspin(text='', color='cyan') as sp:
                sp.write('👉  Run Freqtrade setup')

                # Hide the spinner as the Freqtrade installer asks for user input.
                with sp.hidden():
                    result = self.run_setup_installer(target_dir)

                if result is True:
                    sp.green.ok('✔ Freqtrade setup completed')
                    return True

            sp.red.write('😕 Freqtrade setup failed')
            return False

    def copy_installation_files(self, temp_dirname: str, target_dir: str):
        """
        Copy the installation files to the target directory. Also symlink the 'setup.exp' file.

        :param temp_dirname: (str) The source directory where installation files exist.
        :param target_dir: (str) The target directory where the installation files should be copied to.
        """
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        self.monigomani_cli.run_command('cp -rT {0} {1}'.format(temp_dirname, target_dir))

        if not os.path.isfile(f'{target_dir}/monigomani/setup.exp'):
            self.cli_logger.error('🤷 No "setup.exp" found, back to the MoniGoMani installation docs it is!')
            sys.exit(1)
        os.symlink(f'{target_dir}/monigomani/setup.exp', f'{target_dir}/setup.exp')

    def run_setup_installer(self, target_dir: str) -> bool:
        """
        Run Freqtrade setup.sh --install through setup.exp

        :param target_dir: (str) The target directory where Freqtrade is installed.
        :return bool: True if setup ran successfully. False otherwise.
        """

        if os.path.isfile('{0}/setup.exp'.format(target_dir)):
            # Using 'except' to automatically skip resetting the git repo, but do install all dependencies
            self.monigomani_cli.run_command('{0}/setup.exp'.format(target_dir))
            return True

        self.cli_logger.error('Could not run {0}/setup.exp for Freqtrade because the file does not exist.'
                              .format(target_dir))

        return False

    def download_static_pairlist(self, stake_currency: str, exchange: str) -> dict:
        """
        Use Freqtrade test-pairlist command to download and test valid pair whitelist.

        :param stake_currency: (str) The stake currency to find the list of. Eg. BTC
        :param exchange: (str) The exchange to read the data from. Eg. Binance
        :return dict: The static pair whitelist as a dictionary.
        """
        with tempfile.NamedTemporaryFile() as temp_file:
            self.monigomani_cli.run_command(
                ('source ./.env/bin/activate; '
                 'freqtrade test-pairlist -c {0}/user_data/mgm_tools/{1}-Retrieve-Top-Volume-StaticPairList.json '
                 '--quote {2} --print-json > {3}'
                 .format(self.basedir, exchange.title(), stake_currency, temp_file.name)))

            # Read last line from temp_file, which is the json list containing pairlists
            try:
                last_line = subprocess.check_output(['tail', '-1', temp_file.name])
                pair_whitelist = json.loads(last_line)
            except json.JSONDecodeError as e:
                self.cli_logger.critical('Unfortunately we could generate the static pairlist.')
                self.cli_logger.debug(e)
                return False

            return pair_whitelist

    @staticmethod
    def _get_freqtrade_binary_path(basedir: str, install_type: str):
        """
        Determine the Freqtrade binary path based on install_type.

        :param basedir: (str) Basedir is used in case of source installation
        :param install_type: (str) Either docker or source.
        :return str: Command to run Freqtrade. Defaults to docker.
        """
        freqtrade_binary = 'docker-compose run --rm freqtrade'

        if install_type == 'source':
            freqtrade_binary = 'source {0}/.env/bin/activate; freqtrade'.format(basedir)

        return freqtrade_binary
