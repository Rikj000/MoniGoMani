#!/user/bin/python3
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import argparse
import json
import os
import sys
# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------


class TotalOverallSignalImportanceCalculator:
    """
    Total Overall Signal Importance Calculator for MoniGoMani v0.13.0
    -----------------------------------------------------------------
    First do 1 or 2 HyperOpt Runs and extract your results to a 'mgm-config-hyperopt.json'

    Then execute: 
    `python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py` from your favorite terminal / CLI
    to calculate the overall importance of the signals being used. The higher the score of a signal the better!
    """

    ####################################################################################################################
    #                                           START OF CONFIG NAMES SECTION                                          #
    ####################################################################################################################
    mgm_config_name = 'mgm-config.json'
    mgm_config_hyperopt_name = 'mgm-config-hyperopt.json'
    ####################################################################################################################
    #                                            END OF CONFIG NAMES SECTION                                           #
    ####################################################################################################################

    buy_params = {}
    sell_params = {}
    unclogger_params = {}


class FileAndConsoleLogger(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # If you want the output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


def initialize_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pu', '--precision-used', dest='precision_used', default=1, type=lambda x: eval(x),
                        help='Optional (Defaults to 1 when not omitted): The precision value used during hyperopt. Can '
                             'be decimal (0.2) or fraction 1/5. Mostly useful after a running a hyperopt with precision'
                             ' different from 1, used to patch the weights of the signals displayed in the report to '
                             'what we would expect them to be for comparison with other results.')
    parser.add_argument('-cf', '--create-file', dest='create_file', type=str,
                        default='./user_data/Total-Average-Signal-Importance-Report.log',
                        help='Optional (Unused by default): Save the Total-Average-Signal-Importance-Report as a .log '
                             'file with a custom filename and file output location')
    parser.add_argument('-nf', '--no-file', dest='output_to_file', const=False, default=True, nargs='?',
                        help='Optional (Defaults to True when not omitted): Do not output the '
                             'Total-Average-Signal-Importance-Report as a .log file')
    return parser


def initialize_weighted_buy_signal_names():
    return [
        'adx_strong_up',
        'bollinger_bands',
        'ema_long_golden_cross',
        'ema_short_golden_cross',
        'macd',
        'rsi',
        'sma_long_golden_cross',
        'sma_short_golden_cross',
        'vwap_cross'
    ]


def initialize_weighted_sell_signal_names():
    return [
        'adx_strong_down',
        'bollinger_bands',
        'ema_long_death_cross',
        'ema_short_death_cross',
        'macd',
        'rsi',
        'sma_long_death_cross',
        'sma_short_death_cross',
        'vwap_cross'
    ]


def initialize_combined_weighted_signal_names():
    return {
        'adx_strong_up_down': ['adx_strong_up', 'adx_strong_down'],
        'bollinger_bands': ['bollinger_bands'],
        'ema_long_golden_death_cross': ['ema_long_golden_cross', 'ema_long_death_cross'],
        'ema_short_golden_death_cross': ['ema_short_golden_cross', 'ema_short_death_cross'],
        'macd': ['macd'],
        'rsi': ['rsi'],
        'sma_long_golden_death_cross': ['sma_long_golden_cross', 'sma_long_death_cross'],
        'sma_short_golden_death_cross': ['sma_short_golden_cross', 'sma_short_death_cross'],
        'vwap_cross': ['vwap_cross']
    }


def initialize_unclogger_check_names():
    return [
        'enabled',
        'minimal_losing_trade_duration_minutes',
        'minimal_losing_trades_open',
        'open_trades_losing_percentage_needed',
        'trend_lookback_candles_window',
        'trend_lookback_candles_window_percentage_needed',
        'trend_lookback_window_uses_downwards_candles',
        'trend_lookback_window_uses_sideways_candles',
        'trend_lookback_window_uses_upwards_candles'
    ]


initial_offset = 40
header_format = '{:<17s}{:>6s}{:>14s}'
signal_format = '{:<62s}{:>6s}'
full_signal_format = '{:<35s}{:>6s} | {:>6s} | {:>6s} | {:>6s}'


def print_spacer():
    print('--------------------------------------------------------------------')


def print_bold_spacer():
    print('====================================================================')


def print_section_header(header, white_space=True, main_header=False):
    if white_space:
        print('')

    if main_header is True:
        print_bold_spacer()
        print(header_format.format('#', header, '#'))
        print_bold_spacer()
    else:
        print(header)
        print_spacer()


def print_signal(signal, importance):
    print(signal_format.format(f'{str(signal)}:', f'{str(round(importance, 2))}%'))


def print_total_signal_header():
    print(full_signal_format.format('', '', 'down', 'side', 'up'))


def print_total_buy_signal(calculator_data):
    print(full_signal_format.format('total buy signals needed', '',
                                    str(calculator_data.buy_params['buy__downwards_trend_total_signal_needed']) + '%',
                                    str(calculator_data.buy_params['buy__sideways_trend_total_signal_needed']) + '%',
                                    str(calculator_data.buy_params['buy__upwards_trend_total_signal_needed']) + '%'))


def print_total_buy_lookback(calculator_data):
    print(full_signal_format.format(
        'total buy signals lookback windows', '',
        str(calculator_data.buy_params['buy__downwards_trend_total_signal_needed_candles_lookback_window']),
        str(calculator_data.buy_params['buy__sideways_trend_total_signal_needed_candles_lookback_window']),
        str(calculator_data.buy_params['buy__upwards_trend_total_signal_needed_candles_lookback_window'])))


def print_total_sell_signal(calculator_data):
    print(full_signal_format.format('total sell signals needed', '',
                                    str(calculator_data.sell_params['sell__downwards_trend_total_signal_needed']) + '%',
                                    str(calculator_data.sell_params['sell__sideways_trend_total_signal_needed']) + '%',
                                    str(calculator_data.sell_params['sell__upwards_trend_total_signal_needed']) + '%'))


def print_total_sell_lookback(calculator_data):
    print(full_signal_format.format(
        'total sell signals lookback windows', '',
        str(calculator_data.sell_params['sell__downwards_trend_total_signal_needed_candles_lookback_window']),
        str(calculator_data.sell_params['sell__sideways_trend_total_signal_needed_candles_lookback_window']),
        str(calculator_data.sell_params['sell__upwards_trend_total_signal_needed_candles_lookback_window'])))


def print_full_signal_header():
    print(full_signal_format.format('', 'avg', 'down', 'side', 'up'))


def print_full_buy_signal(calculator_data, signal, importance):
    print(full_signal_format.format(f'{str(signal)}:', f'{str(round(importance, 2))}%',
                                    str(calculator_data.buy_params[f'buy_downwards_trend_{signal}_weight']) + '%',
                                    str(calculator_data.buy_params[f'buy_sideways_trend_{signal}_weight']) + '%',
                                    str(calculator_data.buy_params[f'buy_upwards_trend_{signal}_weight']) + '%'))


def print_full_sell_signal(calculator_data, signal, importance):
    print(full_signal_format.format(f'{str(signal)}:', f'{str(round(importance, 2))}%',
                                    str(calculator_data.sell_params[f'sell_downwards_trend_{signal}_weight']) + '%',
                                    str(calculator_data.sell_params[f'sell_sideways_trend_{signal}_weight']) + '%',
                                    str(calculator_data.sell_params[f'sell_upwards_trend_{signal}_weight']) + '%'))


def print_full_avg_signal(signal, importance, avg_weights):
    print(full_signal_format.format(f'{str(signal)}:', f'{str(round(importance, 2))}%',
                                    str(avg_weights[f'avg_downwards_trend_{signal}_weight']) + '%',
                                    str(avg_weights[f'avg_sideways_trend_{signal}_weight']) + '%',
                                    str(avg_weights[f'avg_upwards_trend_{signal}_weight']) + '%'))


def print_sell_unclogger_check(unclogger_check, value):
    print(signal_format.format(f'{unclogger_check}:', str(value).replace('.0', '')))


def print_buy_sell_params(calculator_data):
    print('')
    print('# Buy hyperspace params:')
    print('buy_params = ' + json.dumps(calculator_data.buy_params, indent=4, sort_keys=True).
          replace('\"', '\'').replace('true', 'True').replace('false', 'False').replace('.0', ''))
    print('')
    print('# Sell hyperspace params:')
    print('sell_params = ' + json.dumps(calculator_data.sell_params, indent=4, sort_keys=True).
          replace('\"', '\'').replace('true', 'True').replace('false', 'False').replace('.0', ''))


def main():
    # Initialize the Total Overall Signal Importance Calculator
    calculator_data = TotalOverallSignalImportanceCalculator
    parser = initialize_argument_parser()
    args = parser.parse_args()

    # Initialize names for spaces, trends, weighted buy/sell signals and the unclogger
    spaces = ['buy', 'sell']
    mgm_trends = ['downwards', 'sideways', 'upwards']
    weighted_buy_signal_names = initialize_weighted_buy_signal_names()
    weighted_sell_signal_names = initialize_weighted_sell_signal_names()
    combined_weighted_signal_names = initialize_combined_weighted_signal_names()
    unclogger_check_names = initialize_unclogger_check_names()

    # Initialize empty dictionaries which will contain data for the report
    total_overall_buy_weights = {}
    total_overall_sell_weights = {}
    total_overall_weights = {}
    avg_trend_weights = {}

    # Load the MoniGoMani settings
    mgm_config_path = os.getcwd() + '/user_data/' + calculator_data.mgm_config_name
    if os.path.isfile(mgm_config_path) is True:
        # Load the 'mgm-config.json' file as an object and parse it as a dictionary
        file_object = open(mgm_config_path, )
        mgm_config_json_data = json.load(file_object)
        mgm_config = mgm_config_json_data['monigomani_settings']

    else:
        sys.exit(f'TotalOverallSignalImportanceCalculator - ERROR - The main MoniGoMani configuration file '
                 f'({calculator_data.mgm_config_name}) can\'t be found at: \'{mgm_config_path}\'... Please provide the '
                 f'correct file and/or alter "mgm_config_name" in "Total-Overall-Signal-Importance-Calculator.py"')

    # If results from a previous HyperOpt Run are found then continue the next HyperOpt Run upon them
    mgm_config_hyperopt_path = os.getcwd() + '/user_data/' + calculator_data.mgm_config_hyperopt_name
    if os.path.isfile(mgm_config_hyperopt_path) is True:
        # Load the provided 'mgm-config-hyperopt.json' file as an object
        file_object = open(mgm_config_hyperopt_path, )
        # Parse it as a dictionary
        mgm_config_hyperopt_json_data = json.load(file_object)

        # Convert the 'mgm-config-hyperopt.json' file data to params needed for the calculator
        try:
            # Convert the Total Signals Needed + Their Lookback Windows + Weighted Buy & Sell Signal Data
            for space in spaces:
                indicator_names = weighted_buy_signal_names if space == 'buy' else weighted_sell_signal_names
                params = getattr(calculator_data, f'{space}_params')
                for trend in mgm_trends:
                    for indicator in indicator_names:
                        dictionary_key = f'{space}_{trend}_trend_{indicator}_weight'
                        params[dictionary_key] = mgm_config_hyperopt_json_data['params'][dictionary_key]

                    dictionary_key = f'{space}__{trend}_trend_total_signal_needed'
                    params[dictionary_key] = mgm_config_hyperopt_json_data['params'][dictionary_key]
                    dictionary_key += '_candles_lookback_window'
                    params[dictionary_key] = mgm_config_hyperopt_json_data['params'][dictionary_key]

            # Convert the Sell Unclogger Data
            for unclogger_check_name in unclogger_check_names:
                dictionary_key = f'sell___unclogger_{unclogger_check_name}'
                config_dictionary_key = f'unclogger_{unclogger_check_name}'
                if dictionary_key in mgm_config_hyperopt_json_data['params']:
                    calculator_data.unclogger_params[unclogger_check_name] = \
                        mgm_config_hyperopt_json_data['params'][dictionary_key]
                elif (config_dictionary_key in mgm_config['unclogger_spaces']) and \
                        (isinstance(mgm_config['unclogger_spaces'][config_dictionary_key], bool) is True):
                    calculator_data.unclogger_params[unclogger_check_name] = \
                        mgm_config['unclogger_spaces'][config_dictionary_key]
                else:
                    raise KeyError(dictionary_key)

        except KeyError as missing_setting:
            sys.exit(f'TotalOverallSignalImportanceCalculator - ERROR - One of the loaded MoniGoMani configuration '
                     f'files \'{mgm_config_path}\' or \'{mgm_config_hyperopt_path}\' is missing some parameters. Please'
                     f' make sure that all parameters are existing inside these files. {missing_setting} has been '
                     f'detected as missing...')

    else:
        sys.exit(f'TotalOverallSignalImportanceCalculator - ERROR - The loaded MoniGoMani configuration file '
                 f'({calculator_data.mgm_config_hyperopt_name}) can\'t be found at: \'{mgm_config_hyperopt_path}\'... '
                 f'Please provide the correct file and/or alter "mgm_config_hyperopt_name" in '
                 f'"Total-Overall-Signal-Importance-Calculator.py"')

    # Apply the precision used
    for params in [calculator_data.sell_params, calculator_data.buy_params]:
        for p in params:
            if isinstance(params[p], (int, float, complex)) and not isinstance(params[p], bool):
                params[p] /= args.precision_used

    # Calculate the total overall buy/sell weights
    for space in spaces:
        indicator_names = weighted_buy_signal_names if space == 'buy' else weighted_sell_signal_names
        params = calculator_data.buy_params if space == 'buy' else calculator_data.sell_params

        for indicator in indicator_names:
            weight = 0

            for trend in mgm_trends:
                dictionary_key = f'{space}_{trend}_trend_{indicator}_weight'
                weight += int(params[dictionary_key])

            if space == 'buy':
                total_overall_buy_weights[indicator] = weight / len(mgm_trends)
            else:
                total_overall_sell_weights[indicator] = weight / len(mgm_trends)

    # Calculate the total overall combined weights
    for combined_indicator in combined_weighted_signal_names.keys():
        indicators = combined_weighted_signal_names[combined_indicator]

        for trend in mgm_trends:
            avg_weight = (int(calculator_data.buy_params[f'buy_{trend}_trend_{indicators[0]}_weight']) +
                          int(calculator_data.sell_params[f'sell_{trend}_trend_{indicators[-1]}_weight'])) / 2
            avg_trend_weights[f'avg_{trend}_trend_{combined_indicator}_weight'] = avg_weight

        total_overall_weights[combined_indicator] = \
            (total_overall_buy_weights[indicators[0]] + total_overall_sell_weights[indicators[-1]]) / 2

    # To output our prints to a file redirect the stdout
    original_stdout = sys.stdout
    f = {}

    if args.output_to_file:
        f = open(args.create_file, 'w')
        sys.stdout = FileAndConsoleLogger(sys.stdout, f)

    # Print out the Signal Importance Report
    print_section_header('MoniGoMani - Signal Importance Report', False, True)
    print_section_header(signal_format.format('Stake currency:', mgm_config_json_data['stake_currency']))

    print_section_header('Total Signals Needed:')
    print_total_signal_header()
    print_total_buy_signal(calculator_data)
    print_total_buy_lookback(calculator_data)
    print_total_sell_signal(calculator_data)
    print_total_sell_lookback(calculator_data)

    print_section_header('Total Overall Signal Importance:')
    print_full_signal_header()
    for signal, importance in total_overall_weights.items():
        print_full_avg_signal(signal, importance, avg_trend_weights)

    print_section_header('Total Overall Buy Signal Importance:')
    print_full_signal_header()
    for signal, importance in total_overall_buy_weights.items():
        print_full_buy_signal(calculator_data, signal, importance)

    print_section_header('Total Overall Sell Signal Importance:')
    print_full_signal_header()
    for signal, importance in total_overall_sell_weights.items():
        print_full_sell_signal(calculator_data, signal, importance)

    print_section_header('Losing Open Trade Sell Unclogger:')
    for unclogger_check, value in calculator_data.unclogger_params.items():
        print_sell_unclogger_check(unclogger_check, value)

    if args.precision_used != 1:
        print_section_header('Buy/Sell Hyperspace Params:')
        print_buy_sell_params(calculator_data)

    if args.output_to_file:
        f.close()
        sys.stdout = original_stdout


if __name__ == '__main__':
    main()
