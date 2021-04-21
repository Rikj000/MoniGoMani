```
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.9.0 by Rikj000                         ###
    ##                          ----------------------------                          ##
    #               Isn't that what we all want? Our money to go many?                 #
    #          Well that's what this Freqtrade strategy hopes to do for you!           #
    ##       By giving you/HyperOpt a lot of signals to alter the weight from         ##
    ###           ------------------------------------------------------             ###
    ##        Big thank you to xmatthias and everyone who helped on MoniGoMani,       ##
    ##      Freqtrade Discord support was also really helpful so thank you too!       ##
    ###         -------------------------------------------------------              ###
    ##              Disclaimer: This strategy is under development.                   ##
    #      I do not recommend running it live until further development/testing.       #
    ##                      TEST IT BEFORE USING IT!                                  ##
    ###                                                              ▄▄█▀▀▀▀▀█▄▄     ###
    ##               -------------------------------------         ▄█▀  ▄ ▄    ▀█▄    ##
    ###   If you like my work, feel free to donate or use one of   █   ▀█▀▀▀▀▄   █   ###
    ##   my referral links, that would also greatly be appreciated █    █▄▄▄▄▀   █    ##
    #     ICONOMI: https://www.iconomi.com/register?ref=JdFzz      █    █    █   █     #
    ##  Binance: https://www.binance.com/en/register?ref=97611461  ▀█▄ ▀▀█▀█▀  ▄█▀    ##
    ###          BTC: 19LL2LCMZo4bHJgy15q1Z1bfe7mV4bfoWK             ▀▀█▄▄▄▄▄█▀▀     ###
    ####                                                                            ####
    ####################################################################################
```

**<span style="color:darkorange">WARNING:</span> MoniGoManiHyperStrategy should always be HyperOpted unless you really know what you are doing when manually allocating weights!**   
**MoniGoManiHyperStrategy found in releases already has a decent hyperopt applied to it for BTC pairs!**   
**When changing anything in one of the `config.json`'s please [re-optimize](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani)!**   

# **Current `MoniGoMani` status @ `v0.9.0`**   
      
## The idea / Theory:   
MoniGoMani derives iteself from other strategies by it's use of something I called "weighted signals".   
Each signal has it's own weight allocated to it & a total buy/sell signal needed is defined too.   
MGM (MoniGoMani) will loop through all signals, if they trigger it will add up the weight and eventually it will check if it's bigger then what's needed in total, if it is it will buy/sell.   
The beauty lies in using MGM in combination with hyperopting (= a form of machine learning where you backtest a timeframe a lot of times to find the most ideal values), since all weighted signals have been made hyperoptable it can be used to find the most "ideal" weight divisions.   
Also will it teach us what works where & what doesn't since MoniGoMani first detects Downwards/Sideways/Upwards trends and then does all of the above individually for each kind of trend (Creating basically 3 individual strategies, 1 for each kind of trend).   
Further it will do various hyperoptable checks upon the open trades to see if there are "bad" ones to unclog while running.   


## Feature List:   
- [Auto-HyperOptable Strategy](https://github.com/freqtrade/freqtrade/pull/4596)! \*No more need for legacy MoniGoMani, legacy MoniGoManiHyperOpt and MoniGoManiHyperOpted strategy classes!   
- All HyperOptable settings are \*\*easily copy/paste-able from the HyperOpt Results
- Configurable Buy/Sell Signal Weight Influence Tables for Downwards/Sideways/Upwards trends, each table **currently** has 9 Buy & 9 Sell signals implemented ***(HyperOptable!)***:
  - ADX + Strong Up/Strong Down
  - RSI
  - MACD
  - SMA Short Death/Golden Cross 
  - EMA Short Death/Golden Cross 
  - SMA Long Death/Golden Cross 
  - EMA Long Death/Golden Cross 
  - Bollinger Band Re-Entrance
  - VWAP Cross
- Configurable Total Buy/Sell Signal Percentages for Downwards/Sideways/Upwards trends ***(HyperOptable!)***
- Configurable Trading on Downwards/Sideways/Upwards trends for Buys/Sells ***(HyperOptable!)***
- Settings to Enable/Disable HyperOpting for individual `buy_params` & `sell_params` and setting them to a static value through [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)
- Configurable [Open Trade Unclogger](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#open-trade-unclogger), if enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades ***(HyperOptable!)*** :rocket:   
- [TimeFrame-Zoom](MoniGoMani/blob/main/VERYQUICKSTART.md#timeframe-zoom) during backtesting/hyperopting to prevent profit exploitation! *(Read: [Backtesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/))*
- [Precision Setting](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#precision-setting) to alter the step-size used during HyperOpting
- [Total Overall Signal Importance Calculator](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#total-overall-signal-importance-calculator) for Total Average Signal Importance Calculation upon the HyperOpt Results (With some really handy subcommands)
- Pre-Configured Main/Sub Plot Configurations for visualisation of all indicators used in FreqUI
- Turn On/Off **All** Individual Weighted Signal DataFrame entries for easy debugging in an IDE or better speed while dry/live running or hyperopting   
   
*\*Support/Updates for Legacy versions stopped since Auto-HyperOptable Strategies are merged into the official Freqtrade Development Branch! Please switch to the new MoniGoManiHyperStrategy!*   
*\*\*If you set up overrides then currently these will be missing from hyperopts results! Please add these back in manually to prevent unexpected behaviour!*   

## Go-To Commands:
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
For Hyper Opting *(the legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/strategies/MoniGoMani.py) + legacy [MoniGoManiHyperOpt.py](https://github.com/Rikj000/MoniGoMani/blob/main/Legacy%20MoniGoMani/user_data/hyperopts/MoniGoManiHyperOpt.py))*:
```powershell
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all --hyperopt MoniGoManiHyperOpt -s MoniGoMani -e 1000 --timerange 20210101-20210316
```

## **Planned**:   
*Ordered by current schedule/priority*
- Huge refactor that should improve the codebase reducing a lot of duplicate code & making implementing new weighted signals even easier
- Extract all `MoniGoMani Settings` into a `config-mgm.json` that will require manual configuration + Extract the `HyperOpt Results Copy/Paste section` into a `config-mgm-hyperopt.json`, this last file will be extractable from hyperopts results using a command!
- Improve upon bot loop speed (Try to improve code to reach reduction in HyperOpting time needed)
- **Other & Better indicators!** MoniGoMani has been designed so signals can easily be inserted / swapped out   
Please use the `Total-Overall-Signal-Importance-Calculator.py` (added in `v0.7.1`) to find out which signals do best and report your results to the Discord server, so we can improve! :rocket:
- Update the `Total-Overall-Signal-Importance-Calculator.py` to show UnClogger hyperoptable variable results   
- Hyperopt over 3 separate timeranges (one representing each individual kind of trend, downwards/sideways/upwards, a timeframe that represents a corresponding trend should be picked)
- Individual `config-btc.json` & `config-usdt.json` files, as well as individual `MoniGoManiHyperOpted-btc.py` & `MoniGoManiHyperOpted.py` releases
- A method to pull a `Static Averaged Volume PairList` (Calculated by summing up the top volume pairlists for each candle over the period of the timerange to hyperopt upon & then dividing by the total amount of candles in the timerange, to create an averaged "volume" pairlist that can be used during backtesting/hyperopting which should lead to a more "realistic" pairlist to test upon when using a VolumePairList when dry/live-running)
- Automate as much of the [optimization process](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) of MoniGoMani as possible  
- HyperOpt over a `timerange` through a simple Telegram commands, review the results and choose if and which new epoch should be applied.   
- [MultiProcessed DataFrame indicator checking](https://www.machinelearningplus.com/python/parallel-processing-python/) if possible for speed improvements

## **ChangeLog**:  
View the Legacy [ChangeLog](https://github.com/Rikj000/MoniGoMani/blob/main/CHANGELOG.md), newer changelogs are appended with each [Release](https://github.com/Rikj000/MoniGoMani/releases/)

## **Got Test Results / Ideas / Config Improvements?**
- Feel free to join [**CryptoStonksShallRise**](https://discord.gg/xFZ9bB6vEz) on Discord there you can follow/participate in the Official MoniGoMani Channels:
  - `#moni-go-mani-updates`
  - `#moni-go-mani-testing`
  - `#moni-go-mani-help`
  - `#moni-go-mani-setup-releases`

## Need help getting started?
[View the VeryQuickStart](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md), the current place where you can find all MoniGoMani Documentation!   

## **Freqtrade**:   
**Freqtrade** is the well known `open source crypto day-trading bot` that makes this strategy possible!   
It's completely free to use and alter and has many amazing features.   
Big thank you to **xmatthias** and everyone who helped on it!   
- **[Official Freqtrade Website](https://www.freqtrade.io/en/latest/)**
- **[Official Freqtrade GitHub Repository](https://github.com/freqtrade/freqtrade)**
- **[Official Freqtrade Discord Server](https://discord.gg/j84KnP57kW)**


## **Iconomi**:   
Can't wait until MoniGoMani is fully on point? Or is this all too technical for you?   
Check out **[Iconomi](https://www.iconomi.com/register?ref=JdFzz)**! *(Please use this link if you would sign up)*   

More information about this platform can be found in the `#welcome` channel of **[CryptoStonksShallRise](https://discord.gg/xFZ9bB6vEz)** on Discord.