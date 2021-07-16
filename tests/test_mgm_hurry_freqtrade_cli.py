import sys
sys.path.append(".")
sys.path.append("..")

from user_data.mgm_tools.mgm_hurry.freqtrade_cli import FreqtradeCli

def test_initialisation_without_logger():
    fc = __get_instance('.', use_logger = False)
    assert isinstance(fc, FreqtradeCli)

def test_initialisation_with_logger():
    fc = __get_instance('.', use_logger = True)
    assert isinstance(fc, FreqtradeCli)

def test_set_basedir():
    fc = __get_instance('.', use_logger=True)
    assert fc.basedir == '.'

def test_set_install_type_to_source():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'source'
    assert fc.install_type == 'source'

def test_set_incorrect_install_type_should_return_none():
    fc = __get_instance('.', use_logger=True)
    fc.install_type = 'foobar'
    assert fc.install_type is None

def test_set_freqtrade_binary():
    fc = __get_instance('.', use_logger=True)
    fc.freqtrade_binary = 'unknown'
    assert fc.freqtrade_binary == 'unknown'

def test_installation_exists_should_return_bool():
    fc = __get_instance('.', use_logger=True)
    # without installation type
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

'''
Private helper methods
'''
def __get_instance(dir, use_logger = True):
    '''
    Todo:
        - Mock logger object
        - Probably mock freqtrade installation
    '''
    logger = None

    if use_logger is True:
        from user_data.mgm_tools.mgm_hurry.leet_logger import get_logger
        logger = get_logger()

    fc = FreqtradeCli(dir, logger)
    return fc
