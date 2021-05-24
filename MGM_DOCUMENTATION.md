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
**<span style="color:darkorange">WARNING:</span> MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) unless you really know what you are doing when manually allocating parameters!**   
**I strongly recommended to [re-optimize](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!**   

# Freqtrade Installation:   
This guide now assumes you have Freqtrade already installed, if you haven't yet, then please see [VERYQUICKSTART_FREQTRADE.md](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART_FREQTRADE.md)

# How to Optimize MoniGoMani:   
*(These are just my ideas/theories, if you have other ideas, please test them & report your results to [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can learn and improve this flow! Also yes the current process is lengthy, but we hope to automate this where possible in further versions)*   
**<span style="color:darkorange">WARNING:</span> It's strongly advised to not do any manual alterations to an already optimized MGM setup, the recommended way to do manual alterations is through setting up [overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides) + [narrowed down search spaces](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-narrowing-down-search-spaces), and finally firing up a new HyperOpt to apply those!**   
   
0) When you change anything in your `config.json`, `config-private.json` (besides personal info etc) or in `MoniGoManiHyperStrategy` itself you should always re-hyperopt to find the new ideal weights for your setup. This should also be done when the market changes in it's long term direction!   
1) Download a good Top Volume StaticPairList and update this in your `config-private.json`. Instructions for how to do this are under [PairLists](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#pairlists).
2) Do some Technical Analysis on how your stake currency has been behaving in the last months/weeks & pick a logical timeframe to do your hyperopt upon (The timeframe in the go-to commands for example resembles some bullish rise/correction cycles & I believe 2021 will be a bullish year thus I think it's a good timeframe to test upon).   
3) Set up the [Current Default MoniGoMani Overrides + Refined Search Spaces](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#current-default-monigomani-overrides--refined-search-spaces) manually with some logical thinking. We do this to disable HyperOpting for some settings inside MGM that don't always get placed logically by HyperOpt. This helps refine the search space during HyperOpting, pushing it more towards where we want it to look. Instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides)   
4) HyperOpt MoniGoManiHyperStrategy for a 1st run with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands) (Free to alter the command if you have a good idea that you want to test)   
5) Pick the `epoch` you deem best. The last one is not always the best one & be wary of profit exploitation on the last epochs! You can use `freqtrade hyperopt-show -n <EPOCH HERE>` to print out HyperOpt results found for a certain epoch.   
6) Apply the HyperOpt results from your 1st run into the HyperOpt Results Copy/Paste Section of `MoniGoManiHyperStrategy.py`
7) Override/Disable HyperOpting for following (Instructions for how to do this are under [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides)):
    - All the `buy/sell__downwards/sideways/upwards_trend_total_signal_needed_candles_lookback_window` settings (Since want to push the 2nd run back into the direction of the 1st run)
    - The `buy/sell_downwards/sideways/upwards_trend_signal_weight` settings that scored lower then `10%` in the 1st HyperOpt run and override them manually to `0%` (Indication of weak signal / signal not working well during these trends with your current weight allocation setup.   
    Also `10%` was just an idea, feel free to change this)   
    - The `buy/sell_downwards/sideways/upwards_trend_signal_weight` settings that scored higher then `90%` in the 1st HyperOpt run and override them manually to `100%` (Indication of strong signal / signal good enough in that trend to act on its own as a full buy/sell signal.   
    Also `90%` was just an idea, feel free to change this)   
8) Refine the Search Spaces for following (Instructions for how to do this are under [HyperOpt Narrowing Down Search Spaces](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-narrowing-down-search-spaces). We do this to push the next HyperOpt run back in the direction that we already had going during the 1st HyperOpt run):
    - All the `buy/sell_downwards/sideways/upwards_trend_signal_weight` settings that still remain in the HyperOpt space (aka normal, not overridden). Change the search space for each `weighted signal` remaining, from the usual **(0 - 100)** and set it to **±10** the value found for said `weighted signal` during the 1st HyperOpt run.   
    Example: If for `sell_sideways_trend_bollinger_bands_weight` a weight of `33` was found during the 1st HyperOpt run, then the refined search space would become as following:   
    `sell_sideways_trend_bollinger_bands_weight = IntParameter(int(23 * precision), int(43 * precision), default=0, space='sell', optimize=True, load=True)`   
    - All the `buy/sell_downwards/sideways/upwards_trend_total_signal_needed` settings. Change the search space for each `total needed signal`, from the usual **(30 - (100 * `number_of_weighted_signals`))** and set it to **±(10 * `number_of_weighted_signals`)** the value found for said `total needed signal` during the 1st HyperOpt run.   
    Example: If for `sell__upwards_trend_total_signal_needed` a weight of `311` was found during the 1st HyperOpt run and if `number_of_weighted_signals = 9`, then the refined search space would become as following (10 * 9 = ±90):   
    `sell__upwards_trend_total_signal_needed = IntParameter(int(221 * precision), int(401 * precision), default=30, space='sell', optimize=True, load=True)`
    - Feel free to further refine/override the Open Trade Unclogger's spaces too, but refine using values that you deem to make sense   
9) HyperOpt MoniGoManiHyperStrategy for a 2nd run with the command provided in the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands). This is needed since we have been altering the "perfectly" calculated setup, thus we have to re-balance the weights in use now. This should not cause overfitting since it's a complete fresh hyperopt run.   
10) Pick the `epoch` you deem best. The last one is not always the best one & be wary of profit exploitation on the last epochs! You can use `freqtrade hyperopt-show -n <EPOCH HERE>` to print out HyperOpt results found for a certain epoch.  
11) Copy/Paste your results into the `Total-Overall-Signal-Importance-Calculator.py` & run it's [Go-To Command](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands) to recieve a nice weighted signal report for sharing in the [Discord server](https://discord.gg/xFZ9bB6vEz) and to pull conclusions from.   
12) Paste the full HyperOpt Results in the Copy/Paste Section of `MoniGoManiHyperStrategy.py`
13) Set the Override settings and Search spaces to their default values again to prevent confusion during your next HyperOpt run & you should have a nicely optimised version now! :smile:      


# HyperOpt Setting Overrides:
When the Parameters in the HyperOpt Space Parameters sections are altered as following examples then they can be used as overrides while hyperopting / backtesting / dry/live-running   
(only truly useful when hyperopting though!) Meaning you can use this to set individual buy_params/sell_params to a fixed value when hyperopting!   
   
**<span style="color:darkorange">WARNING:</span> Always double check that when doing a fresh hyperopt or doing a dry/live-run that all overrides are turned off!**   

### Override / Static Examples:
In this case the `default` value will be used as a static value throughout the whole HyperOpt.   

Override `buy___trades_when_sideways` to always be **False**:
```python
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
```
Override `sell_downwards_trend_macd_weight` to always be **0**:
```python
sell_downwards_trend_macd_weight = \
    IntParameter(0, int(100 * precision), default=0, space='sell', optimize=False, load=False)
```
| Function Param | Meaning |
| --- |--- |
| **default**=X      | The value used when overriding |
| **optimize**=False | Exclude from hyperopting (Make static) |
| **load**=False     | Don't load from the HyperOpt Results Copy/Paste Section |  

### HyperOptable / Normal Examples:   
In this case the value in the HyperOpt Results copy/paste on top will be used as the starting point for the next HyperOpt   
Normal usage of `buy___trades_when_sideways` making it hyperoptable:
```python
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=True, space='buy', optimize=True, load=True)
```
Normal usage of `sell_downwards_trend_macd_weight` making it hyperoptable:
```python
sell_downwards_trend_macd_weight = \
    IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
```
| Function Param | Meaning |
| --- |--- |
| **default**=X     | Not used in this case |
| **optimize**=True | Include during hyperopting (Look for "ideal" value) |
| **load**=True     | Load from the HyperOpt Results Copy/Paste Section |  

# HyperOpt Narrowing Down Search Spaces:   
The search spaces used for HyperOptable settings in MoniGoMani can easily be tweaked/fine-tuned to try and improve upon profit being made.   
It also helps in cutting down the time needed for HyperOpting since fewer values will be possible. This if applied right it means we are pushing/pointing hyperopt in the right direction before it runs off doing its crunching.   

### Narrowed Down Space Example:
Hyperopt Space for `sell_downwards_trend_macd_weight` narrowed down to only search for an ideal weight between **34 up to 54**:
```python
sell_downwards_trend_macd_weight = \
    IntParameter(int(34 * precision), int(54 * precision), default=int(44 * precision), space='sell', optimize=True, load=True)
```

# Current Default MoniGoMani Overrides + Refined Search Spaces:
These are the current go-to overrides & refined search spaces for the 1st HyperOpt Run

*(More testing should be done to find out if there are other/more overrides that would work better!)*   
Feel free to **manually** alter these if you think other values are more logical. These should be applied using the examples above.   

**The `buy/sell___trades_when_downwards/sideways/upwards` settings have proven to sometimes create a hodlr bot if not overriden when hyperopting, which is not what we want:**   
```python
buy___trades_when_downwards = \
    CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)
buy___trades_when_sideways = \
    CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
buy___trades_when_upwards = \
    CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)

sell___trades_when_downwards = \
    CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
sell___trades_when_sideways = \
    CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)
sell___trades_when_upwards = \
    CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
```

**Following narrowed down search spaces + overrides should result in a more realisticly configured unclogger:**
```python
# We'd like to use the Open Trade Unclogger so overridden it to 'True'
sell___unclogger_enabled = \
    CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
# Default narrowed down search-spaces
sell___unclogger_minimal_losing_trade_duration_minutes = \
    IntParameter(int(15 * precision), int(60 * precision), default=int(15 * precision), space='sell', optimize=True, load=True)
sell___unclogger_minimal_losing_trades_open = \
    IntParameter(1, 5, default=1, space='sell', optimize=True, load=True)
sell___unclogger_open_trades_losing_percentage_needed = \
    IntParameter(1, int(60 * precision), default=1, space='sell', optimize=True, load=True)
sell___unclogger_trend_lookback_candles_window = \
    IntParameter(int(10 * precision), int(60 * precision), default=int(10 * precision), space='sell', optimize=True, load=True)
sell___unclogger_trend_lookback_candles_window_percentage_needed = \
    IntParameter(int(10 * precision), int(40 * precision), default=int(10 * precision), space='sell', optimize=True, load=True)
# Setting these logically manually is not too hard to do and will narrow down the hyperopt space, thus resulting in less 
# time/system resources needed to run our hyperopt (We basically push it in the direction we want by hand doing this)
sell___unclogger_trend_lookback_window_uses_downwards/sideways/upwards_candles = \
    CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
sell___unclogger_trend_lookback_window_uses_sideways_candles = \
    CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
sell___unclogger_trend_lookback_window_uses_upwards_candles = \
    CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)
```

**Following are the default search spaces for all the Total Buy/Sell Signal Weights needed + their corresponding lookback windows:**
```python
buy/sell__downwards/sideways/upwards_trend_total_signal_needed = \
    IntParameter(int(30 * precision), int(100 * number_of_weighted_signals * precision), default=int(30 * precision), space='buy/sell', optimize=True, load=True)
buy/sell__downwards/sideways/upwards_trend_total_signal_needed_candles_lookback_window = \
    IntParameter(1, 6, default=1, space='buy/sell', optimize=True, load=True)
```

**Following are the default search spaces for all the Weighted Signals:**
```python
buy/sell_downwards/sideways/upwards_trend_signal_weight = \
    IntParameter(0, int(100 * precision), default=0, space='sell', optimize=True, load=True)
```


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


Only used when `use_custom_stoploss` (To store open trade data) & `sell_params['sell___unclogger_enabled']` are both set to `True`!


# Total Overall Signal Importance Calculator:
Paste the `buy_params` & `sell_params` results from your HyperOpt over in the `/user_data/Total-Overall-Signal-Importance-Calculator.py` file.   
Then execute: `python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc BTC` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better! Now it will also export to a `importance.log` file in the same folder for easy sharing!   
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals!   

### Handy Calculator Sub Commands:
- `-h` or `--help`: Print out information about the usage of all sub commands.
- `-sc` or `--stake-currency` ***Mandatory***: Stake currency displayed in the report (Should match to what is under `stake_currency` in your `config.json`)
- `-lf` or `--load-file` ***Optional (Unused by default)***: Path to `.json` file to load HyperOpt Results from which will be used in the Calculator.   
`.json`'s should be extracted with `freqtrade hyperopt-show --best --no-header --print-json > ./user_data/config-mgm-hyperopt.json`   
**Warning** Make sure your calculator copy-paste section is complete before using this sub-command!   
- `-cf` or `--create-file` ***Optional (Unused by default)***: Save the Total-Average-Signal-Importance-Report as a `.log` file with a custom filename and file output location   
- `-nf` or `--no-file` ***Optional (Defaults to `True` when not omitted)***: Do not output the Total-Average-Signal-Importance-Report as a `.log` file
- `-fm` or `--fix-missing` ***Optional (Defaults to `True` when not omitted)***: Re-Include missing weighted buy/sell_params with **0 as their value** & re-print them as copy/paste-able results. Also keeps the tool from crashing when there are missing values.
- `-pu` or `--precision-used` ***Optional (Defaults to `1` when not omitted)***: The precision value used during hyperopt. Can be decimal (0.2) or fraction 1/5. Mostly useful after a running a hyperopt with precision different from 1, used to patch the weights of the signals displayed in the report to what we would expect them to be for comparison with other results.


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


# Number of weighted signals:
Set the `number_of_weighted_signals` setting to the total number of different weighted signals in use in the weighted tables.   
`buy/sell__downwards/sideways/upwards_trend_total_signal_needed` settings will be multiplied with this value so their search spaces will be larger, resulting in more equally divided total weighted signal scores when hyperopting.
   
**Example Usage:**
```python
number_of_weighted_signals = 9
```


# Long Continuous ROI Table StepSize:
MGM generates a really long custom ROI-Table (Return of Interest) so it will have less gaps in it and be more continuous in it's decrease.
Size of the steps (in minutes) to be used when calculating the long continuous ROI-Table, can be configured using the `roi_table_step_size` setting.

   
**Example Usage:**
```python
roi_table_step_size = 5
```


# Custom HyperLoss Functions:
MoniGoMani comes with an extra set of loss functions for HyperOpting, supplementing the ones shipped with FreqTrade.
You can find these functions in `M̀oniGoMani/user_data/hyperopts/`, and can use them by overriding the freqtrade hyperopt parameter `--hyperopt-loss`.   
   
Following 2 Custom HyperLoss Functions ship with the MoniGoMani Framework:
- [**WinRatioAndProfitRatioLoss**](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/WinRatioAndProfitRatioLoss.py): Attempts to optimise for the best profit **and** stability (Returns smaller number for better results)   
- [**UncloggedWinRatioAndProfitRatioLoss**](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/UncloggedWinRatioAndProfitRatioLoss.py): Same as WinRatioAndProfitRatioLoss but has a configurable Percentage of loss (See `unclogger_profit_ratio_loss_tolerance` setting inside the file) to ignore while HyperOpting (Since small losses are a by-product of the Unclogger)
   
**Example Usage:**
```powershell
--hyperopt-loss WinRatioAndProfitRatioLoss
```


# PairLists:
By default, MoniGoMani includes 2 pairlists in `config-btc.json`:   
- A VolumePairList: 
  - Best to use for Dry and Live Running
  - Will automatically update to the current best top volume coin pairs available
- A StaticPairList: 
  - Used for BackTesting / HyperOpting since a VolumePairList cannot be used here.
  - When [optimizing](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) MoniGoMani for actual dry/live-running (instead of testing) it's truly recommended to [download a fresh top volume StaticPairList](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#download-staticpairlists) and HyperOpt upon that (Preferably as big as possible, but beware of the warning below)!   
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


# TimeFrame-Zoom:
To prevent profit exploitation during backtesting/hyperopting we backtest/hyperopt this can be used.
When normally a `timeframe` (1h candles) would be used, you can zoom in using a smaller `backtest_timeframe`
(5m candles) instead. This happens while still using an `informative_timeframe` (original 1h candles) to generate
the buy/sell signals.

With this more realistic results should be found during backtesting/hyperopting. Since the buy/sell signals will 
operate on the same `timeframe` that live would use (1h candles), while at the same time `backtest_timeframe` 
(5m or 1m candles) will simulate price movement during that `timeframe` (1h candle), providing more realistic 
trailing stoploss and ROI behaviour during backtesting/hyperopting.

**<span style="color:darkorange">WARNING:</span> Since MoniGoMani v0.10.0 it appears TimeFrame-Zoom is not needed anymore and even lead to bad results!**
**<span style="color:darkorange">WARNING:</span> To disable TimeFrame-Zoom just use the same candles for `timeframe` & `backtest_timeframe`**   
**<span style="color:darkorange">WARNING:</span> Remove the `timeframe` line from your `config-btc.json` if it would still be there! Otherwise, TimeFrame-Zoom won't work properly in the current version!**   
**<span style="color:darkorange">WARNING:</span> Candle data for both `timeframe` as `backtest_timeframe` will have to be downloaded before you will be able to backtest/hyperopt! (Since both will be used)**   
**<span style="color:darkorange">WARNING:</span> This will be slower than backtesting at 1h and 1m is a CPU killer. If you plan on using trailing stoploss or ROI, you probably want to know that your backtest results are not complete lies.**   

### TimeFrame-Zoom Examples:
| Parameter | Meaning |
| --- | --- |
| **timeframe**='1h' | TimeFrame used during dry/live-runs |
| **backtest_timeframe**='5m' | Zoomed in TimeFrame used during backtesting/hyperopting |


# Go-To Commands:
For **Hyper Opting** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) using the new [MoniGoManiConfiguration.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiConfiguration.py):
```powershell
freqtrade hyperopt -s MoniGoManiConfiguration -c ./user_data/mgm-config-usdt.json -c ./user_data/mgm-config-private.json --hyperopt-loss WinRatioAndProfitRatioLoss --spaces all -e 1000 --timerange 20210101-20210316
```
For **Back Testing** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) using the new [MoniGoManiConfiguration.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiConfiguration.py)::
```powershell
freqtrade backtesting -s MoniGoManiConfiguration -c ./user_data/mgm-config-usdt.json -c ./user_data/mgm-config-private.json --timerange 20210101-20210316
```
For **Total Average Signal Importance Calculation** *(with the [Total-Overall-Signal-Importance-Calculator.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py))*:
```powershell
python ./user_data/mgm_tools/Total-Overall-Signal-Importance-Calculator.py -sc USDT
```

To retrieve a current **Binance-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))*:
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote USDT --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json
# Don't forget to open the downloaded '...-StaticPairList.json' and copy the PairList Data into your own 'mgm-config-usdt.json' file to start using it!
```

To **Download Candle Data**:
```powershell
freqtrade download-data --timerange 20201201-20210316 -t 5m 1h -c ./user_data/mgm-config-usdt.json -c ./user_data/mgm-config-private.json
```

# How to share your test results properly:
The easiest way to share how your MGM setup has been doing would be by posting a screenshot in the [Discord Server](https://discord.gg/xFZ9bB6vEz) with the output of the `/status table` and `/profit` commands (Using the Telegram connection of the bot).   
   
Also, one of the other most welcome things is the results from the `Total-Overall-Signal-Importance-Calculator`, but you'll have to paste your own fresh hyperopt results in it first before it can make you a nice report that can help us find better signals for MGM !:rocket:   

Of course all FreqUI / Telegram / config / HyperOpt results done on MGM **can be** useful / be learned from!
Try to **always include** a  `Total-Overall-Signal-Importance-Calculator` report or just your own MoniGoMani file with your hyperopt results applied to it!   
Since without knowing which signal weights or which on/off settings are applied we can't really truly learn much from your results!   

The epoch table being generated when hyperopting + the number of the epoch you used is also very helpful, so we can easily rule out if your test results are exploited. (See [Backtesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)!)   

# Common mistakes:

### TypeError: integer argument expected, got float   
You likely are using a `Float` value where you should be using a `Integer` value. Hopefully your error will show more information about which Parameter.   
- `Integer` = Whole number. Examples: 1, 3, 23
- `Float` = Decimal number. Examples: 1.53, 4.2, 17.12   

### -bash: jq: command not found
[jq](https://stedolan.github.io/jq/) (command-line JSON processor) still needs to be installed.