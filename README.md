# **Current `MoniGoMani` status @ `v0.11.0`**   
      
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
    ###                         MoniGoMani v0.11.0 by Rikj000                        ###
    ##                          -----------------------------                         ##
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
**<span style="color:darkorange">WARNING:</span> MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) after doing manual changes!**   
**You need to [optimize](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!**   

## The idea / Theory:   
MoniGoMani aims to be more than just a conventional strategy, it's a framework to "easily" find a profitable strategy configuration in any market! Without the need to do any programming.   
However, you will need to know some Technical Analysis and be able to pull your own conclusions from your test-results, this is not just an easy copy/paste.   

MGM (MoniGoMani) derives itself from other strategies by its use of something I called "weighted signals".   
Each signal has its own weight allocated to it & a total buy/sell signal needed is defined too.   
MGM will loop through all signals, if they trigger it will add up the weight and eventually it will check if it's bigger than what's needed in total over a candle lookback window (to take previous signals into consideration). If the grand total of the sum of weighted signals is bigger then what is required it will buy/sell. The signals used here are implemented, so they can easily be changed by a developer to further improve upon them.   
   
The beauty lies in using MGM in combination with HyperOpting (= A form of machine learning where you BackTest a timerange a lot of times to find the most ideal values), since all weighted signals have been made HyperOptable it can be used to find the most "ideal" weight divisions.   
Also will it teach us what works where & what doesn't since MoniGoMani first detects Downwards/Sideways/Upwards trends and then does all the above individually for each kind of trend (Creating basically 3 individual strategies, 1 for each kind of trend).  
 
Further it will do various HyperOptable checks upon the open trades to see if there are "bad" ones to unclog while running.   

## Feature List:   
- Partially [Automated Optimization Process](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani)
- All HyperOpt Results can easily be applied and removed with the use of some [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands)
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
- Configurable LookBack Windows for Total Buy/Sell Signal Percentages for Downwards/Sideways/Upwards trends ***(HyperOptable!)***
- Configurable Trading on Downwards/Sideways/Upwards trends for Buys/Sells ***(HyperOptable!)***
- Settings to Enable/Disable HyperOpting for individual `buy_params` & `sell_params` and setting them to a static value through [HyperOpt Setting Overrides](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#hyperopt-setting-overrides)
- Configurable [Open Trade Unclogger](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#open-trade-unclogger), if enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades ***(HyperOptable!)*** :rocket:   
- [TimeFrame-Zoom](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#timeframe-zoom) during BackTesting/HyperOpting to prevent profit exploitation! *(Read: [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/))*
- Custom Long Continuously decreasing ROI Table generation with configurable `roi_table_step_size`
- [Precision Setting](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#precision-setting) to alter the step-size used during HyperOpting
- 2 [Custom HyperLoss Functions](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#custom-hyperloss-functions):
  - [WinRatioAndProfitRatioLoss](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/WinRatioAndProfitRatioLoss.py): Attempts to optimise for the best profit **and** stability (Returns smaller number for better results)   
  - [UncloggedWinRatioAndProfitRatioLoss](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/UncloggedWinRatioAndProfitRatioLoss.py): Same as WinRatioAndProfitRatioLoss but has a configurable Percentage of loss to ignore while HyperOpting (Small losses are a by-product of the Unclogger)
- [Top Volume & All Tradable StaticPairList Downloading](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#download-staticpairlists) to easily fetch a good StaticPairList
- [Total Overall Signal Importance Calculator](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#total-overall-signal-importance-calculator) for Total Average Signal Importance Calculation upon the HyperOpt Results (With some really handy subcommands)
- Pre-Configured Main/Sub Plot Configurations for visualisation of all indicators used in FreqUI
- Turn On/Off **All** Individual Weighted Signal DataFrame entries for easy debugging in an IDE or better speed while dry/live running or HyperOpting   
   
*\*Support/Updates for Legacy versions stopped since Auto-HyperOptable Strategies are merged into the official Freqtrade Development Branch! Please switch to the new MoniGoManiHyperStrategy!*   

## Need help getting started?
Take a good read at the [**MGM_DOCUMENTATION.md**](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md), the current place where you can find all MoniGoMani Documentation!   

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

## **Got Test Results / Ideas / Config Improvements?**
- Feel free to join our community [**CryptoStonksShallRise**](https://discord.gg/xFZ9bB6vEz) on Discord, there you can follow/participate in the **Official MoniGoMani Channels**:
  - `#moni-go-mani-announcements`
  - `#moni-go-mani-development` *(Only available to MoniGoMani Developers!)*
  - `#moni-go-mani-updates`
  - `#moni-go-mani-testing`
  - `#moni-go-mani-help` *(Be sure to take your time to read the [Documentation](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md) thoroughly before asking questions though!)*
  - `#moni-go-mani-cluster-releases` *(Only available to the MoniGoMani Cluster Maintainer & MoniGoMani Developers, for now!)*
  - `#moni-go-mani-setup-releases`
   
More general chats for `Technical Analysis`, `Freqtrade`, `Iconomi` and `Random` discussion are also available there :slight_smile:   

## **Planned**:   
*Ordered by current schedule/priority*
- More global/broader trend detection using zoomed out indicator data
- [Sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function) Buy/Sell Signals
- **Other & Better indicators!** MoniGoMani has been designed so signals can easily be inserted / swapped out   
Please use the `Total-Overall-Signal-Importance-Calculator.py` to find out which signals do best and report your results to the [Discord Server](https://discord.gg/xFZ9bB6vEz), so we can improve! :rocket:
- HyperOpt over 3 separate timeranges (one representing each individual kind of trend, downwards/sideways/upwards, a timeframe that represents a corresponding trend should be picked)
- A method to pull a `Static Averaged Volume PairList` (Calculated by summing up the top volume pairlists for each candle over the period of the timerange to hyperopt upon & then dividing by the total amount of candles in the timerange, to create an averaged "volume" pairlist that can be used during BackTesting/HyperOpting which should lead to a more "realistic" pairlist to test upon when using a VolumePairList when dry/live-running)
- Improve upon bot loop speed (Try to improve code to reach reduction in HyperOpting time needed)
- Huge refactor that should improve the codebase reducing a lot of duplicate code & making implementing new weighted signals even easier
- [MultiProcessed DataFrame indicator checking](https://www.machinelearningplus.com/python/parallel-processing-python/) if possible for speed improvements
- HyperOpt over a `timerange` through a few simple Telegram commands, review the results and choose if and which new epoch should be applied.   

## **ChangeLog**:  
View the Legacy [ChangeLog](https://github.com/Rikj000/MoniGoMani/blob/main/CHANGELOG.md), newer changelogs are appended with each [Release](https://github.com/Rikj000/MoniGoMani/releases/)

## **Freqtrade**:   
**Freqtrade** is the well known `open source crypto day-trading bot` that makes this strategy possible!   
It's completely free to use and alter and has many amazing features.   
Big thank you to **xmatthias** and everyone who helped on it!   
- **[Official Freqtrade Website](https://www.freqtrade.io/en/latest/)**
- **[Official Freqtrade GitHub Repository](https://github.com/freqtrade/freqtrade)**
- **[Official Freqtrade Discord Server](https://discord.gg/j84KnP57kW)**- [Sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function) Buy/Sell Signals

## **ICONOMI**:   
Can't wait until MoniGoMani is fully on point? Or is this all too technical for you? Check out **[ICONOMI](https://www.iconomi.com/register?ref=JdFzz)!**

Instead of buying loose individual crypto manually like you usually do on exchanges, this platform has mostly been created to buy & hodl `Investment Strategies`.   
ICONOMI strategies are owned by `Strategy Managers`, these are often day-trades / technical analysts by profession so in general they have quite a good idea what they are doing.   
Each investment strategy contains up to ±20 different coins with a percentage allocated to each one. The managers will often re-balance these percentages towards coins they'll think will be profitable.   

There are fees tied to each strategy, and it's up to the manager of each strategy to pick the percentages of fees for his/her strategy. Usually strategies that are re-balanced often (aka market being watched more actively) or larger strategies with a good reputation ask higher fees. However, fees are only charged if **new** profits have been made, so they are quite in the benefit of the user.   
More [info on fees in general can be found here](https://www.iconomi.com/fees-disclosure), and more [info on Performance fees can be found here](https://iconomi.zendesk.com/hc/en-us/articles/360026664834-Performance-fee-Crypto-Strategies).
   
In general this is a good platform to invest into when you still need to start learning Technical Analysis, when you don't have time to monitor the status of the market or when you don't feel confident trading your own funds.   
Since here you have strategy owners "doing the day-trading for you" by re-balancing the strategies & the percentages of coins in them.

**If you join please use my referral link! => (https://www.iconomi.com/register?ref=JdFzz)** :pray:   
*(Then a percentage of your fees that you have to pay anyways to the strategy owners and ICONOMI will go to me instead, which is a neat win-win way for us both to support me for my work on MGM!)*

#### Recommended Iconomi Strategies
- [**Crypto Knowledge Pool**](https://www.iconomi.com/asset/BTCETHTEST?ref=JdFzz) (CKP): A community influenced strategy   
- [**CKP's Telegram Chat**](https://telegram.me/CKP_Robot?start=1684098549): If you want to vote if the coins will go up or down and hear about interesting news or ask questions. When I wrote this they we're right about 65% of the time. The manager will take the results into consideration when altering the strategy.    
- [**Knepala**](https://www.iconomi.com/asset/KNEPALA?ref=JdFzz): The personal strategy of the owner of CKP, most of the time it does even better than CKP itself.   
- Look on [ICONOMI](https://www.iconomi.com/register?ref=JdFzz) for more strategies you deem interesting :slight_smile: