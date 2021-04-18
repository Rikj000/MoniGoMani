**<span style="color:darkorange">WARNING:</span> MoniGoManiHyperStrategy should always be HyperOpted unless you really know what you are doing when manually allocating weights!**   
**MoniGoManiHyperStrategy found in releases already has a decent hyperopt applied to it for BTC pairs!**   
**When changing anything in one of the `config.json`'s please [re-optimize](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani)!**   


# Very Quick Start (With Docker):   
1) [Download](https://github.com/Rikj000/MoniGoMani/releases) the latest `MoniGoMani` release and unzip it somewhere. Or clone the `main` branch through git.
2) Install [Docker Desktop](https://www.docker.com/get-started)
3) Open and edit `MoniGoMani/user_data/config-private.json` & `MoniGoMani/user_data/config.json`   
([VSCodium](https://vscodium.com/) is open source and comes pre-installed with good color codes to make it easier to read `.json` or `.log` files, and many more too)   
    3.A. Follow [these 4 easy steps](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) to create your own Telegram bot and fetch it's api-token, fill `token` under `telegram` up in `config-private.json` with this. Make sure to start a conversation with your bot before continuing!   
    3.B. Say `/start` to `@userinfobot` on Telegram to get your Chat ID, fill `chat_id` under `telegram` up in `config-private.json` with this.   
    3.C. Generate a strong key/password for `jwt_secret_key` under `api_server` in `config-private.json`   
    3.D. Choose and fill in a `username` and strong `password` also under `api_server` in `config-private.json`   
4) Open a terminal window and navigate to where you put `MoniGoMani` and type on of the following:   
    - `docker-compose pull` to pull in any updates to the Image if there are any
    - `docker-compose up --build` to build and start the bot & view its log or   
    - `docker-compose up -d`  to build and start the bot in the background.   
    - `docker-compose stop` to stop the bot.   
5) When running the included compose file FreqUI is already included and can be accessed from localhost:8080, 
   login is possible using the `username` and `password` from step 3.D.

That's it you successfully set up Freqtrade, connected to Telegram, with FreqUI! Congratulations :partying_face:   
*Need a more detailed guide? Checkout the [Official Freqtrade Website](https://www.freqtrade.io/en/stable/docker_quickstart/)!*    


# Very Quick Start (From Source Code):   
1) Install [Git](https://git-scm.com/downloads)   
2) Open a terminal window and navigate to where you want to put `Freqtrade`   
3) Type `git clone https://github.com/freqtrade/freqtrade.git` to clone the Freqtrade repo    
4) Type `git checkout remotes/origin/develop` to switch to the development branch (currently needed for [Auto-HyperOptable Strategies](https://github.com/freqtrade/freqtrade/pull/4596))   
5) Type `./setup.sh -i` to install freqtrade from scratch   
6) Type `source ./.env/bin/activate` to activate your virtual environment (Needs to be done every time you open the terminal)   
7) *(Type `./setup.sh -u` to update freqtrade with git pull)*   
8) *(Type `./setup.sh -r` to hard reset the branch)*   
9) [Download](https://github.com/Rikj000/MoniGoMani/releases) the latest `MoniGoMani` release and unzip it in the `Freqtrade` folder. Or clone the `main` branch through git & copy the files over.   
10) Follow step 3 from the *Very Quick Start (With Docker)* above   

That's it you successfully set up Freqtrade natively, you can now use `MoniGoManiHyperStrategy` for hyperopting/backtesting/dry/live-running! Congratulations :partying_face:   
Check the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands) for how to use it.   


# How to Optimize MoniGoMani:   
*(These are just my ideas/theories, if you have other ideas, please test them & report your results to [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can learn and improve the workflow! Also yes the current process is lengthy but we hope to automate this where possible in further versions)*   
   
0) When you change anything in your `config.json`, `config-private.json` (besides personal info etc) or in `MoniGoManiHyperStrategy` itself you should always re-hyperopt to find the new ideal weights for your setup. This should also be done when the market changes in it's long term direction!   
1) Do some Technical Analysis on how your stake currency has been behaving in the last months/weeks & pick a logical timeframe to do your hyperopt upon (The timeframe in the go-to commands for example resembles some bullish rise/correction cycles & I believe 2021 will be a bullish year thus I think it's a good timeframe to test upon).   
2) Disable HyperOpting for the 6 `buy/sell___trades_when_downwards/sideways/upwards` settings and override them manually with some logical thinking (Noticed HyperOpt often doesn't place these locically on it's own, sometimes creating a hodlr bot + it narrows down the search spaces so hyperopt will look more where you want it too), instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)   
3) HyperOpt MoniGoManiHyperStrategy for a 1st run with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands) (Free to alter the command if you have a good idea that you want to test)   
4) Apply the HyperOpt results from your 1st run into the HyperOpt Results Copy/Paste Section of `MoniGoManiHyperStrategy.py` (Manually add the 6 `buy/sell___trades_when_downwards/sideways/upwards` settings that where overridden in step 2 since they will be excluded from HyperOpts results)
5) Further Disable HyperOpting for `buy/sell_downwards/sideways/upwards_trend_signal_weight` settings that scored lower then `10%` in the 1st HyperOpt run and override them manually to `0%` (Indication of weak signal / signal not working well during these trends with your current weight allocation setup. Also `10%` was just an idea, feel free to change this) instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)   
6) HyperOpt MoniGoManiHyperStrategy for a 2nd run with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands). This is needed since fully disabling the weak signals in step 4 altered the setup, thus "ideal" weights that take this into consideration will have to be re-calculated again with a 2nd hyperopt run. This should not cause overfitting since it's a complete fresh hyperopt run.   
7) Copy/Paste your results into the `Total-Overall-Signal-Importance-Calculator.py` & run it's [Go-To Command](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands) but include `-fm` or `--fix-missing` at the end of your command. This is needed to make them whole again since overridden weighted buy/sell_params will be missing from your HyperOpt results. (This command will re-include them with 0 as their value & re-print the fixed copy/paste-able weighted buy/sell_params)   
8) Apply the weighted `buy/sell_params` that the calculator fixed & the other result values from the 2nd hyperopt run into the HyperOpt Results Copy/Paste Section of `MoniGoManiHyperStrategy.py` (Manually add the 6 `buy/sell___trades_when_downwards/sideways/upwards` settings that where overridden in step 2 since they will be excluded from HyperOpt & Calculator results)
9) Turn off all Override settings again & you are done :smile:      


# HyperOpt Setting Overrides:
When the Parameters in the HyperOpt Space Parameters sections are altered as following examples then they can be used as overrides while hyperopting / backtesting / dry/live-running   
(only truly useful when hyperopting though!) Meaning you can use this to set individual buy_params/sell_params to a fixed value when hyperopting!   
*(MoniGoManiHyperStrategy v0.8.1 or above Required!)*   
   
**<span style="color:darkorange">WARNING:</span> Always double check that when doing a fresh hyperopt or doing a dry/live-run that all overrides are turned off!**   
**<span style="color:darkorange">WARNING:</span> Overridden buy/sell_params will be missing from the HyperOpt Results!, after hyperopting with IntParameters overridden to 0 you can use the Total Overall Signal Importance Calculator's `--fix-missing` subcommand to re-include the missing IntParameter results with 0 as their weight**   

### Override Examples:
Override `buy___trades_when_sideways` to always be **False**:
```python
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
```
Override `sell_downwards_trend_macd_weight` to always be **0**:
```python
sell_downwards_trend_macd_weight = \
    IntParameter(0, 100, default=0, space='sell', optimize=False, load=False)
```
| Function Param | Meaning |
| --- |--- |
| **default**=X      | The value used when overriding |
| **optimize**=False | Exclude from hyperopting (Make static) |
| **load**=False     | Don't load from the HyperOpt Results Copy/Paste Section |  


# Open Trade Unclogger:
When the Open Trade Unclogger is enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades.   
This `custom_stoploss` function should be able to work in tandem with `Trailing stoploss`.   

It will only unclog a losing trade when all of following checks have been full-filled:    
- Check if everything in custom_storage is up to date with all_open_trades
- Check if there are enough losing trades open for unclogging to occur
- Check if there is a losing trade open for the pair currently being ran through the MoniGoMani loop
- Check if trade has been open for X minutes (long enough to give it a recovery chance)
- Check if total open trades losing % is met
- Check if open_trade's trend changed negatively during past X candles

Please configurable/hyperoptable in the sell_params dictionary under the hyperopt results copy/paste section.
Only used when `use_custom_stoploss` & `sell_params['sell___unclogger_enabled']` are both set to `True`!


# Total Overall Signal Importance Calculator:
Paste the `buy_params` & `sell_params` results from your HyperOpt over in the `/user_data/Total-Overall-Signal-Importance-Calculator.py` file.   
Then execute: `python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc BTC` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better! And now it will also export to a `importance.log` file in the same folder for easy sharing!   
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals!   
   
- Now you must fill in `-sc` or `--stake-currency` with the one you use in `config.json` as `stake_currency` since it really matters
- Optional fill in `-f` or `--file` to submit a custom file name for the log file to be exported
- Optional fill in `-nf` or `--no-file` if you don't want a log file to be exported   
- Optional fill in `-fm` or `--fix-missing` to re-include missing weighted buy/sell_params with 0 as their value & re-print them as copy/paste-able results. Also keeps the tool from crashing when there are missing weighted values (Mostly useful after a hyperopt with overridden values)   
- Optional fill in `-pu` or `--precision-used` to re-calculate the weights to what would be expected after running hyperopt with precision enabled. Always use this after running hyperopt with precision different from 1!   


# Precision Setting:
The `precision` setting can be used to control the precision / step size used during hyperopting.   
A value **smaller than 1** will limit the search space, but may skip over good values.   
While a value **larger than 1** increases the search space, but will increase the duration of hyperopting.   
To disable `precision` / for old the work mode **just** use **1**.   

**<span style="color:darkorange">WARNING:</span> Only use a precision different from 1 during hyperopting & restore to 1 afterwards!**   
**<span style="color:darkorange">WARNING:</span> HyperOpt Results don't take precision into consideration, after hyperopting with precision use the Total Overall Signal Importance Calculator's `--precision-used` subcommand to fix the results**   

### Precision Examples:
| Precision Value | Step Size effectively used during HyperOpting |
| --- | --- |
| **1/5** or **0.2** | **5** (0, 5, 10 ...) |
| **5**   | **1/5** or **0.2** (0, 0.2, 0.4, 0.8, ...) |


# TimeFrame-Zoom:
To prevent profit exploitation during backtesting/hyperopting we backtest/hyperopt MoniGoMani which would normally use a `timeframe` (1h candles) using a smaller `backtest_timeframe` (5m candles) instead. This happens while still using an `informative_timeframe` (original 1h candles) to generate the buy/sell signals.   

With this more realistic results should be found during backtesting/hyperopting. Since the buy/sell signals will operate on the same `timeframe` that live would use (1h candles), while at the same time `backtest_timeframe` (5m or 1m candles) will simulate price movement during that `timeframe` (1h candle), providing more realistic trailing stoploss and ROI behaviour during backtesting/hyperopting.   

For more information on why this is needed please read [Backtesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)! 

**<span style="color:darkorange">WARNING:</span> Candle data for both `timeframe` as `backtest_timeframe` will have to be downloaded before you will be able to backtest/hyperopt! (Since both will be used)**   
**<span style="color:darkorange">WARNING:</span> This will be slower than backtesting at 1h and 1m is a CPU killer. But if you plan on using trailing stoploss or ROI, you probably want to know that your backtest results are not complete lies.**   
**<span style="color:darkorange">WARNING:</span> To disable TimeFrame-Zoom just use the same candles for `timeframe` & `backtest_timeframe`**   

### TimeFrame-Zoom Examples:
| Parameter | Meaning |
| --- | --- |
| **timeframe**='1h' | TimeFrame used during dry/live-runs |
| **backtest_timeframe**='5m' | Zoomed in TimeFrame used during backtesting/hyperopting |


# Go-To Commands:
For Hyper Opting *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py))*:
```properties
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all -s MoniGoManiHyperStrategy -e 1000 --timerange 20210101-20210316
```
For Back Testing *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) or legacy [MoniGoManiHyperOpted.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoManiHyperOpted.py) or legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoMani.py))*:
```properties
freqtrade backtesting -s MoniGoManiHyperStrategy -c ./user_data/config-btc.json -c ./user_data/config-private.json --timerange 20210101-20210316
```
For Total Average Signal Importance Calculation *(with the [Total-Overall-Signal-Importance-Calculator.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py))*:
```properties
python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc BTC
```

To retrieve all tradable pairs on Binance and create your own pairs.json file for 'freqtrade data-download' *(with [binance-retrieve-pair-list.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/binance-retrieve-pair-list.py))*:
```properties
python ./user_data/mgm_tools/binance-retrieve-pair-list.py -q BTC > pairs.json
freqtrade download-data --exchange binance -c ./user_data/config.json -c ./user_data/config-private.json --data-format-ohlcv hdf5 --days 740 --pairs-file user_data/pairs.json --timeframes 5m 1h
```

For Hyper Opting *(the legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoMani.py) + legacy [MoniGoManiHyperOpt.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/hyperopts/MoniGoManiHyperOpt.py))*:
```properties
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all --hyperopt MoniGoManiHyperOpt -s MoniGoMani -e 1000 --timerange 20210101-20210316
```