#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
    belt.py / [MGM-Belt]
    Shorthand for To-Go commands
    
    Current compatibility: freqtrade 2021.06, MoniGoMani v0.13 (development)
    
    usage: belt.py [command] parameters, -h for help

    {download,hyperopt,backtesting,show}
                            Shorthand for Download-Data / Hyperopt / Backtesting / Hyperopt-Show

    optional arguments:
    -h, --help            show this help message and exit
    -e NUMBER, --epoch NUMBER
                            Epoch number
    -a NUMBER, --apply NUMBER
                            Export HyperOpt Run # to mgm-config-hyperopt.json
    -s NAME, --strategy NAME
                            Strategy name
    -t TIMERANGE, --timerange TIMERANGE
                            Time range   
"""

import sys
import os.path

import subprocess
import argparse

### file meta ###

__author__ = "rvasilev"
# __copyright__ = "Copyright 2021, Roman Vasilev"
# __credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley",
#    "Matthew Wakefield"]
# __license__ = "GPL"
__version__ = "0.0.0"
__maintainer__ = "rvasilev"
# __email__ = ""
__status__ = "Prototype"

### end of meta ###

### default parameters ###
__belt__ = '[MGM-Belt]'

__default_strategy = 'MoniGoManiHyperStrategy'
__default_hyperopt_loss = 'WinRatioAndProfitRatioLoss'
__default_timerange = '20210501-20210616'
__default_timeframes = '5m 30m 1h'
__default_epoch = '800'

### end of default parameters ###

mgm_user_data = './user_data/'

mgm_config_name = 'mgm-config.json'
mgm_config_private_name = 'mgm-config-private.json'
mgm_config_hyperopt_name = 'mgm-config-hyperopt.json'

belt_config_hyperopt_new_name = 'mgm-config-hyperopt.new.json'
belt_config_hyperopt_old_name = 'mgm-config-hyperopt.old.json'

FREQTRADE = 'freqtrade'
BACKTESTING = f'{FREQTRADE} backtesting'
HYPEROPT = f'{FREQTRADE} hyperopt'
HYPEROPT_SHOW = f'{HYPEROPT}-show'
DOWNLOAD = f'{FREQTRADE} download-data'
PLOT = f'{FREQTRADE} plot-profit'

COMMON_CONFIG = f'-c ./user_data/{mgm_config_name} -c ./user_data/{mgm_config_private_name}'


def parse_args():
    parser = argparse.ArgumentParser(prog="belt.py", usage='%(prog)s [command] parameters, -h for help',
                                     description=f'{__belt__} Shorthand for To-Go commands')
    parser.add_argument('command', help=f'Shorthand for Download-Data / Hyperopt / Backtesting / Hyperopt-Show / Plot',
                        choices=['download', 'hyperopt', 'backtesting', 'show', 'plot'])
    # parser.add_argument('-q', '--quote',
    #                     help=f'<Optional> Quote of the Binance pairs to retrieve (example, use "BTC" to retrieve all '
    #                          f'pairs like ADA/BTC, ETH/BTC, etc..); default is USDT', required=False, default='USDT')
    parser.add_argument('-e', '--epoch', metavar='NUMBER', type=int,
                        help=f'Epoch number', default=__default_epoch, required=False)
    parser.add_argument(
        '-a', '--apply', metavar='NUMBER', help=f'Export HyperOpt Run # to {mgm_config_hyperopt_name}', choices=['1', '2'])
    # parser.add_argument(
    #     '-r', '--run', help=f'Hyperopt Run', choices=['1', '2'], default='1')
    parser.add_argument('-s', '--strategy', metavar="NAME", help=f'Strategy name',
                        default=__default_strategy, required=False)
    parser.add_argument('--timerange',
                        help=f'Time range', default=__default_timerange, required=False)
    parser.add_argument('-t', '--timeframes',
                        help=f'Time frames', default=__default_timeframes, required=False)
    parser.add_argument('--spaces',
                        help=f'Spaces', choices=['roi', 'buy', 'sell', 'stoploss', 'trailing', 'all', 'default'], default='default', nargs='+', required=False)
    parser.add_argument('--loss', help=f'Loss Function',
                        choices=[__default_hyperopt_loss, 'UncloggedWinRatioAndProfitRatioLoss'], default=__default_hyperopt_loss, required=False)
    # TODO: Should there be a "recommended default random state?"
    parser.add_argument('--state', type=int, help=f'Random State', required=False)

    args = parser.parse_args()
    return args


def download_data(args):
    print(f'{__belt__} Downloading 5m and 1h quotes for timerange {args.timerange}...')
    _cmd = f'{DOWNLOAD} {COMMON_CONFIG} --timerange {args.timerange} --timeframes {args.timeframes}'
    subprocess.run([_cmd], shell=True)


def hyperopt_show(args):
    print(f'{__belt__} Displaying HyperOpted parameters...')
    _cmd = f'{HYPEROPT_SHOW} {COMMON_CONFIG} '

    if (args.epoch):
        print(f'{__belt__} For epoch # {args.epoch}')
        _cmd += f' -n {args.epoch}'

    cmd = [_cmd]
    subprocess.run(cmd, shell=True)


def hyperopt_apply(args, tmp=False):
    print(f'{__belt__} Applying HyperOpted params from epoch # {args.epoch}...')
    cmd = []

    if (not os.path.isfile(f'./user_data/{mgm_config_hyperopt_name}')):
        print(f'{__belt__} Creating empty {mgm_config_hyperopt_name}')
        subprocess.run(
            ['echo "{}" > ./user_data/mgm-config-hyperopt.json'], shell=True)
        
    # TODO: Epoch should not be default 800 here
    _cmd = f"{HYPEROPT_SHOW} -n {args.epoch} {COMMON_CONFIG} --no-header --print-json | tail -n 1 | jq '.' > "

    if (tmp is True):
        # print('[HyperOpt] Temporary Mode')
        _cmd += f"./tmp.json && jq -s '.[0] * .[1]' ./user_data/{mgm_config_hyperopt_name} ./tmp.json > ./user_data/{belt_config_hyperopt_new_name} && rm ./tmp.json"

    if (tmp is False):
        print(
            f'{__belt__} Applying HyperOpted params from Run {args.apply} and epoch # {args.epoch}..')
        if (args.apply == '1'):

            _cmd += f"./user_data/{mgm_config_hyperopt_name}"
            # cmd = [_cmd]

        if (args.apply == '2'):
            _cmd += f"./tmp.json && jq -s '.[0] * .[1]' ./user_data/{mgm_config_hyperopt_name} ./tmp.json > ./tmp2.json && rm ./tmp.json ./user_data/{mgm_config_hyperopt_name} && mv ./tmp2.json ./user_data/{mgm_config_hyperopt_name}"

    cmd.append(_cmd)

    subprocess.run(cmd, shell=True)


def hyperopt(args):
    print(f'{__belt__} Starting HyperOpt for {args.epoch} epochs')
    # print(args)

    spaces = ''

    if (args.spaces):
        spaces = ' '.join(args.spaces)

    if (args.apply):
        hyperopt_apply(args)
    else:
        _cmd = f'{HYPEROPT} -s {args.strategy} {COMMON_CONFIG} --timerange {args.timerange} -e {args.epoch} --spaces {spaces} --hyperopt-loss {args.loss} --enable-protections'
        if (('state' in args) and (args.state != None)):
            _cmd += f' --random-state {args.state}'
        cmd = [_cmd]
        subprocess.run(cmd, shell=True)


def backtesting_epoch(args):
    print(f'{__belt__} Backtesting epoch # {args.epoch}')
    # cmd = ["freqtrade", "backtesting", "-s",
    #        f'{args.strategy}', "--timerange", f'{args.timerange}']

    # this will create ./user_data/mgm-config-hyperopt.old.json and ./user_data/mgm-config-hyperopt.new.json
    hyperopt_apply(args, tmp=True)

    _cmd = f'mv ./user_data/{mgm_config_hyperopt_name} ./user_data/{belt_config_hyperopt_old_name} && '
    _cmd += f'mv ./user_data/{belt_config_hyperopt_new_name} ./user_data/{mgm_config_hyperopt_name} && '
    _cmd += f'{BACKTESTING} -s {args.strategy} {COMMON_CONFIG} --timerange {args.timerange} --enable-protections &&'
    # cmd.append(_cmd)
    _cmd += f'rm ./user_data/{mgm_config_hyperopt_name} &&'
    # cmd.append(
    _cmd += f'mv ./user_data/{belt_config_hyperopt_old_name} ./user_data/{mgm_config_hyperopt_name}'

    subprocess.run([_cmd], shell=True)


def backtesting(args):
    print(f'{__belt__} Starting Backtesting...')
    # print(args)
    # cmd = ["freqtrade", "backtesting", "-s",
    #        f'{args.strategy}', "--timerange", f'{args.timerange}']

    if (args.epoch is None):
        print(f'{__belt__} Backtesting current configuration')
        cmd = [
            f'{BACKTESTING} -s {args.strategy} {COMMON_CONFIG} --timerange {args.timerange} --enable-protections']
        subprocess.run(cmd, shell=True)
        # cmd.extend(["-c", "./user_data/mgm-config.json", "-c",
        #             "./user_data/mgm-config-private.json", "--enable-protections"])
    # "-s", "MoniGoManiHyperStrategy", "-c", "./user_data/mgm-config.json",
    # "-c", "./user_data/mgm-config-private.json", "--timerange", "20210101-20210316", "--enable-protections"]
    else:
        backtesting_epoch(args)

    # subprocess.run(cmd)


def plot(args):
    # TODO: Stub / nothing happens here now
    print(f'{__belt__} Plotting...')

    cmd = [f'{PLOT} {COMMON_CONFIG} --timerange {args.timerange} --timeframe 1h --export-filename {mgm_user_data}backtest_results/{args.timerange}.json']

    subprocess.run(cmd, shell=True)


def main():
    # Instantiate the parser
    args = parse_args()

    # if (args.command is None):
    #     print(f'{__belt__} Help')

    if ('download' in args.command):
        download_data(args)

    if ('hyperopt' in args.command):
        hyperopt(args)

    if ('backtesting' in args.command):
        backtesting(args)

    if ('show' in args.command):
        hyperopt_show(args)

    if ('plot' in args.command):
        plot(args)
    # currency = args.quote

    # resp = requests.get(url=url)
    # data = resp.json()

    # pairs_with_given_quote = \
    #     sorted(['/{}'.format(currency).join(str(d['symbol']).rsplit(currency, 1)) for d in data['symbols']
    #             if d['quoteAsset'] == currency
    #             and d['status'] == 'TRADING'
    #             and d['isSpotTradingAllowed'] is True
    #             # and d['isMarginTradingAllowed'] is True
    #             ])
    # print(json.dumps(pairs_with_given_quote, indent=4, sort_keys=True))

    # print('Quote', currency)


if __name__ == '__main__':
    main()
