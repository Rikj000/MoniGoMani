import getopt
import json
import os
import sys
from pathlib import Path

import rapidjson
from pandas import DataFrame, json_normalize


def ExportCsvTrades(config_file, input_file, output_file, epoch_n):
    # Load the 'mgm-config' file as an object and parse it as a dictionary

    basedir = os.getcwd()

    mgm_config = {}
    if os.path.isfile(config_file) is True:
        file_object = open(config_file, )
        json_data = json.load(file_object)
        mgm_config = json_data['monigomani_settings']

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
    epochs = json_normalize(data, max_level=2)

    #Filter results
    if epoch_n != 0 :
        #Filter choozen epoch only
        epochs = epochs.loc[epochs['current_epoch'] == epoch_n]
    else :
        # Filter out epochs without profit
        epochs = epochs.loc[epochs['total_profit'] > 0]

    # Define result dataframe columns
    results_df = DataFrame(columns=[
        'epoch', 'pair', 'stake_amount', 'amount', 'open_date', 'close_date', 'trade_duration',
        'open_rate', 'close_rate', 'profit_ratio', 'profit_abs', 'sell_reason', 'is_open'
    ])

    # Populate results df with selected values + rearrange format
    trades = DataFrame()
    for idx, row in epochs.iterrows():
        trades = json_normalize(row['results_metrics.trades'], max_level=1)
        trades["epoch"] = row["current_epoch"]
        results_df = results_df.append(trades)

    if len(results_df) > 0 :
        results_df = results_df.drop(['fee_open','fee_close','initial_stop_loss_abs','initial_stop_loss_ratio','stop_loss_abs',
                        'stop_loss_ratio','min_rate','max_rate','buy_tag','open_timestamp','close_timestamp'], axis=1)
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
            output_file = f'{basedir}/user_data/hyperopt_results/{run_id}_trades.csv'

        results_df.to_csv(output_file, index=False, header=True, mode='w', encoding='UTF-8')

def main(argv):
    input_file = ''
    output_file = ''
    config_file = f'{os.getcwd()}/user_data/mgm-config.json'
    epoch = 0
    try:
        opts, args = getopt.getopt(argv, 'hc:i:o:n:', ['cfile=', 'ifile=', 'ofile='])
    except getopt.GetoptError:
        print('ExportCsvTrades.py -c <mgm_config_file> -i <input_file> -o <output_file> -n <epoch>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ExportCsvTrades.py -c <mgm_config_file> -i <input_file> -o <output_file> -n <epoch>')
            sys.exit()
        elif opt in ('-c', '--cfile', '--config_file'):
            config_file = arg
        elif opt in ('-i', '--ifile', '--input_file'):
            input_file = arg
        elif opt in ('-o', '--ofile', '--output_file'):
            output_file = arg
        elif opt in ('-n'):
            epoch = int(arg)

    ExportCsvTrades(config_file, input_file, output_file, epoch)


if __name__ == '__main__':
    main(sys.argv[1:])
