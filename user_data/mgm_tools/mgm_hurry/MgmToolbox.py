# -*- coding: utf-8 -*-
# -* vim: syntax=python -*-
#                           _              _  _
#  _ __   __ _  _ __   ___ | |_  ___  ___ | || |__  ___ __ __
# | '  \ / _` || '  \ |___||  _|/ _ \/ _ \| || '_ \/ _ \\ \ /
# |_|_|_|\__, ||_|_|_|      \__|\___/\___/|_||_.__/\___//_\_\
#        |___/
#
import subprocess
import sys

from user_data.mgm_tools.mgm_hurry.LeetLogger import get_logger

def __exec_cmd(cmd: str) -> int:
    """
    Executes shell command and logs output as debug output.

    :param cmd: (str) The command, sir
    :return returncode: (int) The returncode of the subprocess
    """
    if cmd is None or cmd == '':
        get_logger().error(
            '🤷 Please pass a command through. Without command no objective, sir!'
        )
        sys.exit(1) # @Todo; think about a return statement instead of this destructive instruction

    return_code = 1

    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8') as process:

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break

            if output:
                print(output.strip())

        return_code = process.poll()

    return return_code
