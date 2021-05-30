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

**<span style="color:darkorange">WARNING:</span> I am in no way responsible for your Live results! This strategy is still experimental and under development!**   
**<span style="color:darkorange">WARNING:</span> MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) after doing manual changes!**   
**You need to [optimize](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!**   

# Freqtrade Installation:   
This guide now assumes you have **Freqtrade** and **jq** already installed, if you haven't yet, then please see [VERYQUICKSTART_FREQTRADE.md](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART_FREQTRADE.md)

# How to Optimize MoniGoMani:   
*(These are just my ideas/theories, if you have other ideas, please test them & report your results to [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can learn and improve this flow!)*   
**<span style="color:darkorange">WARNING:</span> It's strongly advised to not do any manual alterations to an already optimized MGM setup! The recommended way to do manual alterations is by [Configuring MoniGoMani](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-configure-monigomani), and then following this optimization process to apply them!**   
   

0) Delete the previous `mgm-config-hyperopt.json` if it exists using:
    ```powershell
    rm ./user_data/mgm-config-hyperopt.json
    ```
1) Setup your `MoniGoMani` by following [How to Configure MoniGoMani](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-configure-monigomani)
2) Download a good Top Volume StaticPairList and update this in your `mgm-config.json`. Instructions for how to do this are under [PairLists](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#pairlists).
3) Do some Technical Analysis on how the global crypto market has been behaving in the last months/weeks & pick a logical timeframe to do your HyperOpt upon (The timeframe in the go-to commands for example resembles some bullish rise/correction cycles & I believe 2021 will be a bullish year thus I think it's a good timeframe to test upon).   
4) HyperOpt for a **1st HyperOpt Run** with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands) (Free to alter the command if you have a good idea that you want to test)   
    The 1st HyperOpt Run *(When no `mgm-config-hyperopt.json` exists)* is automatically ran with:   
        - The Default open search spaces ranging between the default `min_` & `max_` values provided under the `monigomani_settings` section of `mgm-config.json`   
        - The [HYPEROPT PARAMETERS CONFIGURATION SECTION](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#HYPEROPT-PARAMETER-CONFIGURATION-SECTION)   
5) **Reflect over your HyperOpt results!** The computer just tries to get certain values high (profits) and others low (losses), without a true understanding of their meaning. Because of this HyperOpt is prone to profit exploitation which would be no good when used Live. That's why you need to make yourself familiar with possible [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/). Only then you can tell which results would make sense and would be any good when used Live.   
    You can check a certain epoch in the list of best results using:
    ```powershell
    freqtrade hyperopt-show -n <epoch of choice>
    ```
6) Once you picked an `<epoch of choice>` of which you feel confident, then apply the HyperOpt results by extracting them into a new `mgm-config-hyperopt.json` using:
    ```powershell
    freqtrade hyperopt-show -n <epoch of choice> -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --no-header --print-json | tail -n 1 | jq '.' > ./user_data/mgm-config-hyperopt.json
    ```
7) Repeat Steps 4, 5 and 6 at least for a **2nd HyperOpt Run** with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands) (Free to alter the command if you have a good idea that you want to test)   
    The 2nd HyperOpt Run *(When a `mgm-config-hyperopt.json` exists)* is automatically ran with:   
        - Refined search spaces ranging between the values found during the 1st Run (Loaded from `mgm-config-hyperopt.json`) plus their `search_threshold_` and minus their `search_threshold_` values provided under the `monigomani_settings` section of `mgm-config.json` (This is done to push the next HyperOpt run back in the direction that we already had going during the 1st HyperOpt run)   
        - Weak weighted signals weeded out by overriding them to their respective `min_` value (Signals of which the found value is below their default `min_` + `search_threshold_` values provided under the `monigomani_settings` section of `mgm-config.json`)   
        - Strong weighted signals are boosted by overriding them to their respective `max_` value (Signals of which the found value is above their default `max_` - `search_threshold_` values provided under the `monigomani_settings` section of `mgm-config.json`)   
        - The [HYPEROPT PARAMETERS CONFIGURATION SECTION](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#HYPEROPT-PARAMETERS-CONFIGURATION-SECTION)   
8) Load your results into the `Total-Overall-Signal-Importance-Calculator.py` and run it's [Go-To Command](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands) to receive a nice weighted signal report for sharing in the [Discord server](https://discord.gg/xFZ9bB6vEz) and to pull conclusions from.  


# How to Configure MoniGoMani:
In total 4 files are used in the configuration of MoniGoMani:   
- [`mgm-config.json`](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#mgm-config.json): This is the **main** configuration file, containing:   
    - The main `MoniGoMani` settings   
    - The main `Freqtrade` settings (See [The Official Freqtrade Configuration Documentation](https://www.freqtrade.io/en/latest/configuration/) to learn how to configure these)   
- [`mgm-config-private.json`](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config-private.json): This split configuration file contains some `Freqtrade` settings containing critical private information, **never** share this file! 
- `mgm-config-hyperopt.json`: This file contains the optimized HyperOptable `MoniGoMani` and `Freqtrade` settings. It will be created when following the [How to Optimize MoniGoMani](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) process
- [`MoniGoManiHyperStrategy.py`](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#MoniGoManiHyperStrategy.py): The **main** strategy file also has 2 marked sections with some settings that can be configured:
    - `CONFIG NAMES SECTION`
    - `HYPEROPT PARAMETERS CONFIGURATION SECTION`

## mgm-config.json
**Link to:** [mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config.json)   
The main `MoniGoMani` settings can be found under `monigomani_settings`:
| Parameter(s) | Description |
| --- | --- |
| **timeframe** <br> **backtest_timeframe** | These values configure the `timeframe`s used in MoniGoMani. <br> **Documentation:** [TimeFrame-Zoom](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#timeframe-zoom) <br> **Datatypes:** Integer |
| **startup_candle_count** | Number of candles the strategy requires before producing valid signals during BackTesting/HyperOpting. <br> By default this is set to `400` since MoniGoMani uses a 200EMA, which needs 400 candles worth of data to be calculated. <br> **Datatype:** Integer |
| **precision** | This value can be used to control the precision of HyperOpting. Default is `1`. <br> **Documentation:** [Precision Setting](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#precision-setting) <br> **Datatype:** Integer |
| **min_weighted_signal_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for weighted signals. <br> **2nd HyperOpt Run:** Weak weighted signals are weeded out by overriding them to their respective Minimal value. <br> **Datatype:** Integer |
| **max_weighted_signal_value** | **1st HyperOpt Run:** Maximum value used in the HyperOpt Space for weighted signals. <br> **2nd HyperOpt Run:** Strong weighted signals are boosted by overriding them to their respective Maximum value. <br> **Datatype:** Integer |
| **min_trend_total_signal_needed_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for total weighted signals needed. <br> **Datatype:** Integer |
| **min_trend_total_signal_needed_candles_lookback_window_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for the candle lookback window for total signals needed. <br> **Datatype:** Integer |
| **max_trend_total_signal_needed_candles_lookback_window_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for the candle lookback window for total signals needed. <br> **Datatype:** Integer |
| **search_threshold_weighted_signal_values** | **2nd HyperOpt Run:** Used to refine the search spaces for remaining weighted signals with the value found in the 1st run +- the threshold. <br> **Datatype:** Integer |
| **search_threshold_trend_total_signal_needed_candles_lookback_window_value** | **2nd HyperOpt Run:** Used to refine the search spaces for the candle lookback window for total signals needed with the values found in the 1st run +- the threshold. <br> **Datatype:** Integer |
| **number_of_weighted_signals** | Set the `number_of_weighted_signals` setting to the total number of different weighted signals in use in the weighted tables. <br> `buy/sell__downwards/sideways/upwards_trend_total_signal_needed` settings will be multiplied with this value, so their search spaces will be larger, resulting in more equally divided total weighted signal scores when HyperOpting. <br> **Datatype:** Integer |
| **roi_table_step_size** | MoniGoMani generates a really long custom ROI-Table (Return of Interest), so it will have fewer gaps in it and be more continuous in it's decrease. <br> This setting alters the size of the steps (in minutes) to be used when calculating the long continuous ROI-Table. <br> **Datatype:** Integer |
| **debuggable_weighted_signal_dataframe** | If set to `True` all Weighted Signal results will be added to the dataframe for easy debugging with BreakPoints. <br> **<span style="color:darkorange">WARNING:</span> Disable this for anything else then debugging in an IDE! (Integrated Development Environment)** <br> **Datatype:** Boolean |
| **use_mgm_logging** | If set to `True` MoniGoMani logging will be displayed to the console and be integrated in Freqtrades native logging, further logging configuration can be done by setting individual `mgm_log_levels_enabled`. <br> It's recommended to set this to `False` for HyperOpting/BackTesting unless you are testing with breakpoints. <br> **Datatype:** Boolean |
| **mgm_log_levels_enabled** | It allows turning on/off individual `info`, `warning`, `error` and `debug` logging <br> For Live Runs it's recommended to disable at least `info` and `debug` logging, to keep MGM as lightweight as possible! <br> `debug` is very verbose! Always set it to `False` when BackTesting/HyperOpting! <br> **Datatype:** Boolean |

### TimeFrame-Zoom:
To prevent profit exploitation during BackTesting/HyperOpting we BackTest/HyperOpt MoniGoMani using TimeFrame-Zoom.
When normally a `timeframe` (1h candles) would be used, you can zoom in using a smaller `backtest_timeframe`
(5m candles) instead. This happens while still using an `informative_timeframe` (original 1h candles) to generate
the buy/sell signals.

With this more realistic results should be found during BackTesting/HyperOpting. Since the buy/sell signals will 
operate on the same `timeframe` that Live would use (1h candles), while at the same time `backtest_timeframe` 
(5m or 1m candles) will simulate price movement during that `timeframe` (1h candle), providing more realistic 
trailing stoploss and ROI behaviour during BackTesting/HyperOpting.   
If you haven't yet please read: [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)


**<span style="color:darkorange">WARNING:</span> To disable TimeFrame-Zoom just use the same candles for `timeframe` & `backtest_timeframe`**   
**<span style="color:darkorange">WARNING:</span> Candle data for both `timeframe` as `backtest_timeframe` will have to be downloaded before you will be able to BackTest/HyperOpt! (Since both will be used)**   
**<span style="color:darkorange">WARNING:</span> This will be slower than BackTesting at 1h and 1m is a CPU killer. If you plan on using trailing stoploss or ROI, you probably want to know that your BackTest results are not complete lies.**   

### TimeFrame-Zoom Examples:
| Parameter | Description |
| --- | --- |
| **timeframe**='1h' | TimeFrame used during Dry/Live-runs |
| **backtest_timeframe**='5m' | Zoomed in TimeFrame used during BackTesting/HyperOpting |

### Precision Setting:
The `precision` setting can be used to control the precision / step size used during HyperOpting.   
A value **smaller than 1** will limit the search space, but may skip over good values.   
While a value **larger than 1** increases the search space, but will increase the duration of HyperOpting.   
To disable `precision` / for normal work mode **just** use **1**.   

**<span style="color:darkorange">WARNING:</span> Only use a precision different from 1 during HyperOpting & restore to 1 afterwards!**   
**<span style="color:darkorange">WARNING:</span> HyperOpt Results don't take precision into consideration, after HyperOpting with precision use the Total Overall Signal Importance Calculator's `--precision-used` subcommand to fix the results**   

#### Precision Examples:
| Precision Value | Step Size effectively used during HyperOpting |
| --- | --- |
| **1/5** or **0.2** | **5** (0, 5, 10 ...) |
| **5**   | **1/5** or **0.2** (0, 0.2, 0.4, 0.8, ...) |


## MoniGoManiHyperStrategy.py
**Link to:** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py)   
The **main** strategy file has 2 marked sections with some settings that can be configured:
### CONFIG NAMES SECTION
These settings can be used to make MoniGoMani load config files with a custom file name.   
| Parameter | Description |
| --- | --- |
| **mgm_config_name** | Provide a custom file name for `mgm-config.json` |
| **mgm_config_hyperopt_name** | Provide a custom file name for `mgm-config-hyperopt.json` |

### HYPEROPT PARAMETERS CONFIGURATION SECTION
This section can be used to configure the remaining MoniGoMani's HyperOpt Space Parameters at a more in depth level but also more advanced level.   

It contains:
- All the `buy/sell___trades_when_downwards/sideways/upwards` [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides)   
- The Sell Unclogger HyperOpt Space Params, configurable with [Initialize Variables](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#Initialize-variables) and [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides)


#### HyperOpt Setting Overrides:
When the Parameters in the HyperOpt Space Parameters sections are altered as following examples then they can be used as overrides while HyperOpting / BackTesting / Dry/Live-running   
(only truly useful when HyperOpting though!) Meaning you can use this to set individual buy_params/sell_params to a fixed value when HyperOpting!   
   
**<span style="color:darkorange">WARNING:</span> Always double check that when doing a fresh HyperOpt or doing a Dry/Live-run that all overrides are turned off!**   

##### Override / Static Example:
In this case the `default` value will be used as a static value throughout the whole HyperOpt.   

Override `buy___trades_when_sideways` to always be **False**:
```python
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
```
| Function Param | Description |
| --- | --- |
| **default**=X      | The value used when overriding |
| **optimize**=False | Exclude from HyperOpting (Make static) |
| **load**=False     | Don't load from `mgm-config-hyperopt.json` |  

##### HyperOptable / Normal Example:   
In this case the value in `mgm-config-hyperopt.json` will be used as the starting point for the next HyperOpt   
Normal usage of `buy___trades_when_sideways` making it HyperOptable:
```python
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=True, space='buy', optimize=True, load=True)
```
| Function Param | Description |
| --- | --- |
| **default**=X     | Not used in this case |
| **optimize**=True | Include during HyperOpting (Look for "ideal" value) |
| **load**=True     | Load from `mgm-config-hyperopt.json` |  

#### Initialize Variables:   
The `init_vars()` function is used to automatically initialize MoniGoMani's HyperOptable parameter values for both HyperOpt Runs.   

##### Initialize Variables Example:   
Example for `sell___unclogger_minimal_losing_trades_open`   
```python
param = init_vars(sell_params, "sell___unclogger_minimal_losing_trades_open",
                      2, 5, 1, precision, False)
```
| Parameter | Description |
| --- | --- |
| *(parameter_min_value=)* 2 | Minimal search space value to use during the 1st HyperOpt Run and override value for weak signals on the 2nd HyperOpt Run |
| *(parameter_max_value=)* 5 | Maximum search space value to use during the 1st HyperOpt Run and override value for weak signals on the 2nd HyperOpt Run |
| *(parameter_threshold=)* 1 | Threshold to use for overriding weak/strong signals and setting up refined search spaces after the 1st HyperOpt Run |
| *(overrideable=)* False | Allow value to be overrideable or not (defaults to `True`) |


# Open Trade Unclogger:
When the Open Trade Unclogger is enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades.   
This `custom_sell()` function should be able to work in tandem with `Trailing stoploss`.   

It will only unclog a losing trade when all following checks have been full-filled (If a check is set to `0` it will be taken out of the equation, thus the unclogger will continue checking further without it):    
- Check if `sell___unclogger_enabled` is `True`, otherwise abort further unclogger logic.
- Check if everything in custom_storage is up to date with all_open_trades
- Check if there are enough losing trades open to fulfil `sell___unclogger_minimal_losing_trades_open`
- Check if there is a losing trade open for the pair currently being run through the MoniGoMani loop
- Check if trade has been open for `sell___unclogger_minimal_losing_trade_duration_minutes` (long enough to give it a recovery chance)
- Check if `sell___unclogger_open_trades_losing_percentage_needed` is fulfilled
- Check if open_trade's trend changed negatively during past `sell___unclogger_trend_lookback_candles_window`:   
For unclogging to occur `sell___unclogger_trend_lookback_candles_window_percentage_needed` should be fulfilled!   
The trends used for the calculations in this check can be configured with `sell___unclogger_trend_lookback_window_uses_downwards/sideways/upwards_candles=True/False` (Its recommended setting these last 3 true/false values manually using [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides)).   
Each candle fulfilling a trend set to `True` will be added in the sum used to calculate the value for `sell___unclogger_trend_lookback_candles_window_percentage_needed` if it is found in the lookback window.   


Only used when `sell___unclogger_enabled` is set to `True`!


# Total Overall Signal Importance Calculator:
Execute: `python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc USDT -lf ./user_data/mgm-config-hyperopt.json -cf ./user_data/Total-Average-Signal-Importance-Report.log` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better! Now it will also export to a `Total-Average-Signal-Importance-Report.log` file for easy sharing!   
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals!   

### Handy Calculator Sub Commands:
- `-h` or `--help`: Print out information about the usage of all sub commands.
- `-sc` or `--stake-currency` ***Mandatory***: Stake currency displayed in the report (Should match to what is under `stake_currency` in your `mgm-config.json`)
- `-lf` or `--load-file` ***Optional (Unused by default)***: Path to `.json` file to load HyperOpt Results from which will be used in the Calculator.   
`.json`'s should be extracted with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands)
**Warning** Make sure your calculator copy-paste section is complete before using this sub-command!   
- `-cf` or `--create-file` ***Optional (Unused by default)***: Save the Total-Average-Signal-Importance-Report as a `.log` file with a custom filename and file output location   
- `-nf` or `--no-file` ***Optional (Defaults to `True` when not omitted)***: Do not output the Total-Average-Signal-Importance-Report as a `.log` file
- `-fm` or `--fix-missing` ***Optional (Defaults to `True` when not omitted)***: Re-Include missing weighted buy/sell_params with **0 as their value** & re-print them as copy/paste-able results. Also keeps the tool from crashing when there are missing values.
- `-pu` or `--precision-used` ***Optional (Defaults to `1` when not omitted)***: The precision value used during HyperOpt. Can be decimal (0.2) or fraction 1/5. Mostly useful after a running a HyperOpt with precision different from 1, used to patch the weights of the signals displayed in the report to what we would expect them to be for comparison with other results.


# Custom HyperLoss Functions:
MoniGoMani comes with an extra set of loss functions for HyperOpting, supplementing the ones shipped with FreqTrade.
You can find these functions in `M̀oniGoMani/user_data/hyperopts/`, and can use them by overriding the freqtrade HyperOpt parameter `--hyperopt-loss`.   
   
Following 2 Custom HyperLoss Functions ship with the MoniGoMani Framework:
- [**WinRatioAndProfitRatioLoss**](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/HyperOpts/WinRatioAndProfitRatioLoss.py): Attempts to optimise for the best profit **and** stability (Returns smaller number for better results)   
- [**UncloggedWinRatioAndProfitRatioLoss**](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/HyperOpts/UncloggedWinRatioAndProfitRatioLoss.py): Same as WinRatioAndProfitRatioLoss but has a configurable Percentage of loss (See `unclogger_profit_ratio_loss_tolerance` setting inside the file) to ignore while HyperOpting (Since small losses are a by-product of the Unclogger)
   
**Example Usage:**
```powershell
--hyperopt-loss WinRatioAndProfitRatioLoss
```


# PairLists:
By default, MoniGoMani includes 2 pairlists in `mgm-config.json`:   
- A VolumePairList: 
  - Best to use for Dry and Live Running
  - Will automatically update to the current best top volume coin pairs available
- A StaticPairList: 
  - Used for BackTesting / HyperOpting since a VolumePairList cannot be used here.
  - When [optimizing](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) MoniGoMani for actual Dry/Live-running (instead of testing) it's truly recommended to [download a fresh top volume StaticPairList](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#download-staticpairlists) and HyperOpt upon that (Preferably as big as possible, but beware of the warning below)!   
  This should yield much better & more realistic results during HyperOpting/BackTesting!   
  This is due to giving a better reflection of the current market and being closer to the VolumePairList used during Dry/Live-run's.

Switching between the PairList in use can easily be done by moving the `_` in front of the `pairlists` value inside `mgm-config.json` for the pairlist you wish to disable.

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
Retrieve a current **Binance-USDT-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))* (The amount of pairs in these top volume lists can be altered by opening up `Binance-Retrieve-Top-Volume-StaticPairList.json` and changing the `number_assets` value near the bottom of the file to the amount of pairs you'd like in your list):
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote USDT --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json
```

Retrieve a current **Binance-USDT-All-Tradable-StaticPairList.json** file *(using [Binance-Retrieve-All-Tradable-StaticPairList.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-All-Tradable-StaticPairList.py))* (Beware, can be very high system requirements due to a lot of pairs!):
```powershell
python ./user_data/mgm_tools/Binance-Retrieve-All-Tradable-StaticPairList.py -q USDT > ./user_data/mgm_pair_lists/Binance-USDT-All-Tradable-StaticPairList.json
```

**After Downloading** the StaticPairList will be available under `./user_data/mgm_pair_lists/<<NAME_HERE>>-StaticPairList.json`, just open up the file and copy the PairList Data into your own `mgm-config.json` file under `pair_whitelist` section to start using it!   

Don't forget to **Download Candle Data** before HyperOpting or BackTesting (Example timerange):   
```powershell
freqtrade download-data --timerange 20201201-20210316 -t 5m 1h -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json
```

## Go-To Commands:
**Hyper Opting** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py):
```powershell
freqtrade hyperopt -s MoniGoManiHyperStrategy -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --hyperopt-loss WinRatioAndProfitRatioLoss --spaces all -e 1000 --timerange 20210101-20210316
```
**Apply HyperOpt Results** from a `<epoch of choice>`:
```powershell
freqtrade hyperopt-show -n <epoch of choice> -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --no-header --print-json | tail -n 1 | jq '.' > ./user_data/mgm-config-hyperopt.json
```
**Reset HyperOpt Results**:
```powershell
rm ./user_data/mgm-config-hyperopt.json
```
**Back Testing** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py):
```powershell
freqtrade backtesting -s MoniGoManiHyperStrategy -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --timerange 20210101-20210316
```
**Total Average Signal Importance Calculation** *(with the [Total-Overall-Signal-Importance-Calculator.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py))*:
```powershell
python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc USDT -lf ./user_data/mgm-config-hyperopt.json -cf ./user_data/Total-Average-Signal-Importance-Report.log
```
Retrieve a current **Binance-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))*:
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote USDT --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json
# Don't forget to open the downloaded '...-StaticPairList.json' and copy the PairList Data into your own 'mgm-config.json' file to start using it!
```
**Download Candle Data**:
```powershell
freqtrade download-data --timerange 20201201-20210316 -t 5m 1h -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json
```

# How to share your test results properly:
The easiest way to share how your MGM setup has been doing would be by posting a screenshot in the [Discord Server](https://discord.gg/xFZ9bB6vEz) with the output of the `/status table` and `/profit` commands (Using the Telegram connection of the bot).   
   
Also, one of the other most welcome things is the results from the `Total-Overall-Signal-Importance-Calculator`, but you'll have to paste your own fresh HyperOpt results in it first before it can make you a nice report that can help us find better signals for MGM !:rocket:   

Of course all FreqUI / Telegram / config / HyperOpt results done on MGM **can be** useful / be learned from!
Try to **always include** a  `Total-Overall-Signal-Importance-Calculator` report or just your own MoniGoMani file with your HyperOpt results applied to it!   
Since without knowing which signal weights or which on/off settings are applied we can't really truly learn much from your results!   

The epoch table being generated when HyperOpting + the number of the epoch you used is also very helpful, so we can easily rule out if your test results are exploited. (See [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)!)   

# Common mistakes:

### TypeError: integer argument expected, got float   
You likely are using a `Float` value where you should be using a `Integer` value. Hopefully your error will show more information about which Parameter.   
- `Integer` = Whole number. Examples: 1, 3, 23
- `Float` = Decimal number. Examples: 1.53, 4.2, 17.12   

### -bash: jq: command not found
You still need to install [jq](https://stedolan.github.io/jq/)
