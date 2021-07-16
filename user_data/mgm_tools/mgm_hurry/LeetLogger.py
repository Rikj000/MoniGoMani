# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import logging
import coloredlogs
# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


def get_logger():
    """
    Let's Log and Roll
    """
    logging.basicConfig(format='= MGM-HURRY = %(levelname)s: %(message)s', level=logging.DEBUG)
    leetLogger = logging.getLogger(__name__)
    coloredlogs.install(level=logging.DEBUG, logger=leetLogger)

    return leetLogger
