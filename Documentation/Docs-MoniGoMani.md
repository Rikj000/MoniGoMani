<p align="left">
    <a href="https://discord.gg/xFZ9bB6vEz">
        <img src="https://img.shields.io/discord/819237123009150977?label=Discord%20Server&logo=discord" alt="Join CryptoStonksShallRise on Discord">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases">
        <img src="https://img.shields.io/github/downloads/Rikj000/MoniGoMani/total?label=Total%20Downloads&logo=github" alt="Total Releases Downloaded from GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases/latest">
        <img src="https://img.shields.io/github/v/release/Rikj000/MoniGoMani?include_prereleases&label=Latest%20Release&logo=github" alt="Latest Official Release on GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Rikj000/MoniGoMani?label=License&logo=gnu" alt="GNU General Public License">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md">
        <img src="https://img.shields.io/badge/Docs-MGM__DOCUMENTATION.md-blue?logo=libreoffice&logoColor=white" alt="The current place where you can find all MoniGoMani Documentation!">
    </a> <a href="https://www.freqtrade.io/en/latest/">
        <img src="https://img.shields.io/badge/Trading%20Bot-Freqtrade-blue?logo=probot&logoColor=white" alt="Freqtrade - The open source crypto day-trading bot">
    </a> <a href="https://www.iconomi.com/register?ref=JdFzz">
        <img src="https://img.shields.io/badge/Join-ICONOMI-blue?logo=bitcoin&logoColor=white" alt="ICONOMI - The world’s largest crypto strategy provider">
    </a> <a href="https://www.buymeacoffee.com/Rikj000">
        <img src="https://img.shields.io/badge/-Buy%20me%20a%20Coffee!-FFDD00?logo=buy-me-a-coffee&logoColor=black" alt="Buy me a Coffee as a way to sponsor this project!">
    </a>
</p>

## ⚠️ Disclaimer
 - This strategy is under development. It is not recommended running it live at this moment.
 - Always test this strategy before using it!
 - I am in no way responsible for your live results! This strategy is still experimental and under heavy development!
 - MoniGoMani should always be [re-optimized](#how-to-optimize-monigomani) after doing manual changes!
 - You need to [optimize](#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!
<hr>


# Table of Contents
- [Table of Contents](#table-of-contents)
- [Freqtrade Installation](#freqtrade-installation)
- [How to Optimize MoniGoMani](#how-to-optimize-monigomani)
- [How to Configure MoniGoMani](#how-to-configure-monigomani)
  - [mgm-config.json](#mgm-configjson)
    - [TimeFrame-Zoom](#timeframe-zoom)
      - [TimeFrame-Zoom Examples](#timeframe-zoom-examples)
    - [Precision Setting](#precision-setting)
      - [Precision Examples](#precision-examples)
    - [Trading During Trends](#trading-during-trends)
    - [Weighted Signal Spaces](#weighted-signal-spaces)
    - [Stoploss Spaces](#stoploss-spaces)
    - [Open Trade Unclogger](#open-trade-unclogger)
      - [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries)
    - [Default Stub Values](#default-stub-values)
  - [mgm-config-hyperopt.json](#mgm-config-hyperoptjson)
    - [Reflect over HyperOpt Results](#reflect-over-hyperopt-results)
      - [Bad Weighted signal setup example](#bad-weighted-signal-setup-example)
  - [MoniGoManiHyperStrategy](#monigomanihyperstrategy)
    - [Weighted Signal Interface](#weighted-signal-interface)
      - [Defining Indicators Examples](#defining-indicators-examples)
      - [Defining Weighted Buy & Sell Signals Examples](#defining-weighted-buy--sell-signals-examples)
      - [Visualize Weighted Signals in FreqUI](#visualize-weighted-signals-in-frequi)
- [Total Overall Signal Importance Calculator](#total-overall-signal-importance-calculator)
    - [Handy Calculator Sub Commands](#handy-calculator-sub-commands)
- [Custom HyperLoss Functions](#custom-hyperloss-functions)
- [PairLists](#pairlists)
    - [Enabled StaticPairList / Disabled VolumePairList Example](#enabled-staticpairlist--disabled-volumepairlist-example)
    - [Download StaticPairLists](#download-staticpairlists)
- [Go-To Commands](#go-to-commands)
- [How to test for improvements](#how-to-test-for-improvements)
- [How to share your test results properly](#how-to-share-your-test-results-properly)
- [Common mistakes](#common-mistakes)
    - [HyperOpting: +300 epochs, no results yet](#hyperopting-300-epochs-no-results-yet)
    - [TypeError: integer argument expected, got float](#typeerror-integer-argument-expected-got-float)
    - [-bash: jq: command not found](#-bash-jq-command-not-found)
    - [ValueError: the lower bound X has to be less than the upper bound Y](#valueerror-the-lower-bound-x-has-to-be-less-than-the-upper-bound-y)

# Freqtrade Installation
This guide now assumes you have **Freqtrade** and **jq** already installed, if you haven't yet, then please see [VERYQUICKSTART_FREQTRADE.md](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART_FREQTRADE.md)

# How to Optimize MoniGoMani
*(These are just my ideas/theories, if you have other ideas, please test them & report your results to [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can learn and improve this flow!)*   
**<span style="color:darkorange">WARNING:</span> It's strongly advised to not do any manual alterations to an already optimized MGM setup! The recommended way to do manual alterations is by [Configuring MoniGoMani](#how-to-configure-monigomani), and then following this optimization process to apply them!**   
   

**0)** Delete the previous `mgm-config-hyperopt.json` and/or `MoniGoManiHyperStrategy.json` files if they exist, by using:
   ```powershell
   rm ./user_data/mgm-config-hyperopt.json ./user_data/strategies/MoniGoManiHyperStrategy.json
   ```
**1) Setup your `MoniGoMani` by following [How to Configure MoniGoMani](#how-to-configure-monigomani)**
**2)** Download a good Top Volume StaticPairList and update this in your `mgm-config.json`. Instructions for how to do this are under [PairLists](#pairlists).
**3)** Do some Technical Analysis on how the global crypto market has been behaving in the last months/weeks & pick a logical timeframe to do your HyperOpt upon *(The timeframe in the [Go-To Commands](#go-to-commands) for example resembles some bullish, some bearish and some sideways market behavior, with the idea to give MGM all trends to train upon).*   
**4)** HyperOpt for a **1st HyperOpt Run** with the command provided in the [Go-To Commands](#go-to-commands) (Free to alter the command if you have a good idea that you want to test)   
   The 1st HyperOpt Run *(When no `mgm-config-hyperopt.json` exists)* is automatically ran with the default open search spaces ranging between the default `min_` & `max_` values provided under the `monigomani_settings` section of `mgm-config.json`
**5) [Reflect over your HyperOpt results!]((#reflect-over-hyperopt-results))** The computer just tries to get certain values high (profits) and others low (losses), without a true understanding of their meaning. Because of this HyperOpt is prone to profit exploitation which would be no good when used Live. That's why you need to make yourself familiar with possible [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/). Only then you can tell which results would make sense and would be any good when used Live.   
   You can check and automatically apply an `<epoch of choice>` of which you feel confident, in the list of best results using:
   ```powershell
   freqtrade hyperopt-show -n <epoch of choice> -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json && mv ./user_data/strategies/MoniGoManiHyperStrategy.json ./user_data/mgm-config-hyperopt.json
   ```
**6)** Repeat `Steps 4 and 5` at least for a **2nd HyperOpt Run** with the command provided in the [Go-To Commands](#go-to-commands) (Free to alter the command if you have a good idea that you want to test)
   The 2nd HyperOpt Run *(When a `mgm-config-hyperopt.json` exists)* is automatically ran with:   
       - Refined search spaces ranging between the values found during the 1st Run (Loaded from `mgm-config-hyperopt.json`) plus their `search_threshold_` and minus their `search_threshold_` values provided under the `monigomani_settings` section of `mgm-config.json` (This is done to push the next HyperOpt run back in the direction that we already had going during the 1st HyperOpt run)   
       - Weak weighted signals weeded out by overriding them to their respective `min_` value (Signals of which the found value is below their default `min_` + `search_threshold_` values provided under the `monigomani_settings` section of `mgm-config.json`)   
       - Strong weighted signals are boosted by overriding them to their respective `max_` value (Signals of which the found value is above their default `max_` - `search_threshold_` values provided under the `monigomani_settings` section of `mgm-config.json`)   
**7)** Load your results into the `TotalOverallSignalImportanceCalculator.py` and run it's [Go-To Command](#go-to-commands) to receive a nice weighted signal report for sharing in the [Discord server](https://discord.gg/xFZ9bB6vEz) and to pull conclusions from.  


# How to Configure MoniGoMani
In total 5 files are used in the configuration of MoniGoMani, all can be found in the `user_data` & `user_data/strategies` folders:   
- [`mgm-config.json`](#mgm-config.json): This is the **main configuration file**, containing:   
    - The main `MoniGoMani` settings   
    - The main `Freqtrade` settings (See [The Official Freqtrade Configuration Documentation](https://www.freqtrade.io/en/latest/configuration/) to learn how to configure these)   
- [`mgm-config-private.json`](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config-private.json): This split configuration file contains some `Freqtrade` settings containing critical private information, **never** share this file! 
- [`mgm-config-hyperopt.json`](#mgm-config-hyperopt.json): This file contains the optimized HyperOptable `MoniGoMani` and `Freqtrade` settings. It will be created when following the [How to Optimize MoniGoMani](#how-to-optimize-monigomani) process
- [`MoniGoManiHyperStrategy.py`](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py): The **main strategy file**, containing the [Weighted Signal Interface](#weighted-signal-interface) where you can implement new weighted signals & indicators in a nearly plug and play like fashion.
- [`MasterMoniGoManiHyperStrategy.py`](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MasterMoniGoManiHyperStrategy.py): The **main framework file** also has 2 settings you can configure marked under the `CONFIG NAMES SECTION` section inside the file:
    - **mgm_config_name**: Provide a custom file name for `mgm-config.json`
    - **mgm_config_hyperopt_name**: Provide a custom file name for `mgm-config-hyperopt.json`

## mgm-config.json
**Link to:** [mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config.json)   
The main `MoniGoMani` settings can be found under `monigomani_settings`:
| Parameter(s) | Description |
| --- | --- |
| **timeframe** <br> **backtest_timeframe** | These values configure the `timeframe`s used in MoniGoMani. <br> **Documentation:** [TimeFrame-Zoom](#timeframe-zoom) <br> **Datatypes:** Integer |
| **startup_candle_count** | Number of candles the strategy requires before producing valid signals during BackTesting/HyperOpting. <br> By default this is set to `400` since MoniGoMani uses a 200EMA, which needs 400 candles worth of data to be calculated. <br> **Datatype:** Integer |
| **precision** | This value can be used to control the precision of HyperOpting. Default is `1`. <br> **Documentation:** [Precision Setting](#precision-setting) <br> **Datatype:** Integer |
| **roi_table_step_size** | MoniGoMani generates a really long custom ROI-Table (Return of Interest), so it will have fewer gaps in it and be more continuous in it's decrease. <br> This setting alters the size of the steps (in minutes) to be used when calculating the long continuous ROI-Table. <br> **Datatype:** Integer |
| **trading_during_trends** | The settings inside the `trading_during_trends` section are used to configure during which trends (Downwards/Sideways/Upwards) MGM will be allowed to trade (for Buys/Sells).<br> **Documentation:** [Trading During Trends](#trading-during-trends) <br> **Datatype:** Dictionary |
| **weighted_signal_spaces** | The settings inside the `weighted_signal_spaces` section are used to control how MGM handles the HyperOpting of (Total) Weighted Signal Values during it's [optimization process](#how-to-optimize-monigomani).<br> **Documentation:** [Weighted Signal Spaces](#weighted-signal-spaces) <br> **Datatype:** Dictionary |
| **stoploss_spaces** | The settings inside the `stoploss_spaces` section are used to refine the search spaces that MGM will use for the (trailing) stoploss during it's [optimization process](#how-to-optimize-monigomani).<br> **Documentation:** [Stoploss Spaces](#stoploss-spaces) <br> **Datatype:** Dictionary |
| **unclogger_spaces** | The settings inside the `unclogger_spaces` section are used to refine the search spaces that MGM will use for the open trade unclogger during it's [optimization process](#how-to-optimize-monigomani).<br> **Documentation:** [Open Trade Unclogger](#open-trade-unclogger) <br> **Datatype:** Dictionary |
| **default_stub_values** | The settings inside the `default_stub_values` section are **only used** to control some default startup values that MGM will use when no other values are found and/or used for them.<br> **Documentation:** [Default Stub Values](#default-stub-values) <br> **Datatype:** Dictionary |
| **debuggable_weighted_signal_dataframe** | If set to `True` all Weighted Signal results will be added to the dataframe for easy debugging with BreakPoints. <br> **<span style="color:darkorange">WARNING:</span> Disable this for anything else then debugging in an IDE! (Integrated Development Environment)** <br> **Datatype:** Boolean |
| **use_mgm_logging** | If set to `True` MoniGoMani logging will be displayed to the console and be integrated in Freqtrades native logging, further logging configuration can be done by setting individual `mgm_log_levels_enabled`. <br> It's recommended to set this to `False` for HyperOpting/BackTesting unless you are testing with breakpoints. <br> **Datatype:** Boolean |
| **mgm_log_levels_enabled** | It allows turning on/off individual `info`, `warning`, `error` and `debug` logging <br> For Live Runs it's recommended to disable at least `info` and `debug` logging, to keep MGM as lightweight as possible! <br> `debug` is very verbose! Always set it to `False` when BackTesting/HyperOpting! <br> **Datatype:** Dictionary |

### TimeFrame-Zoom
To prevent profit exploitation during BackTesting/HyperOpting we BackTest/HyperOpt MoniGoMani using TimeFrame-Zoom.
When normally a `timeframe` (1h candles) would be used, you can zoom in using a smaller `backtest_timeframe`
(5m candles) instead. This happens while still using an `informative_timeframe` (original 1h candles) to generate
the buy/sell signals.

With this more realistic results should be found during BackTesting/HyperOpting. Since the buy/sell signals will 
operate on the same `timeframe` that Live would use (1h candles), while at the same time `backtest_timeframe` 
(5m or 1m candles) will simulate price movement during that `timeframe` (1h candle), providing more realistic 
trailing stoploss and ROI behavior during BackTesting/HyperOpting.   
If you haven't yet please read: [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)


**<span style="color:darkorange">WARNING:</span> To disable TimeFrame-Zoom just use the same candles for `timeframe` & `backtest_timeframe`**   
**<span style="color:darkorange">WARNING:</span> Candle data for both `timeframe` as `backtest_timeframe` will have to be downloaded before you will be able to BackTest/HyperOpt! (Since both will be used)**   
**<span style="color:darkorange">WARNING:</span> This will be slower than BackTesting at 1h and 1m is a CPU killer. If you plan on using trailing stoploss or ROI, you probably want to know that your BackTest results are not complete lies.**   

#### TimeFrame-Zoom Examples
| Parameter | Description |
| --- | --- |
| **timeframe**='1h' | TimeFrame used during Dry/Live-runs |
| **backtest_timeframe**='5m' | Zoomed in TimeFrame used during BackTesting/HyperOpting |

### Precision Setting
The `precision` setting can be used to control the precision / step size used during HyperOpting.   
A value **smaller than 1** will limit the search space, but may skip over good values.   
While a value **larger than 1** increases the search space, but will increase the duration of HyperOpting.   
To disable `precision` / for normal work mode **just** use **1**.   

**<span style="color:darkorange">WARNING:</span> Only use a precision different from 1 during HyperOpting & restore to 1 afterwards!**   
**<span style="color:darkorange">WARNING:</span> HyperOpt Results don't take precision into consideration, after HyperOpting with precision use the Total Overall Signal Importance Calculator's `--precision-used` subcommand to fix the results**   

#### Precision Examples
| Precision Value | Step Size effectively used during HyperOpting |
| --- | --- |
| **1/5** or **0.2** | **5** (0, 5, 10 ...) |
| **5**   | **1/5** or **0.2** (0, 0.2, 0.4, 0.8, ...) |

### Trading During Trends
The settings inside `mgm-config.json`'s `trading_during_trends` section are used to configure during which trends (Downwards/Sideways/Upwards) MGM will be allowed to trade (for Buys/Sells).

| Parameter | Description |
| --- | --- |
| **buy_trades_when_downwards** | Enable or completely disable the buying of new trades during downwards trends.<br> **Datatype:** Boolean |
| **buy_trades_when_sideways** | Enable or completely disable the buying of new trades during sideways trends.<br> **Datatype:** Boolean |
| **buy_trades_when_upwards** | Enable or completely disable the buying of new trades during upwards trends.<br> **Datatype:** Boolean |
| **sell_trades_when_downwards** | Enable or completely disable the selling of open trades (through normal sell signals) during downwards trends.<br> **Datatype:** Boolean |
| **sell_trades_when_sideways** | Enable or completely disable the selling of open trades (through normal sell signals) during sideways trends.<br> **Datatype:** Boolean |
| **sell_trades_when_upwards** | Enable or completely disable the selling of open trades (through normal sell signals) during upwards trends.<br> **Datatype:** Boolean |

### Weighted Signal Spaces
The settings inside `mgm-config.json`'s `weighted_signal_spaces` section are used to control how MGM handles the HyperOpting of (Total) Weighted Signal Values during it's [optimization process](#how-to-optimize-monigomani).   

| Parameter | Description |
| --- | --- |
| **sell_profit_only** | If set to `true`, then weighted sell signals require to be profitable to go through.<br> **Datatype:** Boolean |
| **min_weighted_signal_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for weighted signals. <br> **2nd HyperOpt Run:** Weak weighted signals are weeded out by overriding them to their respective Minimal value. <br> **Datatype:** Integer |
| **max_weighted_signal_value** | **1st HyperOpt Run:** Maximum value used in the HyperOpt Space for weighted signals. <br> **2nd HyperOpt Run:** Strong weighted signals are boosted by overriding them to their respective Maximum value. <br> **Datatype:** Integer |
| **min_trend_total_signal_needed_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for total weighted signals needed. <br> **Datatype:** Integer |
| **min_trend_total_signal_needed_candles_lookback_window_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for the candle lookback window for total signals needed. <br> **Datatype:** Integer |
| **max_trend_total_signal_needed_candles_lookback_window_value** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for the candle lookback window for total signals needed. <br> **Datatype:** Integer |
| **min_trend_signal_triggers_needed** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for the amount of signals that need to trigger in it's respective (trend depending) candle lookback window.<br> **Datatype:** Integer |
| **search_threshold_weighted_signal_values** | **2nd HyperOpt Run:** Used to refine the search spaces for remaining weighted signals with the value found in the 1st run +- the threshold. <br> **Datatype:** Integer |
| **search_threshold_trend_total_signal_needed_candles_lookback_window_value** | **2nd HyperOpt Run:** Used to refine the search spaces for the candle lookback window for total signals needed with the values found in the 1st run +- the threshold. <br> **Datatype:** Integer |
| **search_threshold_trend_signal_triggers_needed** | **2nd HyperOpt Run:** Used to refine the search spaces for the amount of signals that need to trigger in it's respective (trend depending) candle lookback window. with the value found in the 1st run +- the threshold. <br> **Datatype:** Integer |

### Stoploss Spaces
The settings inside `mgm-config.json`'s `stoploss_spaces` section are used to refine the search spaces that MGM will use for the (trailing) stoploss during it's [optimization process](#how-to-optimize-monigomani).

| Parameter | Description |
| --- | --- |
| **stoploss_min_value** | Minimal value used in the HyperOpt Space for the `stoploss`.<br> **Datatype:** Decimal |
| **stoploss_max_value** | Maximum value used in the HyperOpt Space for the `stoploss`.<br> **Datatype:** Decimal |
| **trailing_stop_positive_min_value** | Minimal value used in the HyperOpt Space for the `trailing_stop_positive`.<br> **Datatype:** Decimal |
| **trailing_stop_positive_max_value** | Maximum value used in the HyperOpt Space for the `trailing_stop_positive`.<br> **Datatype:** Decimal |
| **trailing_stop_positive_offset_min_value** | Minimal value used for the intermediate offset parameter used to calculate the HyperOpt Space for the `trailing_stop_positive_offset`.<br> **Datatype:** Decimal |
| **trailing_stop_positive_offset_max_value** | Maximum value used for the intermediate offset parameter used to calculate the HyperOpt Space for the `trailing_stop_positive_offset`.<br> **Datatype:** Decimal |

### Open Trade Unclogger
When the Open Trade Unclogger is enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades.   
This `custom_sell()` function should be able to work in tandem with `Trailing stoploss`.   

It will only unclog a losing trade when all following checks have been full-filled (If a check is set to `0` it will be taken out of the equation, thus the unclogger will continue checking further without it):    
- Check if there is no `buy` or `sell` signal already occurring on the current candle.
- Check if `sell___unclogger_enabled` is `True`, otherwise abort further unclogger logic.
- Check if there are any open trades
- Check if the current pair isn't cooling down under it's `sell___unclogger_buy_cooldown_minutes_window`
- Check if everything in custom_storage is up to date with all_open_trades
- Check if there are enough losing trades open to fulfil `sell___unclogger_minimal_losing_trades_open`
- Check if there is a losing trade open for the pair currently being run through the MoniGoMani loop
- Check if trade has been open for `sell___unclogger_minimal_losing_trade_duration_minutes` (long enough to give it a recovery chance)
- Check if `sell___unclogger_open_trades_losing_percentage_needed` is fulfilled
- Check if the current detected trend is flagged as "bad" (aka `sell___unclogger_trend_lookback_window_uses_downwards/sideways/upwards_candles=True`)
- Check if open_trade's trend changed negatively during past `sell___unclogger_trend_lookback_candles_window`:   
For unclogging to occur `sell___unclogger_trend_lookback_candles_window_percentage_needed` should be fulfilled!   
The trends used for the calculations in this check can be configured with `sell___unclogger_trend_lookback_window_uses_downwards/sideways/upwards_candles=True/False`).   
Each candle fulfilling a trend set to `True` will be added in the sum used to calculate the value for `sell___unclogger_trend_lookback_candles_window_percentage_needed` if it is found in the lookback window.   

The settings inside `mgm-config.json`'s `unclogger_spaces` section are used to configure the Open Trade Unclogger:
| Parameter | Description |
| --- | --- |
| **unclogger_enabled** | Enable or completely disable the open trade unclogger.<br> **Datatype:** Boolean |
| **unclogger_buy_cooldown_minutes_window** | Settings to configure the HyperOpt Space for the minimal duration needed (in minutes) before MGM is allowed to buy recently unclogged pairs again.<br> **Documentation:** [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries) <br> **Datatype:** Dictionary |
| **unclogger_minimal_losing_trade_duration_minutes** | Settings to configure the HyperOpt Space for the minimal duration needed (in minutes) before the unclogger is allowed to attempt to unclog the open trade. <br> **Documentation:** [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries) <br> **Datatype:** Dictionary |
| **unclogger_minimal_losing_trades_open** | Settings to configure the HyperOpt Space for the minimal losing trades open before the unclogger is allowed to attempt to unclog the open trade.<br> **Documentation:** [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries) <br> **Datatype:** Dictionary |
| **unclogger_open_trades_losing_percentage_needed** | Settings to configure the HyperOpt Space for the minimal percentage of losing open trades before the unclogger is allowed to attempt to unclog the open trade.<br> **Documentation:** [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries) <br> **Datatype:** Dictionary |
| **unclogger_trend_lookback_candles_window** | Settings to configure the HyperOpt Space for the lookback window use by the `unclogger_trend_lookback_candles_window_percentage_needed` check.<br> **Documentation:** [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries) <br> **Datatype:** Dictionary |
| **unclogger_trend_lookback_candles_window_percentage_needed** | Settings to configure the HyperOpt Space for the minimal percentage of **bad** trends that needs to be detected inside the lookback window before the unclogger is allowed to attempt to unclog the open trade.<br> **Documentation:** [Unclogger Sub Dictionaries](#unclogger-sub-dictionaries) <br> **Datatype:** Dictionary |
| **unclogger_trend_lookback_window_uses_downwards_candles** | Enable or completely disable the open trade unclogger from seeing downwards trends as **bad** in it's lookback window.<br> **Datatype:** Boolean (true = bad) |
| **unclogger_trend_lookback_window_uses_sideways_candles** | Enable or completely disable the open trade unclogger from seeing sideways trends as **bad** in it's lookback window.<br> **Datatype:** Boolean (true = bad) |
| **unclogger_trend_lookback_window_uses_upwards_candles** | Enable or completely :sparkles: Added hyperoptable unclogger_buy_cooldown_minutes_windowdisable the open trade unclogger from seeing upwards trends as **bad** in it's lookback window.<br> **Datatype:** Boolean (true = bad) |

#### Unclogger Sub Dictionaries
| Parameter | Description |
| --- | --- |
| **min** | **1st HyperOpt Run:** Minimal value used in the HyperOpt Space for the unclogger setting at hand. <br> **2nd HyperOpt Run:** Value remains unused and refined search spaces are applied based on the value loaded from `mgm-config-hyperopt.json`.<br> **Datatype:** Integer |
| **max** | **1st HyperOpt Run:** Maximum value used in the HyperOpt Space for the unclogger setting at hand. <br> **2nd HyperOpt Run:** Value remains unused and refined search spaces are applied based on the value loaded from `mgm-config-hyperopt.json`.<br> **Datatype:** Integer |
| **threshold** | ***(Optional parameter)*** 2nd HyperOpt Run:** If this setting is found, then it's used to refine the search spaces based on the value found in the 1st run ± the threshold. If no custom `threshold` is provided then the `search_threshold_weighted_signal_values` is used instead.<br> **Datatype:** Integer |

### Default Stub Values
The settings inside `mgm-config.json`'s `default_stub_values` section are **only used** to control some default startup values that MGM will use when no other values are found and/or used for them.   
*(These would be used when not HyperOpting `--spaces all` in one go and/or during the initialization of MGM's variables in the 1st HyperOpt Run)*
| Parameter | Description |
| --- | --- |
| **minimal_roi** | **Official Freqtrade Documentation:** [Understand minimal_roi](https://www.freqtrade.io/en/latest/configuration/#understand-minimal_roi) <br> **Datatype:** Dictionary |
| **stoploss** | **Official Freqtrade Documentation:** [Stop Loss](https://www.freqtrade.io/en/latest/stoploss/#stop-loss) <br> **Datatype:** Decimal |
| **trailing_stop** | **Official Freqtrade Documentation:** [Trailing Stop Loss](https://www.freqtrade.io/en/latest/stoploss/#trailing-stop-loss) <br> **Datatype:** Boolean |
| **trailing_stop_positive** | **Official Freqtrade Documentation:** [Trailing stop loss, custom positive loss](https://www.freqtrade.io/en/latest/stoploss/#trailing-stop-loss-custom-positive-loss) <br> **Datatype:** Decimal |
| **trailing_stop_positive_offset** | **Official Freqtrade Documentation:** [Trailing stop loss only once the trade has reached a certain offset](https://www.freqtrade.io/en/latest/stoploss/#trailing-stop-loss-only-once-the-trade-has-reached-a-certain-offset) <br> **Datatype:** Decimal |
| **trailing_only_offset_is_reached** | **Official Freqtrade Documentation:** [Trailing stop loss only once the trade has reached a certain offset](https://www.freqtrade.io/en/latest/stoploss/#trailing-stop-loss-only-once-the-trade-has-reached-a-certain-offset) <br> **Datatype:** Boolean |


## mgm-config-hyperopt.json
This file contains the optimized HyperOptable `MoniGoMani` and `Freqtrade` settings. It will be created when following the [How to Optimize MoniGoMani](#how-to-optimize-monigomani) process and its one of the main files that will define your MGM configuration when moving to dry/live-run mode.   

It's truly **important** that you reflect over these files in between HyperOpt Runs.

### Reflect over HyperOpt Results
Please read [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/) to learn about the common traps that can occur in your HyperOpt results.

Further you want to confirm that your total signals needed are reasonable/possible.
The sum of all weighted buy/sell signals found in a trend should always be bigger then the respective total signal needed!

Following equation should always be true:

#### Bad Weighted signal setup example
**Way too low total needed:**   
Imagine following configuration for `buy` on `upwards` trends:
```json
{
    "buy__upwards_trend_total_signal_needed": "33",
    "buy__upwards_trend_total_signal_needed_candles_lookback_window": "2",
    "buy_upwards_trend_adx_strong_up_weight": "79",
    "buy_upwards_trend_bollinger_bands_weight": "97",
    "buy_upwards_trend_ema_long_golden_cross_weight": "74",
    "buy_upwards_trend_ema_short_golden_cross_weight": "91",
    "buy_upwards_trend_macd_weight": "53",
    "buy_upwards_trend_rsi_weight": "17",
    "buy_upwards_trend_sma_long_golden_cross_weight": "32",
    "buy_upwards_trend_sma_short_golden_cross_weight": "100",
    "buy_upwards_trend_vwap_cross_weight": "58"
}
```
Here we are working with a lookback window of 2 candles, this means that all signals counting up for the total needed may occur in the current candle and the candle before that, but each signal is only allowed to fire off once.

If we calculate the sum of all weighted signals, we will see that its way above te total signal needed! Meaning that this MGM configuration will probably try to buy too much candles than need during this trend.

Sum of all weighted signals:
`79 + 97 + 74 + 91 + 53 + 17 + 32 + 100 + 58 = 601`

## MoniGoManiHyperStrategy
This is the main strategy file used by MoniGoMani, containing the [Weighted Signal Interface](#weighted-signal-interface).

**Link to:** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py)

### Weighted Signal Interface
With this you can easily define new indicators and weighted signals that will be used by MGM.   
A different amount of buy and sell signals is possible, and the initial search spaces will automatically be adjusted towards the detected amount.
*(We'll only use RSI and MACD in below examples to keep things simple)*

#### Defining Indicators Examples
First add the technical analysis indicators you wish to use to MGM's `do_populate_indicators()` function.   

Check out these **+200 Easy to implement Indicators** for toying with the Weighted Signal Interface:
- [Freqtrade Technical](https://github.com/freqtrade/technical)
- [TA-Lib](https://mrjbq7.github.io/ta-lib/funcs.html)
- [Pandas-TA](https://twopirllc.github.io/pandas-ta)
- [Hacks for Life Blog](https://hacks-for-life.blogspot.com)

But feel free to look for other means of implementing indicators too.

```python
def do_populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Generate all indicators used by MoniGoMani
    """
    # MACD - Moving Average Convergence Divergence
    macd = ta.MACD(dataframe)
    dataframe['macd'] = macd['macd']  # MACD - Blue TradingView Line (Bullish if on top)
    dataframe['macdsignal'] = macd['macdsignal']  # Signal - Orange TradingView Line (Bearish if on top)

    # RSI - Relative Strength Index (Under bought / Over sold & Over bought / Under sold indicator Indicator)
    dataframe['rsi'] = ta.RSI(dataframe)

    return dataframe
```

#### Defining Weighted Buy & Sell Signals Examples
Secondly define the Weighted signal conditions you wish to use in MGM's `buy_signals` and `sell_signals` dictionaries by using the names of the indicators you just defined in the examples above.
```python
# Define the Weighted Buy Signals to be used by MGM
buy_signals = {
    # Weighted Buy Signal: MACD above Signal
    'macd': lambda df: (df['macd'] > df['macdsignal']),
    # Weighted Buy Signal: RSI crosses above 30 (Under-bought / low-price and rising indication)
    'rsi': lambda df: (qtpylib.crossed_above(df['rsi'], 30))
}

# Define the Weighted Sell Signals to be used by MGM
sell_signals = {
    # Weighted Sell Signal: MACD below Signal
    'macd': lambda df: (df['macd'] < df['macdsignal']),
    # Weighted Sell Signal: RSI crosses below 70 (Over-bought / high-price and dropping indication)
    'rsi': lambda df: (qtpylib.crossed_below(df['rsi'], 70))
}
```

#### Visualize Weighted Signals in FreqUI
Finally you can easily define your freshly implemented indicators inside the `plot_config` dictionary for visualization in FreqUI. Then you can easily read when which weighted signals triggered.
```python
plot_config = {
        'main_plot': {
            # Add indicators here which you'd like to see in the main graph
        },
        'subplots': {
            # Subplots - Each dict defines one additional plot (MACD, ADX, Plus/Minus Direction, RSI)
            'MACD (Moving Average Convergence Divergence)': {
                'macd': {'color': '#19038a'},
                'macdsignal': {'color': '#ae231c'}
            },
            'RSI (Relative Strength Index)': {
                'rsi': {'color': '#7fba3c'}
            }
        }
}
```
For more documentation about defining these see the **Official Freqtrade Documentation:** [Advanced Plot Configuration](https://www.freqtrade.io/en/latest/plotting/#advanced-plot-configuration)


Once you defined them you can load them in FreqUI as following:
1) Click the cog-wheel at the right top   
   ![Click the cog-wheel at the right top](https://i.imgur.com/VDeCFDT.png)
2) Click `Load from strategy`   
   ![Click Load from strategy](https://i.imgur.com/dOvHGdq.png)
3) Give it a name (like `MoniGoManiPlot`) Click `Save`   
   ![Give it a name (like MoniGoManiPlot) Click Save](https://i.imgur.com/Rk30ARC.png)
4) Now you will be able to select and view your saved plot in FreqUI! *(Individual indicators can be toggled on/off by clicking on them in the header on top)*   
   ![Final Result](https://i.imgur.com/Q5zfnk2.png)


# Total Overall Signal Importance Calculator
Execute: `python ./user_data/mgm_tools/TotalOverallSignalImportanceCalculator.py` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better! It will also export to a `./user_data/Total-Average-Signal-Importance-Report.log` file for easy sharing!   
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals!   

The calculator file also has 2 settings you can configure marked under the `CONFIG NAMES SECTION` section inside the file:
    - **mgm_config_name**: Provide a custom file name for `mgm-config.json`
    -  **mgm_config_hyperopt_name**: Provide a custom file name for `mgm-config-hyperopt.json`

### Handy Calculator Sub Commands
- `-h` or `--help`: Print out information about the usage of all sub commands.
- `-pu` or `--precision-used` ***Optional (Defaults to `1` when not omitted)***: The precision value used during HyperOpt. Can be decimal (0.2) or fraction 1/5. Mostly useful after a running a HyperOpt with precision different from 1, used to patch the weights of the signals displayed in the report to what we would expect them to be for comparison with other results.
- `-cf` or `--create-file` ***Optional (Unused by default)***: Save the Total-Average-Signal-Importance-Report as a `.log` file with a custom filename and file output location   
- `-nf` or `--no-file` ***Optional (Defaults to `True` when not omitted)***: Do not output the Total-Average-Signal-Importance-Report as a `.log` file


# Custom HyperLoss Functions
MoniGoMani comes with an extra set of loss functions for HyperOpting, supplementing the ones shipped with FreqTrade.
You can find these functions in `M̀oniGoMani/user_data/hyperopts/`, and can use them by overriding the freqtrade HyperOpt parameter `--hyperopt-loss`.   
   
Following 2 Custom HyperLoss Functions ship with the MoniGoMani Framework:
- [**WinRatioAndProfitRatioLoss**](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/WinRatioAndProfitRatioLoss.py): Attempts to optimise for the best profit **and** stability (Returns smaller number for better results)   
- [**UncloggedWinRatioAndProfitRatioLoss**](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/UncloggedWinRatioAndProfitRatioLoss.py): Same as WinRatioAndProfitRatioLoss but has a configurable Percentage of loss (See `unclogger_profit_ratio_loss_tolerance` setting inside the file) to ignore while HyperOpting (Since small losses are a by-product of the Unclogger)
   
**Example Usage:**
```powershell
--hyperopt-loss WinRatioAndProfitRatioLoss
```


# PairLists
By default, MoniGoMani includes 2 pairlists in `mgm-config.json`:   
- A VolumePairList: 
    - Best to use for Dry and Live Running
    - Will automatically update to the current best top volume coin pairs available
- A StaticPairList: 
    - Used for BackTesting / HyperOpting since a VolumePairList cannot be used here.
    - When [optimizing](#how-to-optimize-monigomani) MoniGoMani for actual Dry/Live-running (instead of testing) it's truly recommended to [download a fresh top volume StaticPairList](#download-staticpairlists) and HyperOpt upon that (Preferably as big as possible, but beware of the warning below)!   
    This should yield much better & more realistic results during HyperOpting/BackTesting!   
    This is due to giving a better reflection of the current market and being closer to the VolumePairList used during Dry/Live-run's.

Switching between the PairList in use can easily be done by moving the `_` in front of the `pairlists` value inside `mgm-config.json` for the pairlist you wish to disable.

**<span style="color:darkorange">WARNING:</span> The bigger the (Volume/Static)PairList in use the higher the system requirements (CPU usage, RAM usage & Time needed to HyperOpt will go up)! Switch to a smaller list if your system can't handle it!**   

### Enabled StaticPairList / Disabled VolumePairList Example
```json
"pairlists": [{
        "method": "StaticPairList"
    }],
"_pairlists": [
    {
        "method": "VolumePairList",
```

### Download StaticPairLists
Retrieve and apply a current **Binance-USDT-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))* (The amount of pairs in these top volume lists can be altered by opening up `Binance-Retrieve-Top-Volume-StaticPairList.json` and changing the `number_assets` value near the bottom of the file to the amount of pairs you'd like in your list. Further you can also change the `min_days_listed` to make sure that all downloaded pairs where available for the duration of your whole HyperOpt timerange):
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote USDT --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json && jq 'del(.exchange.pair_whitelist )' ./user_data/mgm-config.json > ./tmp.json && jq -s '.[0] * .[1]' ./tmp.json ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json > ./user_data/mgm-config.json && rm ./tmp.json && jq '.' ./user_data/mgm-config.json
```

Retrieve and apply a current **Binance-USDT-All-Tradable-StaticPairList.json** file *(using [Binance-Retrieve-All-Tradable-StaticPairList.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-All-Tradable-StaticPairList.py))* (Beware, can be very high system requirements due to a lot of pairs!):
```powershell
python ./user_data/mgm_tools/Binance-Retrieve-All-Tradable-StaticPairList.py -q USDT | jq '.|{exchange: { pair_whitelist: . }}' > ./user_data/mgm_pair_lists/Binance-USDT-All-Tradable-StaticPairList.json && jq 'del(.exchange.pair_whitelist )' ./user_data/mgm-config.json > ./tmp.json && jq -s '.[0] * .[1]' ./tmp.json ./user_data/mgm_pair_lists/Binance-USDT-All-Tradable-StaticPairList.json > ./user_data/mgm-config.json && rm ./tmp.json && jq '.' ./user_data/mgm-config.json
```

**After Downloading** the StaticPairList automatically applied to `./user_data/mgm-config.json`. There will also be a copy available under `./user_data/mgm_pair_lists/<<NAME_HERE>>-StaticPairList.json`!   

Don't forget to **Download Candle Data** before HyperOpting or BackTesting (Example timerange):   
```powershell
freqtrade download-data --timerange 20201201-20210316 -t 5m 1h -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json
```

# Go-To Commands
**Hyper Opting** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) & Apply *"best"* HyperOpt Results:
```powershell
freqtrade hyperopt -s MoniGoManiHyperStrategy -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --hyperopt-loss WinRatioAndProfitRatioLoss --spaces all -e 1000 --timerange 20210501-20210616 --enable-protections && mv ./user_data/strategies/MoniGoManiHyperStrategy.json ./user_data/mgm-config-hyperopt.json
```
**View & Apply HyperOpt Results** from a trusted `<epoch of choice>`:
```powershell
freqtrade hyperopt-show -n <epoch of choice> -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json && mv ./user_data/strategies/MoniGoManiHyperStrategy.json ./user_data/mgm-config-hyperopt.json
```
**Reset HyperOpt Results**:
```powershell
rm ./user_data/mgm-config-hyperopt.json ./user_data/strategies/MoniGoManiHyperStrategy.json
```
**Back Testing** [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py):
```powershell
freqtrade backtesting -s MoniGoManiHyperStrategy -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --timerange 20210501-20210616 --enable-protections
```
**Total Average Signal Importance Calculation** *(with the [TotalOverallSignalImportanceCalculator.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/TotalOverallSignalImportanceCalculator.py))*:
```powershell
python ./user_data/mgm_tools/TotalOverallSignalImportanceCalculator.py
```
Retrieve and apply a current **Binance-Top-Volume-StaticPairList.json** file *(using [Binance-Retrieve-Top-Volume-StaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json))*:
```powershell
freqtrade test-pairlist -c ./user_data/mgm_tools/Binance-Retrieve-Top-Volume-StaticPairList.json --quote USDT --print-json | tail -n 1 | jq '.|{exchange: { pair_whitelist: .}}' > ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json && jq 'del(.exchange.pair_whitelist )' ./user_data/mgm-config.json > ./tmp.json && jq -s '.[0] * .[1]' ./tmp.json ./user_data/mgm_pair_lists/Binance-USDT-Top-Volume-StaticPairList.json > ./user_data/mgm-config.json && rm ./tmp.json && jq '.' ./user_data/mgm-config.json
```
**Download Candle Data**:
```powershell
freqtrade download-data --timerange 20210414-20210618 -t 5m 30m -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json
```

**Plot-Profits** from a `<backtest-results-file>`:
```powershell
freqtrade plot-profit --export-filename ./user_data/backtest_results/<backtest-results-file> -c ./user_data/mgm-config.json -c ./user_data/mgm-config-private.json --timerange 20210501-20210616 --timeframe 1h
```

# How to test for improvements
The process is rather simple really on **1st HyperOpt Runs**:
- Copy/paste the Run 1 command
- Check/Save the HyperOpt Run 1a Results
- Reset MoniGoMani
- Adjust a single:
  - Setting in `mgm-config.json`
  - Indicator/weighted signal
  - The spaces used
  - The protections enabled/disabled
  - ...
- Copy/paste the Run 1 command again, use the same `--random-state` as you used in the previous test
- Compare if the HyperOpt Run 1b Results are better then on your Run 1a attempt

You can also do this for  **2nd HyperOpt Runs**, but this is a little more difficult, after your 1st Run be sure to:
- Check/Save the HyperOpt Run 1 Results, Copy/paste the Run 2 command upon an epoch of choice and with a new random state
- Check/Save the HyperOpt Run 2a Results
- Reset MoniGoMani
- Restore your initial 1st Run with `hyperopt-show` with the correct epoch and `--hyperopt-filename`
- Adjust a single:
  - Setting in `mgm-config.json`
  - Indicator/weighted signal
  - The spaces used
  - The protections enabled/disabled
  - ...
- Copy/paste the Run 2 command again, use the same `--random-state` as you used in the previous test
- Compare if the HyperOpt Run 2b Results are better then on your Run 2a attempt

# How to share your test results properly
The easiest way to share how your MGM setup has been doing would be by posting a screenshot in the [Discord Server](https://discord.gg/xFZ9bB6vEz) with the output of the `/status table` and `/profit` commands (Using the Telegram connection of the bot) + The complete output of the log being printed while HyperOpting (See [Some Test Results]() for examples).   
   
Also, one of the other most welcome things is the results from the `TotalOverallSignalImportanceCalculator`, but you'll have to paste your own fresh HyperOpt results in it first before it can make you a nice report that can help us find better signals for MGM !:rocket:   

Of course all FreqUI / Telegram / config / HyperOpt results done on MGM **can be** useful / be learned from!
Try to **always include** a  `TotalOverallSignalImportanceCalculator` report or just your own MoniGoMani file with your HyperOpt results applied to it!   
Since without knowing which signal weights or which on/off settings are applied we can't really truly learn much from your results!   

The epoch table being generated when HyperOpting + the number of the epoch you used is also very helpful, so we can easily rule out if your test results are exploited. (See [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/)!)   

# Common mistakes

### HyperOpting: +300 epochs, no results yet
Make sure you have [downloaded the candle data](#download-staticpairlists) needed for your HyperOpt.

This is also possible because of how MoniGoMani handles the automatic filtering of total signals needed that would be impossible too reach during HyperOpt. If MGM detects impossible too reach signals then it forces the bot to do nothing for that epoch.

Because of this reason it's normal that you can have 200-300 epochs without a result.
However if after 300-400 epochs you still get nothing, then its recommended to stop your HyperOpt and start a clean new one on another random state.

### TypeError: integer argument expected, got float
You likely are using a `Float` value where you should be using a `Integer` value. Hopefully your error will show more information about which Parameter.   
- `Integer` = Whole number. Examples: 1, 3, 23
- `Float` = Decimal number. Examples: 1.53, 4.2, 17.12   

### -bash: jq: command not found
You still need to install [jq](https://stedolan.github.io/jq/)

### ValueError: the lower bound X has to be less than the upper bound Y
You probably ran with precision different from 1. If so then you need to run your 1st HO Run results through the calculator with `-pu` or `--precision-used` and then fix up your `mgm-config-hyperopt.json` with the adjusted results before firing up the 2nd HO Run.   

Check out the documentation for the [Precision Setting](#precision-setting) and the [Total Overall Signal Importance Calculator](#total-overall-signal-importance-calculator)!
