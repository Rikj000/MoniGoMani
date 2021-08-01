# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.FreqtradeCli import FreqtradeCli

def test_initialisation():
    fc = __get_instance('.')
    assert isinstance(fc, FreqtradeCli)

def test_set_basedir():
    fc = __get_instance('.')
    assert fc.basedir == '.'

def test_set_install_type_to_source():
    fc = __get_instance('.')
    fc.install_type = 'source'
    assert fc.install_type == 'source'

def test_set_incorrect_install_type_should_not_return_none():
    fc = __get_instance('.')
    fc.install_type = 'foobar'
    assert fc.install_type is not None

def test_get_freqtrade_binary_path_unknown_install_type_should_return_docker_path():
    '''
    Case:
        - install_type = foobar
    Expected:
        - path is a string
        - path contains 'docker-compose' because foobar
            is an unknown install type
    '''
    fc = __get_instance('.')
    cmd = fc._get_freqtrade_binary_path('.', 'foobar')
    assert isinstance(cmd, str) and \
        cmd.find('docker-compose') > -1

def test_get_freqtrade_binary_path_docker():
    '''
    Case:
        - install_type = docker
    Expected:
        - path is a string
        - path contains 'docker-compose'
    '''
    fc = __get_instance('.')
    cmd = fc._get_freqtrade_binary_path('.', 'docker')
    assert isinstance(cmd, str) \
        and cmd.find('docker-compose') > -1

def test_get_freqtrade_binary_path_source():
    '''
    Case:
        - install_type = source
    Expected:
        - path is a string
        - path contains 'freqtrade'
        - path contains '.env'
    '''
    fc = __get_instance('.')
    cmd = fc._get_freqtrade_binary_path('.', 'source')
    assert isinstance(cmd, str) \
        and cmd.find('freqtrade') > -1 \
        and cmd.find('.env') > -1

def test_installation_exists_should_return_bool():
    '''
    Case:
        - without installation type
    '''
    fc = __get_instance('.')
    assert isinstance(fc.installation_exists(), bool)

def test_installation_exists_faulty_install_type():
    fc = __get_instance('.')
    fc.install_type = 'foobar'
    assert fc.install_type != 'foobar'

def test_installation_exists_faulty_freqtrade_binary():
    fc = __get_instance('.')
    fc.install_type = 'source'
    fc.freqtrade_binary = 'unknown'
    assert fc.installation_exists() is False

def test_installation_exists_install_type_docker():
    fc = __get_instance('.')
    fc.install_type = 'docker'
    fc.freqtrade_binary = 'unknown'
    assert fc.installation_exists() is True

def __get_instance(directory: str):
    """Create instance of freqtradecli."""
    return FreqtradeCli(directory)
