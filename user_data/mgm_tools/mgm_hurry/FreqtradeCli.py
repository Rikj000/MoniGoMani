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

import distro
import glob
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from shutil import copytree

import pygit2
from InquirerPy import prompt
from InquirerPy.validator import NumberValidator
from pygit2 import Repository, clone_repository
from yaspin import yaspin

from user_data.mgm_tools.mgm_hurry.CliColor import Color
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
        """
        Initialize the Freqtrade binary.

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
            self.cli_logger.warning(Color.yellow('🤷 No Freqtrade installation found. Please run '
                                                 '"mgm-hurry install_freqtrade" before attempting to go further!'))
            return False

        if self.freqtrade_binary is None:
            self.freqtrade_binary = self._get_freqtrade_binary_path(self.basedir, self.install_type)

        self.cli_logger.debug(f'👉 Freqtrade binary: `{self.freqtrade_binary}`')

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

    def installation_exists(self, silent: bool = False) -> bool:
        """
        Return true if all is setup correctly.

        :param silent: (bool, Optional) Silently run method (without command line output)
        :return bool: True if install_type is docker or Freqtrade is found. False otherwise.
        """
        if self.install_type is None:
            if silent is False:
                self.cli_logger.warning(Color.yellow('FreqtradeCli - installation_exists() failed. No install_type.'))
            return False

        # Well if install_type is docker, we return True because we don't verify if docker is installed
        if self.install_type == 'docker':
            if silent is False:
                self.cli_logger.debug('FreqtradeCli - installation_exists() succeeded because '
                                      'install_type is set to docker.')
            return True

        if self.freqtrade_binary is None:
            if silent is False:
                self.cli_logger.warning(Color.yellow('FreqtradeCli - installation_exists() failed. '
                                                     'No freqtrade_binary.'))
            return False

        if self.install_type == 'source':
            if silent is False:
                self.cli_logger.debug('FreqtradeCli - installation_exists() install_type is "source".')
            if os.path.exists(f'{self.basedir}/.env/bin/freqtrade'):
                return True

            if silent is False:
                self.cli_logger.warning(Color.yellow(f'FreqtradeCli - installation_exists() failed. Freqtrade binary '
                                                     f'not found in {self.basedir}/.env/bin/freqtrade.'))

        return False

    def download_setup_freqtrade(self, target_dir: str = None, branch: str = 'develop',
                                 commit: str = None, install_ui: bool = True) -> bool:
        """
        Install Freqtrade using a git clone to target_dir.

        :param target_dir: (str) Specify a target_dir to install Freqtrade. Defaults to os.getcwd().
        :param branch: (str) Checkout a specific branch. Defaults to 'develop'.
        :param commit: (str) Checkout a specific commit. Defaults to latest supported by MoniGoMani,
            but 'latest' can also be used.
        :param install_ui: (bool) Install FreqUI. Defaults to True.
        :return bool: True if setup completed without errors, else False.
        """
        if target_dir is None:
            target_dir = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dirname:
            text = '👉  Clone Freqtrade repository'
            if (commit == 'latest') or (commit is None):
                text = f'{text} on the latest commit'
            else:
                text = f'{text} and resetting to commit {commit}'
            with yaspin(text=text, color='cyan') as sp:
                repo = clone_repository(GIT_URL_FREQTRADE, temp_dirname, checkout_branch=branch)
                if (commit is not None) and (commit != 'latest'):
                    repo.reset(commit, pygit2.GIT_RESET_HARD)

                if not isinstance(repo, Repository):
                    sp.red.write('😕  Failed to clone Freqtrade repo. I quit!')
                    self.cli_logger.critical(Color.red('😕  Failed to clone Freqtrade repo. I quit!'))
                    sys.exit(1)

                sp.green.ok('✔')

            with yaspin(text='👉  Copy Freqtrade installation', color='cyan') as sp:
                self.copy_installation_files(temp_dirname, target_dir)
                sp.green.ok('✔')

            with yaspin(text='', color='cyan') as sp:
                sp.write('👉  Run Freqtrade setup')

                # Hide the spinner as the Freqtrade installer asks for user input.
                with sp.hidden():
                    result = self.run_setup_installer(target_dir=target_dir, install_ui=install_ui)

                if result is True:
                    sp.green.ok('✔ Freqtrade setup completed!')
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

        self.monigomani_cli.fix_git_object_permissions(temp_dir_filepath=temp_dirname)
        copytree(temp_dirname, target_dir, dirs_exist_ok=True)

        if not os.path.isfile(f'{target_dir}/monigomani/setup.exp'):
            self.cli_logger.error(Color.red('🤷 No "setup.exp" found, back to the MoniGoMani installation docs it is!'))
            sys.exit(1)

        os.chmod(f'{target_dir}/monigomani/setup.exp', 0o444)
        if os.path.islink(f'{target_dir}/setup.exp') is False:
            os.symlink(f'{target_dir}/monigomani/setup.exp', f'{target_dir}/setup.exp')

    def run_setup_installer(self, target_dir: str, install_ui: bool = True) -> bool:
        """
        Run Freqtrade setup.sh --install through setup.exp + Install Freq-UI

        :param target_dir: (str) The target directory where Freqtrade is installed.
        :param install_ui: (bool) Install FreqUI. Defaults to True.
        :return bool: True if setup ran successfully. False otherwise.
        """

        if os.path.isfile(f'{target_dir}/setup.exp'):
            command = f'expect {target_dir}/setup.exp'
            if distro.id() in ['ubuntu', 'debian']:
                command = f'echo "$USER ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$USER-temp-root; ' \
                          f'{command}; sudo rm /etc/sudoers.d/$USER-temp-root'

            # Using 'except' to automatically skip resetting the git repo, but do install all dependencies
            # Temporarily unset the VIRTUAL_ENV environment variable to keep Freqtrade from aborting the installation
            self.monigomani_cli.run_command(f'export VIRTUAL_ENV_BAK=$VIRTUAL_ENV; unset VIRTUAL_ENV; {command}; '
                                            f'export VIRTUAL_ENV=$VIRTUAL_ENV_BAK; unset VIRTUAL_ENV_BAK;')
            if install_ui is True:
                # Explicitly re-fetch the Freqtrade binary path after installation
                self.freqtrade_binary = self._get_freqtrade_binary_path(self.basedir, self.install_type)
                self.monigomani_cli.run_command(f'{self.freqtrade_binary} install-ui')
                self.cli_logger.info(Color.green('✔ Successfully installed FreqUI!'))
            return True

        self.cli_logger.error(Color.red(f'Could not run {target_dir}/setup.exp '
                                        f'for Freqtrade because the file does not exist.'))

        return False

    def download_static_pairlist(self, stake_currency: str = 'USDT', exchange: str = 'binance',
                                 pairlist_length: int = None, min_days_listed: int = None) -> dict:
        """
        Use Freqtrade test-pairlist command to download and test valid pair whitelist.

        :param stake_currency: (str) The stake currency to find the list of. Defaults to USDT
        :param exchange: (str) The exchange to read the data from. Defaults to Binance
        :param pairlist_length (int) Amount of pairs wish to use in your pairlist
        :param min_days_listed (int) The minimal days that coin pairs need to be listed on the exchange.
            Defaults to the amount of days in between now and the start of
            the timerange in '.hurry' minus the startup_candle_count
        :return dict: The static pair whitelist as a dictionary.
        """

        if pairlist_length is None:
            length_choice = prompt(questions=[{
                'type': 'input',
                'name': 'pairlist_length',
                'message': 'How much pairs would you like in your TopVolumeStaticPairList? (1 - 200)',
                'filter': lambda val: int(val),
                'validate': NumberValidator(),
                'default': '15'
            }])
            pairlist_length = length_choice.get('pairlist_length')

        if min_days_listed is None:
            new_timerange_dict = self.monigomani_cli.calculate_timerange_start_minus_startup_candle_count()
            new_start_date = new_timerange_dict['new_start_date']
            min_days_listed = (datetime.today() - new_start_date).days

        # Update the exchange & min days listed in the pairlist download tool
        retrieve_json_path = f'{self.basedir}/user_data/mgm_tools/RetrieveTopVolumeStaticPairList.json'
        if os.path.isfile(retrieve_json_path):
            with open(retrieve_json_path, ) as retrieve_json_file:
                retrieve_json_object = json.load(retrieve_json_file)
                retrieve_json_file.close()

            with open(retrieve_json_path, 'w') as retrieve_json_file:
                retrieve_json_object['exchange']['name'] = exchange.lower()
                retrieve_json_object['pairlists'][1]['min_days_listed'] = min_days_listed
                retrieve_json_object['pairlists'][
                    len(retrieve_json_object['pairlists'])-1]['number_assets'] = pairlist_length
                json.dump(retrieve_json_object, retrieve_json_file, indent=4)
                retrieve_json_file.close()

        with tempfile.NamedTemporaryFile() as temp_file:
            self.monigomani_cli.run_command(f'{self.freqtrade_binary} test-pairlist -c {retrieve_json_path} '
                                            f'--quote {stake_currency} --print-json > {temp_file.name}')

            # Read last line from temp_file, which is the json list containing pairlists
            try:
                last_line = subprocess.check_output(['tail', '-1', temp_file.name])
                pair_whitelist = json.loads(last_line)
            except json.JSONDecodeError as e:
                self.cli_logger.critical(Color.red('Unfortunately we could generate the static pairlist.'))
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
            freqtrade_binary = f'. {basedir}/.env/bin/activate; freqtrade'

        return freqtrade_binary

    def choose_fthypt_file(self) -> str:
        """
        Interactive prompt to choose an 'strategy_<strategy-name>_<timestamp>.fthypt' file.
        :return: The chosen fthypt filename
        """
        fthypt_files = map(os.path.basename, sorted(glob.glob(f'{self.basedir}/user_data/hyperopt_results/*.fthypt'),
                                                    key=os.path.getmtime, reverse=True))
        fthypt_options = list(fthypt_files)

        if len(fthypt_options) == 0:
            self.cli_logger.warning(Color.yellow('Whoops, no HyperOpt results could be found.'))
            sys.exit(1)

        questions = [{
            'type': 'list',
            'name': 'fthypt_file',
            'message': 'Please select the HyperOpt results you want to use: ',
            'choices': fthypt_options
        }]

        answers = prompt(questions=questions)
        return answers.get('fthypt_file')

    def parse_fthypt_name(self, fthypt_name: str) -> str:
        """
        Helper method to parse the '.fthypt' filename provided/asked by the user

        :param fthypt_name: '.fthypt' filename provided by the user
        :return: fthypt_name usable for the code
        """
        if fthypt_name is True or fthypt_name.lower() == 'true':
            return self.choose_fthypt_file()
        elif os.path.isfile(f'{self.basedir}/user_data/hyperopt_results/{fthypt_name}.fthypt'):
            return f'{fthypt_name}.fthypt'
        elif os.path.isfile(f'{self.basedir}/user_data/hyperopt_results/{fthypt_name}'):
            return fthypt_name
        else:
            self.cli_logger.warning(Color.yellow('🤷 Provided fthypt file not exist, please select fthypt file:'))
            return self.choose_fthypt_file()

    def choose_backtest_results_file(self, choose_results: bool = True) -> str:
        """
        Interactive prompt to choose a 'backtest-result-<timestamp>.json' file.

        :param choose_results: (bool) If false automatically selects the last results. Defaults to true
        :return str: The chosen backtest results filename
        """
        backtest_results_path = f'{self.basedir}/user_data/backtest_results/backtest-result-*.json'
        backtest_result_files = map(os.path.basename, sorted(glob.glob(backtest_results_path),
                                                             key=os.path.getmtime, reverse=True))
        backtest_result_options = list(backtest_result_files)

        if len(backtest_result_options) == 0:
            self.cli_logger.warning(Color.yellow('Whoops, no BackTest results could be found.'))
            sys.exit(1)

        if choose_results is True:
            questions = [{
                'type': 'list',
                'name': 'backtest_result_file',
                'message': 'Please select the BackTest results you want to use: ',
                'choices': backtest_result_options
            }]

            answers = prompt(questions=questions)
            return answers.get('backtest_result_file')
        else:
            return backtest_result_options[0]
