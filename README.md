# **Current `MoniGoMani` status @ `v0.9.1`**   
      
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

```
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.9.1 by Rikj000                         ###
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

**<span style="color:darkorange">WARNING:</span> I am in no way responsible for your live results! This strategy is still experimental and under development!**   
**<span style="color:darkorange">WARNING:</span> MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) unless you really know what you are doing when manually allocating parameters!**   
**I strongly recommended to [re-optimize](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!**   

## The idea / Theory:   
MoniGoMani is more a framework to "easily" find a profitable strategy configuration then just a conventional strategy!   
It derives itself from other strategies by its use of something I called "weighted signals".   
Each signal has its own weight allocated to it & a total buy/sell signal needed is defined too.   
MGM (MoniGoMani) will loop through all signals, if they trigger it will add up the weight and eventually it will check if it's bigger than what's needed in total, if it is it will buy/sell. The signals used here are implemented, so they can easily be changed by a developer to further improve upon them.   
   
The beauty lies in using MGM in combination with HyperOpting (= A form of machine learning where you BackTest a timerange a lot of times to find the most ideal values), since all weighted signals have been made HyperOptable it can be used to find the most "ideal" weight divisions.   
Also will it teach us what works where & what doesn't since MoniGoMani first detects Downwards/Sideways/Upwards trends and then does all the above individually for each kind of trend (Creating basically 3 individual strategies, 1 for each kind of trend).   
Further it will do various HyperOptable checks upon the open trades to see if there are "bad" ones to unclog while running.   

## Feature List:   
- [Auto-HyperOptable Strategy](https://github.com/freqtrade/freqtrade/pull/4596)! \*No more need for legacy MoniGoMani, legacy MoniGoManiHyperOpt and MoniGoManiHyperOpted strategy classes!   
- All HyperOptable settings are \*\*easily copy/paste-able from the HyperOpt Results
- Configurable Buy/Sell Signal Weight Influence Tables for Downwards/Sideways/Upwards trends, each table **currently** has 9 Buy & 9 Sell signals implemented ***(HyperOptable!)***:
  - [ADX](https://www.investopedia.com/terms/a/adx.asp) + Strong [Up](https://www.investopedia.com/terms/p/positivedirectionalindicator.asp)/Strong [Down](https://www.investopedia.com/terms/n/negativedirectionalindicator.asp)
  - [RSI](https://www.investopedia.com/terms/r/rsi.asp)
  - [MACD](https://www.investopedia.com/terms/m/macd.asp)
  - [SMA](https://www.investopedia.com/terms/s/sma.asp) Short [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross 
  - [EMA](https://www.investopedia.com/terms/e/ema.asp) Short [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross 
  - [SMA](https://www.investopedia.com/terms/s/sma.asp) Long [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross 
  - [EMA](https://www.investopedia.com/terms/e/ema.asp) Long [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross 
  - [Bollinger Band](https://www.investopedia.com/terms/b/bollingerbands.asp) Re-Entrance
  - [VWAP](https://www.investopedia.com/terms/v/vwap.asp) Cross
- Configurable Total Buy/Sell Signal Percentages for Downwards/Sideways/Upwards trends ***(HyperOptable!)***
- Configurable Trading on Downwards/Sideways/Upwards trends for Buys/Sells ***(HyperOptable!)***
- Settings to Enable/Disable HyperOpting for individual `buy_params` & `sell_params` and setting them to a static value through [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#hyperopt-setting-overrides)
- Configurable [Open Trade Unclogger](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#open-trade-unclogger), if enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades ***(HyperOptable!)*** :rocket:   
- [TimeFrame-Zoom](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#timeframe-zoom) during backtesting/hyperopting to prevent profit exploitation! *(Read: [Backtesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/))*
- [Precision Setting](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#precision-setting) to alter the step-size used during HyperOpting
- 2 [Custom HyperLoss Functions](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#custom-hyperloss-functions):
  - [WinRatioAndProfitRatioLoss](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/WinRatioAndProfitRatioLoss.py): Attempts to optimise for the best profit **and** stability (Returns smaller number for better results)   
  - [UncloggedWinRatioAndProfitRatioLoss](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/UncloggedWinRatioAndProfitRatioLoss.py): Same as WinRatioAndProfitRatioLoss but has a configurable Percentage of loss to ignore while HyperOpting (Small losses are a by-product of the Unclogger)
- [Top Volume & All Tradable StaticPairList Downloading](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#download-staticpairlists) to easily fetch a good StaticPairList
- [Total Overall Signal Importance Calculator](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#total-overall-signal-importance-calculator) for Total Average Signal Importance Calculation upon the HyperOpt Results (With some really handy subcommands)
- Pre-Configured Main/Sub Plot Configurations for visualisation of all indicators used in FreqUI
- Turn On/Off **All** Individual Weighted Signal DataFrame entries for easy debugging in an IDE or better speed while dry/live running or hyperopting   
   
*\*Support/Updates for Legacy versions stopped since Auto-HyperOptable Strategies are merged into the official Freqtrade Development Branch! Please switch to the new MoniGoManiHyperStrategy!*   
*\*\*If you set up overrides then currently these will be missing from HyperOpt Results! Please add these back in manually to prevent unexpected behaviour!*   

# Go-To Commands:
For Hyper Opting *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py))*:
```powershell
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss WinRatioAndProfitRatioLoss --spaces all -s MoniGoManiHyperStrategy -e 1000 --timerange 20210101-20210316
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
freqtrade hyperopt -c ./user_data/config-btc.json -c ./user_data/config-private.json --hyperopt-loss WinRatioAndProfitRatioLoss --spaces all --hyperopt MoniGoManiHyperOpt -s MoniGoMani -e 1000 --timerange 20210101-20210316
```

## **Planned**:   
*Ordered by current schedule/priority*
- Huge refactor that should improve the codebase reducing a lot of duplicate code & making implementing new weighted signals even easier
- Extract all `MoniGoMani Settings` into a `config-mgm.json` that will require manual configuration + Extract the `HyperOpt Results Copy/Paste section` into a `config-mgm-hyperopt.json`, this last file will be extractable from HyperOpt Results using a command!
- Improve upon bot loop speed (Try to improve code to reach reduction in HyperOpting time needed)
- Lookback candle window for weighted signals (As learned from a picture in [EmperorBTC's Trading Manual](https://drive.google.com/file/d/1W-9XUcTRc1Zerwi6D-ZYTVzRrVbXoVbG/view) a combination of different 6 signals triggering rapidly after another (but within a window of a few candles) lead to using a total buy/sell signal)
- **Other & Better indicators!** MoniGoMani has been designed so signals can easily be inserted / swapped out   
Please use the `Total-Overall-Signal-Importance-Calculator.py` to find out which signals do best and report your results to the [Discord Server](https://discord.gg/xFZ9bB6vEz), so we can improve! :rocket:
- HyperOpt over 3 separate timeranges (one representing each individual kind of trend, downwards/sideways/upwards, a timeframe that represents a corresponding trend should be picked)
- Individual `config-btc.json` & `config-usdt.json` files, as well as individual `MoniGoManiHyperOpted-btc.py` & `MoniGoManiHyperOpted.py` releases
- A method to pull a `Static Averaged Volume PairList` (Calculated by summing up the top volume pairlists for each candle over the period of the timerange to hyperopt upon & then dividing by the total amount of candles in the timerange, to create an averaged "volume" pairlist that can be used during backtesting/hyperopting which should lead to a more "realistic" pairlist to test upon when using a VolumePairList when dry/live-running)
- Automate as much of the [optimization process](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#how-to-optimize-monigomani) of MoniGoMani as possible  
- HyperOpt over a `timerange` through a few simple Telegram commands, review the results and choose if and which new epoch should be applied.   
- [MultiProcessed DataFrame indicator checking](https://www.machinelearningplus.com/python/parallel-processing-python/) if possible for speed improvements

## **ChangeLog**:  
View the Legacy [ChangeLog](https://github.com/Rikj000/MoniGoMani/blob/main/CHANGELOG.md), newer changelogs are appended with each [Release](https://github.com/Rikj000/MoniGoMani/releases/)

## **Got Test Results / Ideas / Config Improvements?**
- Feel free to join our community [**CryptoStonksShallRise**](https://discord.gg/xFZ9bB6vEz) on Discord, there you can follow/participate in the **Official MoniGoMani Channels**:
  - `#moni-go-mani-announcements`
  - `#moni-go-mani-development` *(Only available to MoniGoMani Developers!)*
  - `#moni-go-mani-updates`
  - `#moni-go-mani-testing`
  - `#moni-go-mani-help` *(Be sure to take your time to read the [Documentation](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md) thoroughly before asking questions though!)*
  - `#moni-go-mani-cluster-releases` *(Only available to the MoniGoMani Cluster Maintainer & MoniGoMani Developers, for now!)*
  - `#moni-go-mani-setup-releases`

## Need help getting started?
[View the VeryQuickStart](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md), the current place where you can find all MoniGoMani Documentation!   
   
More general chats for `Technical Analysis`, `Freqtrade`, `Iconomi` and `Random` discussion are also available there :slight_smile:   
   
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