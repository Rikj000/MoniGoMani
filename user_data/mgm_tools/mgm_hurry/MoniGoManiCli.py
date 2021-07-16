# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import os
import shutil
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

    def create_config_files(self, target_dir: str):
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
