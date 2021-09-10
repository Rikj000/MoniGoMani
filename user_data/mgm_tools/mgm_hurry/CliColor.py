# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-

class Color:
    """
    Helper class to easily print colored & formatted lines
    """

    # ↓ Format lines ↓
    @staticmethod
    def bold(text: str) -> str:
        return f'\033[1m{text}\033[m'

    @staticmethod
    def underline(text: str) -> str:
        return f'\033[4m{text}\033[m'

    @staticmethod
    def title(text: str) -> str:
        spacer = '       '
        return f'💨 💨 💨\n{spacer + Color.bold(Color.underline(text))}\n{spacer}💨 💨 💨'

    # ↓ Color lines ↓
    @staticmethod
    def blue(text: str) -> str:
        return f'\033[94m{text}\033[m'

    @staticmethod
    def cyan(text: str) -> str:
        return f'\033[0;36m{text}\033[m'

    @staticmethod
    def darkcyan(text: str) -> str:
        return f'\033[36m{text}\033[m'

    @staticmethod
    def green(text: str) -> str:
        return f'\033[0;32m{text}\033[m'

    @staticmethod
    def purple(text: str) -> str:
        return f'\033[95m{text}\033[m'

    @staticmethod
    def red(text: str) -> str:
        return f'\033[0;31m{text}\033[m'

    @staticmethod
    def white(text: str) -> str:
        return f'\033[1;37m{text}\033[m'

    @staticmethod
    def yellow(text: str) -> str:
        return f'\033[1;33m{text}\033[m'
