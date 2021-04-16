# --- Do not remove these libs ---
import argparse
import json
import sys
# --------------------------------

# Total Overall Signal Importance Calculator for MoniGoMani v0.9.0
# ----------------------------------------------------------------
# Paste the results from your HyperOpt over below `buy_params` & `sell_params` arrays
# Then execute: `python ./user_data/Total-Overall-Signal-Importance-Calculator.py -sc BTC` from your favorite
# terminal / CLI to calculate the overall importance of the signals being used.
# The higher the score of a signal the better

########################################################################################################################
#                                  START OF HYPEROPT BUY/SELL RESULTS COPY-PASTE SECTION                               #
########################################################################################################################


# Buy hyperspace params:
buy_params = {
    'buy___trades_when_downwards': True,
    'buy___trades_when_sideways': False,
    'buy___trades_when_upwards': True,
    'buy__downwards_trend_total_signal_needed': 4,
    'buy__sideways_trend_total_signal_needed': 17,
    'buy__upwards_trend_total_signal_needed': 50,
    'buy_downwards_trend_adx_strong_up_weight': 71,
    'buy_downwards_trend_bollinger_bands_weight': 54,
    'buy_downwards_trend_ema_long_golden_cross_weight': 0,
    'buy_downwards_trend_ema_short_golden_cross_weight': 87,
    'buy_downwards_trend_macd_weight': 47,
    'buy_downwards_trend_rsi_weight': 62,
    'buy_downwards_trend_sma_long_golden_cross_weight': 56,
    'buy_downwards_trend_sma_short_golden_cross_weight': 46,
    'buy_downwards_trend_vwap_cross_weight': 44,
    'buy_sideways_trend_adx_strong_up_weight': 65,
    'buy_sideways_trend_bollinger_bands_weight': 25,
    'buy_sideways_trend_ema_long_golden_cross_weight': 74,
    'buy_sideways_trend_ema_short_golden_cross_weight': 59,
    'buy_sideways_trend_macd_weight': 64,
    'buy_sideways_trend_rsi_weight': 52,
    'buy_sideways_trend_sma_long_golden_cross_weight': 4,
    'buy_sideways_trend_sma_short_golden_cross_weight': 86,
    'buy_sideways_trend_vwap_cross_weight': 57,
    'buy_upwards_trend_adx_strong_up_weight': 13,
    'buy_upwards_trend_bollinger_bands_weight': 21,
    'buy_upwards_trend_ema_long_golden_cross_weight': 71,
    'buy_upwards_trend_ema_short_golden_cross_weight': 12,
    'buy_upwards_trend_macd_weight': 94,
    'buy_upwards_trend_rsi_weight': 24,
    'buy_upwards_trend_sma_long_golden_cross_weight': 14,
    'buy_upwards_trend_sma_short_golden_cross_weight': 26,
    'buy_upwards_trend_vwap_cross_weight': 23
}

# Sell hyperspace params:
sell_params = {
    'sell___trades_when_downwards': True,
    'sell___trades_when_sideways': True,
    'sell___trades_when_upwards': False,
    'sell___unclogger_enabled': True,
    'sell___unclogger_enabled_when_downwards': True,
    'sell___unclogger_enabled_when_sideways': True,
    'sell___unclogger_enabled_when_upwards': False,
    'sell___unclogger_minimal_losing_trades_open': 5,
    'sell___unclogger_minimal_losing_trade_duration_minutes': 70,
    'sell___unclogger_percentage_open_trades_losing': 60,
    'sell___unclogger_trend_lookback_candles_window': 10,
    'sell__downwards_trend_total_signal_needed': 87,
    'sell__sideways_trend_total_signal_needed': 22,
    'sell__upwards_trend_total_signal_needed': 89,
    'sell_downwards_trend_adx_strong_down_weight': 34,
    'sell_downwards_trend_bollinger_bands_weight': 83,
    'sell_downwards_trend_ema_long_death_cross_weight': 0,
    'sell_downwards_trend_ema_short_death_cross_weight': 42,
    'sell_downwards_trend_macd_weight': 0,
    'sell_downwards_trend_rsi_weight': 49,
    'sell_downwards_trend_sma_long_death_cross_weight': 40,
    'sell_downwards_trend_sma_short_death_cross_weight': 0,
    'sell_downwards_trend_vwap_cross_weight': 12,
    'sell_sideways_trend_adx_strong_down_weight': 45,
    'sell_sideways_trend_bollinger_bands_weight': 94,
    'sell_sideways_trend_ema_long_death_cross_weight': 8,
    'sell_sideways_trend_ema_short_death_cross_weight': 33,
    'sell_sideways_trend_macd_weight': 65,
    'sell_sideways_trend_rsi_weight': 11,
    'sell_sideways_trend_sma_long_death_cross_weight': 57,
    'sell_sideways_trend_sma_short_death_cross_weight': 23,
    'sell_sideways_trend_vwap_cross_weight': 55,
    'sell_upwards_trend_adx_strong_down_weight': 54,
    'sell_upwards_trend_bollinger_bands_weight': 0,
    'sell_upwards_trend_ema_long_death_cross_weight': 36,
    'sell_upwards_trend_ema_short_death_cross_weight': 12,
    'sell_upwards_trend_macd_weight': 90,
    'sell_upwards_trend_rsi_weight': 52,
    'sell_upwards_trend_sma_long_death_cross_weight': 97,
    'sell_upwards_trend_sma_short_death_cross_weight': 18,
    'sell_upwards_trend_vwap_cross_weight': 51
}


########################################################################################################################
#                                   END OF HYPEROPT BUY/SELL RESULTS COPY-PASTE SECTION                                #
########################################################################################################################


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


def print_spacer():
    print("--------------------------------------------------------------------")


def print_section_header(header, whitespace=True):
    if whitespace:
        print("")
    print(header)
    print_spacer()


initial_offset = 40
signal_format = '{:<35s}{:>6s}'
full_signal_format = '{:<35s}{:>6s} | {:>6s} | {:>6s} | {:>6s}'


def print_signal(signal, importance):
    print(signal_format.format(str(signal) + ":", str(round(importance, 2)) + "%"))


def print_full_signal_header():
    print(full_signal_format.format("", "avg", "down", "side", "up"))


def print_full_buy_signal(signal, importance):
    print(full_signal_format.format(str(signal) + ":",
                                    str(round(importance, 2)) + "%",
                                    str(round(buy_params["buy_downwards_trend_" + signal + "_weight"], 2)) + "%",
                                    str(round(buy_params["buy_sideways_trend_" + signal + "_weight"], 2)) + "%",
                                    str(round(buy_params["buy_upwards_trend_" + signal + "_weight"], 2)) + "%"))


def print_full_sell_signal(signal, importance):
    print(full_signal_format.format(str(signal) + ":",
                                    str(round(importance, 2)) + "%",
                                    str(round(sell_params["sell_downwards_trend_" + signal + "_weight"], 2)) + "%",
                                    str(round(sell_params["sell_sideways_trend_" + signal + "_weight"], 2)) + "%",
                                    str(round(sell_params["sell_upwards_trend_" + signal + "_weight"], 2)) + "%"))


def print_full_avg_signal(signal, importance, avg_weights):
    print(full_signal_format.format(str(signal) + ":",
                                    str(round(importance, 2)) + "%",
                                    str(round(avg_weights["avg_downwards_trend_" + signal + "_weight"], 2)) + "%",
                                    str(round(avg_weights["avg_sideways_trend_" + signal + "_weight"], 2)) + "%",
                                    str(round(avg_weights["avg_upwards_trend_" + signal + "_weight"], 2)) + "%"))


def print_fixed_buy_sell_params():
    print("(buy/sell___trades_when_downwards/sideways/upwards might still be missing!)")
    print("")
    print("# Buy hyperspace params:")
    print("buy_params = " + json.dumps(buy_params, indent=4, sort_keys=True).
          replace("\"", "\'").replace("true", "True").replace("false", "False"))
    print("")
    print("# Sell hyperspace params:")
    print("sell_params = " + json.dumps(sell_params, indent=4, sort_keys=True).
          replace("\"", "\'").replace("true","True").replace("false", "False"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sc', '--stake-currency', dest='stake_currency', type=str, required=True,
                        help='Stake currency displayed in the report (should match to what is under '
                             '"stake_currency" in your config.json)')
    parser.add_argument('-f', '--file', dest='file', type=str, default='importance.log',
                        help='Filename to save result to')
    parser.add_argument('-nf', '--no-file', dest='output_to_file', const=False, default=True, nargs='?',
                        help='Do not output to a file')
    parser.add_argument('-fm', '--fix-missing', dest='fix_missing', action="store_true",
                        help='Re-Include missing weighted buy/sell_params with 0 as their value & re-print them as '
                             'copy/paste-able results. Also keeps the tool from crashing when there are missing values')
    parser.add_argument("-pu", "--precision-used", dest="precision_used", default=1, type=lambda x: eval(x),
                        help="The precision value used during hyperopt. Can be decimal (0.2) or fraction 1/5."
                             "If you didn't change the precision set this to 1 (default value when -pu is not omitted.")
    parser.add_argument("--verbosity", help="increase output verbosity")
    args = parser.parse_args()

    trend_names = ['downwards', 'sideways', 'upwards']
    buy_indicator_names = [
        'adx_strong_up',
        'bollinger_bands',
        'ema_long_golden_cross',
        'ema_short_golden_cross',
        'macd',
        'rsi',
        'sma_long_golden_cross',
        'sma_short_golden_cross',
        'vwap_cross',
    ]

    sell_indicator_names = [
        'adx_strong_down',
        'bollinger_bands',
        'ema_long_death_cross',
        'ema_short_death_cross',
        'macd',
        'rsi',
        'sma_long_death_cross',
        'sma_short_death_cross',
        'vwap_cross',
    ]

    combined_indicator_names = {
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

    for params in [sell_params, buy_params]:
        for p in params:
            if isinstance(params[p], (int, float, complex)) and not isinstance(params[p], bool):
                params[p] /= args.precision_used

    total_overall_buy_weights = {}
    total_overall_sell_weights = {}
    total_overall_weights = {}
    avg_trend_weights = {}

    for indicator in buy_indicator_names:
        buy_weight = 0
        for trend in trend_names:
            if args.fix_missing & ("buy_" + trend + "_trend_" + indicator + "_weight" not in buy_params):
                buy_params["buy_" + trend + "_trend_" + indicator + "_weight"] = 0
            buy_weight += buy_params["buy_" + trend + "_trend_" + indicator + "_weight"]
        total_overall_buy_weights[indicator] = buy_weight / len(trend_names)
    for indicator in sell_indicator_names:
        sell_weight = 0
        for trend in trend_names:
            if args.fix_missing & ("sell_" + trend + "_trend_" + indicator + "_weight" not in sell_params):
                sell_params["sell_" + trend + "_trend_" + indicator + "_weight"] = 0
            sell_weight += sell_params["sell_" + trend + "_trend_" + indicator + "_weight"]
        total_overall_sell_weights[indicator] = sell_weight / len(trend_names)
    for combined_indicator in combined_indicator_names.keys():
        indicators = combined_indicator_names[combined_indicator]

        for trend in trend_names:
            avg_weight = (buy_params["buy_" + trend + "_trend_" + indicators[0] + "_weight"] +
                          sell_params["sell_" + trend + "_trend_" + indicators[-1] + "_weight"]) / 2
            avg_trend_weights["avg_" + trend + "_trend_" + combined_indicator + "_weight"] = avg_weight

        total_overall_weights[combined_indicator] = (total_overall_buy_weights[indicators[0]] +
                                                     total_overall_sell_weights[indicators[-1]]) / 2

    # to output our prints to a file redirect the stdout
    original_stdout = sys.stdout
    f = {}

    if args.output_to_file:
        f = open(args.file, 'w')
        sys.stdout = FileAndConsoleLogger(sys.stdout, f)

    print_section_header("Signal importance report", False)
    print(signal_format.format('Stake currency' + ":", args.stake_currency))

    print_section_header("Total Overall Signal Importance:")
    print_full_signal_header()
    for signal, importance in total_overall_weights.items():
        print_full_avg_signal(signal, importance, avg_trend_weights)

    print_section_header("Total Overall Buy Signal Importance:")
    print_full_signal_header()
    for signal, importance in total_overall_buy_weights.items():
        print_full_buy_signal(signal, importance)

    print_section_header("Total Overall Sell Signal Importance:")
    print_full_signal_header()
    for signal, importance in total_overall_sell_weights.items():
        print_full_sell_signal(signal, importance)

    if args.fix_missing or (args.precision_used != 1):
        print_section_header("Buy/Sell Hyperspace Params (Missing Zero Fixed):")
        print_fixed_buy_sell_params()

    if args.output_to_file:
        f.close()
        sys.stdout = original_stdout


if __name__ == "__main__":
    main()
