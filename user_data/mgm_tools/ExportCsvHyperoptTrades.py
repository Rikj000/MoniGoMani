import getopt
import json
import os
import sys
from pathlib import Path

import rapidjson
from pandas import DataFrame, json_normalize


def ExportCsvHyperoptTrades(config_file, input_file, output_file, epoch_n):
    # Load the 'mgm-config' file as an object and parse it as a dictionary
    basedir = os.getcwd()

    # Fetch the latest '.fthypt' filename from last_result
    if input_file is None or input_file == '':
        last_result_file = Path(f'{basedir}/user_data/hyperopt_results/.last_result.json')
        with last_result_file.open('r') as f:
            data = [rapidjson.loads(line) for line in f]
        last_rf = json_normalize(data, max_level=1)

        results_file = Path(f'{basedir}/user_data/hyperopt_results/{last_rf["latest_hyperopt"].loc[0]}')
    else:
        results_file = Path(input_file)

    run_id = results_file.name.split('.')[0]

    # Open '.fthypt' file and normalize '.json' to dataframe
    with results_file.open('r') as f:
        data = [rapidjson.loads(line) for line in f]
    hyperopt_results = json_normalize(data, max_level=2)

    #Filter results
    if epoch_n != 0 :
        #Filter choozen epoch only
        hyperopt_results = hyperopt_results.loc[hyperopt_results['current_epoch'] == epoch_n]
    else :
        # Filter out epochs without profit
        hyperopt_results = hyperopt_results.loc[hyperopt_results['total_profit'] > 0]

    # Define result dataframe columns
    list_of_colums = ['epoch', 'pair', 'stake_amount', 'amount', 'open_date', 'close_date', 'trade_duration',
                      'open_rate', 'close_rate', 'profit_ratio', 'profit_abs', 'sell_reason', 'is_open']
    results_df = DataFrame(columns=list_of_colums)

    # Populate results df with selected values + rearrange format
    for idx, row in hyperopt_results.iterrows():
        trades = json_normalize(row['results_metrics.trades'], max_level=1)
        trades["epoch"] = row["current_epoch"]
        results_df = results_df.append(trades)

    if len(results_df) > 0 :
        results_df = results_df.loc[:, list_of_colums]
        results_df['stake_amount'] = results_df['stake_amount'].apply(lambda x: round(x, 3))
        results_df['amount'] = results_df['amount'].apply(lambda x: round(x, 3))
        results_df['trade_duration'] = results_df['trade_duration'].apply(lambda x: round(x / 3600, 2))
        results_df['open_rate'] = results_df['open_rate'].apply(lambda x: round(x, 3))
        results_df['close_rate'] = results_df['close_rate'].apply(lambda x: round(x, 3))
        results_df['profit_ratio'] = results_df['profit_ratio'].apply(lambda x: round(x * 100, 2))
        results_df['profit_abs'] = results_df['profit_abs'].apply(lambda x: round(x, 3))
        results_df.insert(0, 'run_id', run_id)

        # Export result as '.csv' file for readable result
        if output_file is None or output_file == '':
            output_file = f'{basedir}/user_data/csv_results/{run_id}_trades.csv'

        results_df.to_csv(output_file, index=False, header=True, mode='w', encoding='UTF-8')

def main(argv):
    input_file = ''
    output_file = ''
    config_file = f'{os.getcwd()}/user_data/mgm-config.json'
    epoch = 0
    try:
        opts, args = getopt.getopt(argv, 'hc:i:o:n:', ['cfile=', 'ifile=', 'ofile='])
    except getopt.GetoptError:
        print('ExportCsvHyperoptTrades.py -c <mgm_config_file> -i <input_file> -o <output_file> -n <epoch>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ExportCsvHyperoptTrades.py -c <mgm_config_file> -i <input_file> -o <output_file> -n <epoch>')
            sys.exit()
        elif opt in ('-c', '--cfile', '--config_file'):
            config_file = arg
        elif opt in ('-i', '--ifile', '--input_file'):
            input_file = arg
        elif opt in ('-o', '--ofile', '--output_file'):
            output_file = arg
        elif opt in ('-n'):
            epoch = int(arg)

    ExportCsvHyperoptTrades(config_file, input_file, output_file, epoch)


if __name__ == '__main__':
    main(sys.argv[1:])
