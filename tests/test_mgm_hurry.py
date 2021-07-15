import sys
sys.path.append(".")
sys.path.append("..")

from user_data.mgm_tools.mgm_hurry.freqtrade_cli import FreqtradeCli

def test_initialisation_without_logger():
    fc = FreqtradeCli('.', None)
    assert isinstance(fc, FreqtradeCli)

def test_initialisation_with_logger():
    '''
    Todo:
        - Mock logger object
    '''
    from user_data.mgm_tools.mgm_hurry.LeetLogger import get_logger
    logger = get_logger()

    fc = FreqtradeCli('.', logger)
    assert isinstance(fc, FreqtradeCli)

def test_initialisation_with_logger():
    '''
    Checks if instantiation succeeds without freqtrade installation

    Todo:
        - Mock logger object
        - Probably mock freqtrade installation
    '''
    from user_data.mgm_tools.mgm_hurry.LeetLogger import get_logger
    logger = get_logger()

    fc = FreqtradeCli('.', logger)
    assert isinstance(fc, FreqtradeCli)
