
import logging
import coloredlogs

def get_logger():
    '''
    Let's Log and Roll
    '''
    logging.basicConfig(format='= MGM-HURRY = %(levelname)s: %(message)s', level=logging.DEBUG)
    leetLogger = logging.getLogger(__name__)
    coloredlogs.install(level=logging.DEBUG, logger=leetLogger)

    return leetLogger
