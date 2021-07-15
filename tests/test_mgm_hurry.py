import sys
sys.path.append(".")
sys.path.append("..")

from user_data.mgm_tools.mgm_hurry.freqtrade_cli import FreqtradeCli

def test_initialisation_without_logger():
    fc = __get_instance('.', use_logger = False)
    assert isinstance(fc, FreqtradeCli)

def test_initialisation_with_logger():
    '''
    Checks if instantiation succeeds without freqtrade installation

    Todo:
        - Mock logger object
        - Probably mock freqtrade installation
    '''
    fc = __get_instance('.', use_logger = True)
    assert isinstance(fc, FreqtradeCli)

def test_set_basedir():
    fc = __get_instance('.', use_logger=True)
    assert fc.basedir == '.'

'''
Private helper methods
'''
def __get_instance(dir, use_logger = True):
    logger = None

    if use_logger is True:
        from user_data.mgm_tools.mgm_hurry.LeetLogger import get_logger
        logger = get_logger()

    fc = FreqtradeCli(dir, logger)
    return fc
