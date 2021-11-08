import getopt
import json
import os
import sys
from pathlib import Path

import rapidjson
import pandas as pd
from pandas import DataFrame, json_normalize, read_json


def ExportCsvBacktest(input_file, output_file):
    basedir = os.getcwd()

    # Fetch the latest '.json' filename from last_result
    if input_file is None or input_file == '':
        last_result_file = Path(f'{basedir}/user_data/backtest_results/.last_result.json')
        with last_result_file.open('r') as f:
            data = [rapidjson.loads(line) for line in f]
        last_rf = json_normalize(data, max_level=1)

        results_file = Path(f'{basedir}/user_data/backtest_results/{last_rf["latest_backtest"].loc[0]}')
    else:
        results_file = Path(input_file)

    run_id = results_file.name.split('.')[0]

    # Open and normalize '.json' to dataframe
    with results_file.open('r') as f:
        data = [rapidjson.loads(line) for line in f]
    backtest = json_normalize(data, max_level=0)

    # Define result dataframe columns
    results_df = DataFrame(columns=[
        'epoch', 'pair', 'stake_amount', 'amount', 'open_date', 'close_date', 'trade_duration',
        'open_rate', 'close_rate', 'profit_ratio', 'profit_abs', 'sell_reason', 'is_open'
    ])

    backtest_result = json_normalize(backtest["strategy"], max_level=1)
    trades = pd.DataFrame.from_dict(backtest_result.iloc[0,0])

    if len(trades) > 0 :
        trades = trades.drop(['fee_open','fee_close','initial_stop_loss_abs','initial_stop_loss_ratio','stop_loss_abs',
                        'stop_loss_ratio','min_rate','max_rate','buy_tag','open_timestamp','close_timestamp'], axis=1)
        trades['stake_amount'] = trades['stake_amount'].apply(lambda x: round(x, 3))
        trades['amount'] = trades['amount'].apply(lambda x: round(x, 3))
        trades['trade_duration'] = trades['trade_duration'].apply(lambda x: round(x / 3600, 2))
        trades['open_rate'] = trades['open_rate'].apply(lambda x: round(x, 3))
        trades['close_rate'] = trades['close_rate'].apply(lambda x: round(x, 3))
        trades['profit_ratio'] = trades['profit_ratio'].apply(lambda x: round(x * 100, 2))
        trades['profit_abs'] = trades['profit_abs'].apply(lambda x: round(x, 3))
        trades.insert(0, 'run_id', run_id)

        # Export result as '.csv' file for readable result
        if output_file is None or output_file == '':
            output_file = f'{basedir}/user_data/backtest_results/{run_id}_trades.csv'

        trades.to_csv(output_file, index=False, header=True, mode='w', encoding='UTF-8')

def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, 'h:i:o:', ['cfile=', 'ifile=', 'ofile='])
    except getopt.GetoptError:
        print('ExportCsvBacktest.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ExportCsvBacktest.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ('-i', '--ifile', '--input_file'):
            input_file = arg
        elif opt in ('-o', '--ofile', '--output_file'):
            output_file = arg

    ExportCsvBacktest(input_file, output_file)


if __name__ == '__main__':
    main(sys.argv[1:])
