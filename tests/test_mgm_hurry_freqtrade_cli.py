import sys

sys.path.append('.')
sys.path.append('..')

from user_data.mgm_tools.mgm_hurry.FreqtradeCli import FreqtradeCli


'''
Test ininialisation
'''
def test_initialisation_without_logger():
    fc = __get_instance('.', use_logger=False)
    assert isinstance(fc, FreqtradeCli)


def test_initialisation_with_logger():
    fc = __get_instance('.', use_logger=True)
    assert isinstance(fc, FreqtradeCli)


'''
Test basedir related
'''
def test_set_basedir():
    fc = __get_instance('.', use_logger=True)
    assert fc.basedir == '.'


'''
Test install_type related
'''
def test_set_install_type_to_source():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'source'
    assert fc.install_type == 'source'


def test_set_incorrect_install_type_should_return_none():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'foobar'
    assert fc.install_type is None


'''
Test _get_freqtrade_binary_path
'''
def test_get_freqtrade_binary_path_unknown_install_type_should_return_docker_path():
    '''
    Case:
        - install_type = foobar
    Expected:
        - path is a string
        - path contains 'docker-compose' because foobar
            is an unknown install type
    '''
    fc = __get_instance('.', use_logger=True)
    cmd = fc._get_freqtrade_binary_path('.', 'foobar')
    assert type(cmd) is str and \
        cmd.find('docker-compose') > -1


def test_get_freqtrade_binary_path_docker():
    '''
    Case:
        - install_type = docker
    Expected:
        - path is a string
        - path contains 'docker-compose'
    '''
    fc = __get_instance('.', use_logger=True)
    cmd = fc._get_freqtrade_binary_path('.', 'docker')
    assert type(cmd) is str \
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
    fc = __get_instance('.', use_logger=True)
    cmd = fc._get_freqtrade_binary_path('.', 'source')
    assert type(cmd) is str \
        and cmd.find('freqtrade') > -1 \
        and cmd.find('.env') > -1


'''
Test installation_exists()
'''
def test_installation_exists_should_return_bool():
    '''
    Case:
        - without installation type
    '''
    fc = __get_instance('.', use_logger=True)
    assert type(fc.installation_exists()) is bool


def test_installation_exists_faulty_install_type():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'foobar'
    assert fc.installation_exists() is False


def test_installation_exists_faulty_freqtrade_binary():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'source'
    fc.freqtrade_binary = 'unknown'
    assert fc.installation_exists() is False


def test_installation_exists_install_type_docker():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'docker'
    fc.freqtrade_binary = 'unknown'
    assert fc.installation_exists() is True


"""
Private helper methods
"""
def __get_instance(dir, use_logger=True):
    """
    Todo:
        - Mock logger object
        - Probably mock freqtrade installation
    """
    logger = None

    if use_logger is True:
        from user_data.mgm_tools.mgm_hurry.LeetLogger import get_logger
        logger = get_logger()

    fc = FreqtradeCli(dir, logger)
    return fc
