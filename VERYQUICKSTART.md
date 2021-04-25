<p align="left">
    <a href="https://discord.gg/xFZ9bB6vEz">
        <img src="https://img.shields.io/discord/819237123009150977?label=Discord%20Server&logo=discord" alt="Join CryptoStonksShallRise on Discord">
    </a>
        <a href="https://github.com/Rikj000/MoniGoMani/releases">
        <img src="https://img.shields.io/github/downloads/Rikj000/MoniGoMani/total?label=Total%20Downloads&logo=github" alt="Total Releases Downloaded from GitHub">
    </a>
    <a href="https://github.com/Rikj000/MoniGoMani/releases/latest">
        <img src="https://img.shields.io/github/v/release/Rikj000/MoniGoMani?include_prereleases&label=Latest%20Release&logo=github" alt="Latest Official Release on GitHub">
    </a>
    <a href="https://github.com/Rikj000/MoniGoMani/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Rikj000/MoniGoMani?label=License&logo=gnu" alt="GNU General Public License">
    </a>
    <a href="https://www.freqtrade.io/en/latest/">
        <img src="https://img.shields.io/badge/Trading%20Bot-Freqtrade-blue?logo=probot&logoColor=white" alt="Freqtrade - The open source crypto day-trading bot">
    </a>
        <a href="https://www.iconomi.com/register?ref=JdFzz">
        <img src="https://img.shields.io/badge/Join-ICONOMI-blue?logo=bitcoin&logoColor=white" alt="ICONOMI - The world’s largest crypto strategy provider">
    </a>
</p>

**<span style="color:darkorange">WARNING:</span> I am in no way responsible for your live results! This strategy is still experimental and under development!**   
**<span style="color:darkorange">WARNING:</span> MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) unless you really know what you are doing when manually allocating parameters!**   
**I strongly recommended to [re-optimize](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!**   


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
*(These are just my ideas/theories, if you have other ideas, please test them & report your results to [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can learn and improve this flow! Also yes the current process is lengthy but we hope to automate this where possible in further versions)*   
   
0) When you change anything in your `config.json`, `config-private.json` (besides personal info etc) or in `MoniGoManiHyperStrategy` itself you should always re-hyperopt to find the new ideal weights for your setup. This should also be done when the market changes in it's long term direction!   
1) Do some Technical Analysis on how your stake currency has been behaving in the last months/weeks & pick a logical timeframe to do your hyperopt upon (The timeframe in the go-to commands for example resembles some bullish rise/correction cycles & I believe 2021 will be a bullish year thus I think it's a good timeframe to test upon).   
2) Setup the [Current Default MoniGoMani Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#current-default-monigomani-overrides) manually with some logical thinking. We do this to disable HyperOpting for some settings inside MGM that don't always get placed logically by HyperOpt. This helps refine the search space during HyperOpting, pushing it more towards where we want it to look. Instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)   
3) HyperOpt MoniGoManiHyperStrategy for a 1st run with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands) (Free to alter the command if you have a good idea that you want to test)   
4) Pick the `epoch` you deem best. The last one is not always the best one & be wary of profit exploitation on the last epochs! You can use `freqtrade hyperopt-show -n <EPOCH HERE>` to print out HyperOpt results found for a certain epoch.   
5) Apply the HyperOpt results from your 1st run into the HyperOpt Results Copy/Paste Section of `MoniGoManiHyperStrategy.py` (Manually add the settings back in that where overridden in step 2 since they will be excluded from HyperOpts results!)
6) Further Disable HyperOpting for `buy/sell_downwards/sideways/upwards_trend_signal_weight` settings that scored lower then `10%` in the 1st HyperOpt run and override them manually to `0%` (Indication of weak signal / signal not working well during these trends with your current weight allocation setup.   
Also `10%` was just an idea, feel free to change this) instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)   
7) Further Disable HyperOpting for `buy/sell_downwards/sideways/upwards_trend_signal_weight` settings that scored higher then `90%` in the 1st HyperOpt run and override them manually to `100%` (Indication of strong signal / signal good enough in that trend to act on it's own as a full buy/sell signal.   
Also `90%` was just an idea, feel free to change this) instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)   
8) Refine the search spaces for **all** signals still remaining in the HyperOpt space (aka normal, not overrided). We do this to push the next HyperOpt run back in the direction that we already had going during the 1st HyperOpt run. See [HyperOpt Narrowing Down Search Spaces](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-narrowing-down-search-spaces) for how to do this.   
By changing the search space for each signal remaining, from the usual (0 - 100) and setting it's to ±10 the value found for said signal during the 1st HyperOpt run.   
Example: If for `sell_sideways_trend_bollinger_bands_weight` a weight of `33` was found during the 1st HyperOpt run, then the refined search space would become as following:   
`sell_sideways_trend_bollinger_bands_weight = IntParameter(23, int(43 * precision), default=0, space='sell', optimize=True, load=True)`   
*(1000 epochs might be overkill for the 2nd run with refined search spaces, we will have to take notice where new 'best' results stop popping up since it could save us time if for example no results are ever found after epoch 250)*   
9) HyperOpt MoniGoManiHyperStrategy for a 2nd run with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands). This is needed since we have been altering the "perfectly" calculated setup, thus we have to re-balance the weights in use now. This should not cause overfitting since it's a complete fresh hyperopt run.   
10) Pick the `epoch` you deem best. The last one is not always the best one & be wary of profit exploitation on the last epochs! You can use `freqtrade hyperopt-show -n <EPOCH HERE>` to print out HyperOpt results found for a certain epoch.  
11) Copy/Paste your results into the `Total-Overall-Signal-Importance-Calculator.py` & run it's [Go-To Command](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands) but include `-fm` or `--fix-missing` at the end of your command. This is needed to make them whole again since overridden weighted buy/sell_params will be missing from your HyperOpt results. (This command will re-include them with **0** as their value & re-print the fixed copy/paste-able weighted buy/sell_params. **<span style="color:darkorange">WARNING:</span> The results will still be partial!! Since the calculator only fills in missing `Integer` values with `0`, the ones with `100%` and the `True/False` should still be added back in manually!**)   
12) Once you fixed all missing signals (those that where overridden) paste the full HyperOpt Results in the Copy/Paste Section of `MoniGoManiHyperStrategy.py` (You need to manually add the settings that where overridden since they will be excluded from HyperOpt & Calculator results)
13) Turn off all Override settings again to prevent confusion during your next HyperOpt run & you should have a nicely optimised version now! :smile:      


# HyperOpt Setting Overrides:
When the Parameters in the HyperOpt Space Parameters sections are altered as following examples then they can be used as overrides while hyperopting / backtesting / dry/live-running   
(only truly useful when hyperopting though!) Meaning you can use this to set individual buy_params/sell_params to a fixed value when hyperopting!   
*(MoniGoManiHyperStrategy v0.8.1 or above Required!)*   
   
**<span style="color:darkorange">WARNING:</span> Always double check that when doing a fresh hyperopt or doing a dry/live-run that all overrides are turned off!**   
**<span style="color:darkorange">WARNING:</span> Overridden buy/sell_params will be missing from the HyperOpt Results!, after hyperopting with IntParameters overridden to 0 you can use the Total Overall Signal Importance Calculator's `--fix-missing` subcommand to re-include the missing IntParameter results with 0 as their weight**   

### Override / Static Examples:
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

### HyperOptable / Normal Examples:
Normal usage of `buy___trades_when_sideways` making it hyperoptable:
```python
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=True, space='buy', optimize=True, load=True)
```
Normal usage of `sell_downwards_trend_macd_weight` making it hyperoptable:
```python
sell_downwards_trend_macd_weight = \
    IntParameter(0, 100, default=0, space='sell', optimize=True, load=True)
```
| Function Param | Meaning |
| --- |--- |
| **default**=X     | Not used in this case |
| **optimize**=True | Include during hyperopting (Look for "ideal" value) |
| **load**=True     | Load from the HyperOpt Results Copy/Paste Section |  

### Current Default MoniGoMani Overrides:
*(More testing should be done to find out if there are other/more overrides that would work better!)*   
Feel free to **manually** alter these if you think other values are more logical. These should be applied using the examples above.   

Following have proven to sometimes create a hodlr bot when hyperopting, which is not what we want!   
- `buy___trades_when_downwards` = `True`
- `buy___trades_when_sideways` = `False`
- `buy___trades_when_upwards` = `True`
- `sell___trades_when_downwards` = `True`
- `sell___trades_when_sideways` = `False`
- `sell___trades_when_upwards` = `True`   

We would like to use the sell unclogger
- `sell___unclogger_enabled` = `True`   

Setting these logically manually is not too hard to do and will narrow down the hyperopt space, thus resulting in less time/system resources needed to run our hyperopt (We basically push it in the direction we want by hand doing this)
- `sell___unclogger_trend_lookback_window_uses_downwards_candles` = `True`
- `sell___unclogger_trend_lookback_window_uses_sideways_candles` = `True`
- `sell___unclogger_trend_lookback_window_uses_upwards_candles` = `False`

# HyperOpt Narrowing Down Search Spaces:   
The search spaces used for HyperOptable settings in MoniGoMani can easily be tweaked/fine-tuned to try and improve upon profit being made.   
It also helps in cutting down the time needed for HyperOpting since less values will be possible. This if applied right it means we are pushing/pointing hyperopt in the right direction before it runs off doing it's crunching.   

### Narrowed Down Space Example:
Hyperopt Space for `sell___unclogger_minimal_losing_trades_open` narrowed down to only search for an ideal setup between **1 up to 5** losing trades open:
```python
sell___unclogger_minimal_losing_trades_open = \
    IntParameter(1, int(5 * precision), default=0, space='sell', optimize=True, load=True)
```

# Open Trade Unclogger:
When the Open Trade Unclogger is enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades.   
This `custom_stoploss` function should be able to work in tandem with `Trailing stoploss`.   

It will only unclog a losing trade when all of following checks have been full-filled (If a check is set to `0` it will be taken out of the equation, thus the unclogger will continue checking further without it):    
- Check if `sell___unclogger_enabled` is `True`, otherwise abort further unclogger logic.
- Check if everything in custom_storage is up to date with all_open_trades
- Check if there are enough losing trades open to fullfil `sell___unclogger_minimal_losing_trades_open`
- Check if there is a losing trade open for the pair currently being ran through the MoniGoMani loop
- Check if trade has been open for `sell___unclogger_minimal_losing_trade_duration_minutes` (long enough to give it a recovery chance)
- Check if `sell___unclogger_open_trades_losing_percentage_needed` is fulfilled
- Check if open_trade's trend changed negatively during past `sell___unclogger_trend_lookback_candles_window`:   
For unclogging to occur `sell___unclogger_trend_lookback_candles_window_percentage_needed` should be fulfilled!   
The trends used for the calculations in this check can be configured with `sell___unclogger_trend_lookback_window_uses_downwards/sideways/upwards_candles=True/False` (Recommended to set these last 3 true/false values manually using [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)).   
Each candle fulfilling a trend set to `True` will be added in the sum used to calculate the value for `sell___unclogger_trend_lookback_candles_window_percentage_needed` if it is found in the lookback window.   


Only used when `use_custom_stoploss` & `sell_params['sell___unclogger_enabled']` are both set to `True`!


# Total Overall Signal Importance Calculator:
Paste the `buy_params` & `sell_params` results from your HyperOpt over in the `/user_data/Total-Overall-Signal-Importance-Calculator.py` file.   
Then execute: `python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc BTC` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better! And now it will also export to a `importance.log` file in the same folder for easy sharing!   
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals!   

### Handy Calculator Sub Commands:
- `-h` or `--help`: Print out information about the usage of all sub commands.
- `-sc` or `--stake-currency` ***Mandatory***: Stake currency displayed in the report (Should match to what is under `stake_currency` in your `config.json`)
- `-lf` or `--load-file` ***Optional (Unused by default)***: Path to `.json` file to load HyperOpt Results from which will be used in the Calculator.   
`.json`'s should be extracted with `freqtrade hyperopt-show --best --no-header --print-json > ./user_data/config-mgm-hyperopt.json`   
**Warning** Make sure your calculator copy-paste section is complete before using this sub-command!   
- `-cf` or `--create-file` ***Optional (Unused by default)***: Save the Total-Average-Signal-Importance-Report as a `.log` file with a custom filename and file output location   
- `-nf` or `--no-file` ***Optional (Defaults to `True` when not omitted)***: Do not output the Total-Average-Signal-Importance-Report as a `.log` file
- `-fm` or `--fix-missing` ***Optional (Defaults to `True` when not omitted)***: Re-Include missing weighted buy/sell_params with **0 as their value** & re-print them as copy/paste-able results. Also keeps the tool from crashing when there are missing values. Mostly useful after a hyperopt with overridden/missing values in the hyperopt results.
- `-pu` or `--precision-used` ***Optional (Defaults to `1` when not omitted)***: The precision value used during hyperopt. Can be decimal (0.2) or fraction 1/5. Mostly useful after a running a hyperopt with precision different from 1, used to patch the weights of the signals displayed in the report to what we would expect them to be for comparison with other results.


# TimeFrame-Zoom:
To prevent profit exploitation during backtesting/hyperopting we backtest/hyperopt MoniGoMani which would normally use a `timeframe` (1h candles) using a smaller `backtest_timeframe` (5m candles) instead. This happens while still using an `informative_timeframe` (original 1h candles) to generate the buy/sell signals.   

With this more realistic results should be found during backtesting/hyperopting. Since the buy/sell signals will operate on the same `timeframe` that live would use (1h candles), while at the same time `backtest_timeframe` (5m or 1m candles) will simulate price movement during that `timeframe` (1h candle), providing more realistic trailing stoploss and ROI behaviour during backtesting/hyperopting.   

For more information on why this is needed please read [Backtesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)! 

**<span style="color:darkorange">WARNING:</span> Remove the `timeframe` line from your `config-btc.json` if it would still be there! Otherwise TimeFrame-Zoom won't work properly in the current version!**   
**<span style="color:darkorange">WARNING:</span> Candle data for both `timeframe` as `backtest_timeframe` will have to be downloaded before you will be able to backtest/hyperopt! (Since both will be used)**   
**<span style="color:darkorange">WARNING:</span> This will be slower than backtesting at 1h and 1m is a CPU killer. But if you plan on using trailing stoploss or ROI, you probably want to know that your backtest results are not complete lies.**   
**<span style="color:darkorange">WARNING:</span> To disable TimeFrame-Zoom just use the same candles for `timeframe` & `backtest_timeframe`**   

### TimeFrame-Zoom Examples:
| Parameter | Meaning |
| --- | --- |
| **timeframe**='1h' | TimeFrame used during dry/live-runs |
| **backtest_timeframe**='5m' | Zoomed in TimeFrame used during backtesting/hyperopting |


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


# PairLists:
By default MoniGoMani includes 2 pairlists in `config-btc.json`:   
- A VolumePairList: 
  - Best to use for Dry and Live Running
  - Will automatically update to the current best top volume coin pairs available
- A StaticPairList: 
  - Used for BackTesting / HyperOpting since a VolumePairList cannot be used here.
  - When [optimizing](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) MoniGoMani for actual dry/live-running (instead of testing) it's truly recommended to [download a fresh top volume StaticPairList](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#download-staticpairlists) and HyperOpt upon that (Preferably as big as possible, but beware for the warning below)!   
  This should yield much better & more realistic results during HyperOpting/BackTesting!   
  This is due to giving a better reflection of the current market and being closer to the VolumePairList used during dry/live-run's.

Switching between the PairList in use can easily be done by moving the `_` in front of the `pairlists` value inside `config-btc.json` for the pairlist you wish to disable.

**<span style="color:darkorange">WARNING:</span> The bigger the (Volume/Static)PairList in use the higher the system requirements (CPU usage, RAM usage & Time needed to HyperOpt will go up)! Switch to a smaller list if your system can't handle it!**   

### Enabled StaticPairList / Disabled VolumePairList Example:
```json
"pairlists": [{
        "method": "StaticPairList"
    }],
"_pairlists": [
    {
        "method": "VolumePairList",
```

### Download StaticPairLists   
Retrieve a current **Binance-BTC-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))* (The amount of pairs in these top volume lists can be altered by opening up `Binance-Retrieve-Top-Volume-StaticPairList.json` and changing the `number_assets` value inside to the amount of pairs you'd like in your list):
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote BTC --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-BTC-Top-Volume-StaticPairList.json
```

Retrieve a current **Binance-BTC-All-Tradable-StaticPairList.json** file *(using [Binance-Retrieve-All-Tradable-StaticPairList.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-All-Tradable-StaticPairList.py))* (Beware, very high system requirements due to a lot of BTC pairs!):
```powershell
python ./user_data/mgm_tools/Binance-Retrieve-All-Tradable-StaticPairList.py -q BTC > ./user_data/mgm_pair_lists/Binance-BTC-All-Tradable-StaticPairList.json
```

**After Downloading** the StaticPairList will be available under `./user_data/mgm_pair_lists/<<NAME_HERE>>-StaticPairList.json`, just open up the file and copy the PairList Data into your own `config-private.json` file under `pair_whitelist` section to start using it!   

Don't forget to **Download Candle Data** before HyperOpting or Backtesting (Example for last 2 years of candle data):   
```powershell
freqtrade download-data --exchange binance -c ./user_data/config-btc.json -c ./user_data/config-private.json --data-format-ohlcv hdf5 --days 740 --timeframes 5m 1h
```

# Go-To Commands:
For Hyper Opting *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py))*:
```powershell
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all -s MoniGoManiHyperStrategy -e 1000 --timerange 20210101-20210316
```
For Back Testing *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) or legacy [MoniGoManiHyperOpted.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoManiHyperOpted.py) or legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoMani.py))*:
```powershell
freqtrade backtesting -s MoniGoManiHyperStrategy -c ./user_data/config-btc.json -c ./user_data/config-private.json --timerange 20210101-20210316
```
For Total Average Signal Importance Calculation *(with the [Total-Overall-Signal-Importance-Calculator.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py))*:
```powershell
python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc BTC
```

To retrieve a current **Binance-BTC-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))*:
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote BTC --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-BTC-Top-Volume-StaticPairList.json
# Don't forget to open the downloaded '...-StaticPairList.json' and copy the PairList Data into your own 'config-private.json' file to start using it!
```

For Hyper Opting *(the legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoMani.py) + legacy [MoniGoManiHyperOpt.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/hyperopts/MoniGoManiHyperOpt.py). Please use the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) instead though since support for Legacy versions stopped!)*:
```powershell
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all --hyperopt MoniGoManiHyperOpt -s MoniGoMani -e 1000 --timerange 20210101-20210316
```

# How to share your test results properly:
Easiest way to share how your MGM setup has been doing would be by posting a screenshot in the [Discord Server](https://discord.gg/xFZ9bB6vEz) with the output of the `/status table` and `/profit` commands (Using the Telegram connection of the bot).   
   
Also one of the other most welcome things is the results from the `Total-Overall-Signal-Importance-Calculator`, but you'll have to paste your own fresh hyperopt results in it first before it can make you a nice report that can help us find better signals for MGM !:rocket:   

Of course all FreqUI / Telegram / config / HyperOpt results done on MGM **can be** useful / be learned from!
But try to **always include** a  `Total-Overall-Signal-Importance-Calculator` report or just your own MoniGoMani file with your hyperopt results applied to it!   
Since without knowing which signal weights or which on/off settings are applied we can't really truly learn much from your results!   

The epoch table being generated when hyperopting + the number of the epoch you used is also very helpful, so we can easily rule out if your test results are exploited. (See [Backtesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)!)   

# Common mistakes:

### TypeError: integer argument expected, got float   
You likely are using a `Float` value where you should be using a `Integer` value. Hopefully your error will show more information about which Parameter.   
- `Integer` = Whole number. Examples: 1, 3, 23
- `Float` = Decimal number. Examples: 1.53, 4.2, 17.12   