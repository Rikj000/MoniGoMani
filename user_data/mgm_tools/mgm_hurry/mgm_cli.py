import logging
import os
import shutil

class MgmCli:
    '''
    MgmCli is responsible for all MGM related tasks.
    '''

    def __init__(self, basedir, logger: logging):
        self.__basedir = basedir
        self.__logger = logger

    def _lets_log(self) -> bool:
        return type(self.__logger) is logging

    def installation_exists(self) -> bool:
        '''
        Checks if the MGM Hyper Strategy installation exists

        Returns:
            success (bool)
        '''
        if os.path.exists(f"{self.__basedir}/user_data/mgm-config.json") is False:
            self._lets_log() and self.__logger.warning('🤷‍♂️ No MGM installation found.')
            return False

        if os.path.exists(f"{self.__basedir}/user_data/strategies/MoniGoManiHyperStrategy.py") is False:
            self._lets_log() and self.__logger.warning('🤷‍♂️ No MGM Hyper Strategy installation found.')
            return False

        self._lets_log() and self.__logger.debug('👉 MGM Hyper Strategy and configuration found √')

        return True

    def create_config_files(self, target_dir: str) -> bool:
        '''
        Copy example files as def files.

        Args:
            target_dir (string): The target dir where the mgm-config.example.json exists.

        Returns:
            success (bool): True if files are created, false if something failed.

        Todo:
            * Check if the example files exist
        '''
        if os.path.exists(f'{target_dir}/user_data/mgm-config.json') is False:
            shutil.copyfile(
                f'{target_dir}/user_data/mgm-config.example.json',
                f'{target_dir}/user_data/mgm-config.json')

        if os.path.exists(
                f'{target_dir}/user_data/mgm-config-private.json') is False:
            shutil.copyfile(
                f'{target_dir}/user_data/mgm-config-private.example.json',
                f'{target_dir}/user_data/mgm-config-private.json')

        self._lets_log() and self.logger.info('👉 MGM config files prepared')

        return True
