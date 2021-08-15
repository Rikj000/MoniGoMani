<p align="center">
        <img src="https://repository-images.githubusercontent.com/352191040/43a50e00-ab61-11eb-92c9-fb91d458e8af" alt="MoniGoMani" height="250" />
</p>

<p align="center" style="font-family: 'Segoe Script'">
    <i><b style="font-size: 2em;">MoniGoMani</b><br>Freqtrade Framework & Strategy</i>
</p>

<p align="center">
    <a href="https://matrix.to/#/+moni-go-mani:matrix.org">
        <img src="https://img.shields.io/matrix/MoniGoMani-Testing:matrix.org?label=Matrix%20Community&logo=matrix" alt="Join MoniGoMani on Matrix">
    </a> <a href="https://discord.gg/xFZ9bB6vEz">
        <img src="https://img.shields.io/discord/819237123009150977?label=Discord%20Server&logo=discord" alt="Join CryptoStonksShallRise on Discord">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases">
        <img src="https://img.shields.io/github/downloads/Rikj000/MoniGoMani/total?label=Total%20Downloads&logo=github" alt="Total Releases Downloaded from GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases/latest">
        <img src="https://img.shields.io/github/v/release/Rikj000/MoniGoMani?include_prereleases&label=Latest%20Release&logo=github" alt="Latest Official Release on GitHub">
    </a>
    <br>
    <a href="https://github.com/Rikj000/MoniGoMani/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Rikj000/MoniGoMani?label=License&logo=gnu" alt="GNU General Public License">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/wiki">
        <img src="https://img.shields.io/badge/Docs-MoniGoMani-blue?logo=libreoffice&logoColor=white" alt="The current place where you can find all MoniGoMani Documentation!">
    </a> <a href="https://www.freqtrade.io/en/latest/">
        <img src="https://img.shields.io/badge/Trading%20Bot-Freqtrade-blue?logo=probot&logoColor=white" alt="Freqtrade - The open source crypto day-trading bot">
    </a> <a href="https://www.iconomi.com/register?ref=JdFzz">
        <img src="https://img.shields.io/badge/Join-ICONOMI-blue?logo=bitcoin&logoColor=white" alt="ICONOMI - The world’s largest crypto strategy provider">
    </a>
</p>

<p align="center">
    <table>
        <tbody>
            <td align="center">
                <br><b>⚠️ Warning: Pre-release / Experimental ⚠️</b><br><sub>
                It's <b>not recommended</b> to use this strategy <b>live</b> already, due to it still being under heavy development!<br>
                If you'd like to see this project progress faster then please help out where you can
                <a href="https://github.com/Rikj000/MoniGoMani/issues">here</a>!
                <br><img width=1000><br>
                <b>Recommended Freqtrade commit: <a href="https://github.com/freqtrade/freqtrade/pull/5219/commits/3503fdb4ec31be99f433fdce039543e0911964d6">3503fdb4</a></b>
                <br><br>
            </td>
        </tbody>
    </table>
</p>

## Motivation
Isn't that what we all want? Our money to go many? Well that's what this Freqtrade  Framework & Strategy hopes to do for you "easily", in any market!

Big thank you to xmatthias and everyone who helped on MoniGoMani, Freqtrade Discord support was also really helpful, so thank you as-well!

If you like my work, feel free to donate or use [one of my referral links](#supported-exchanges), that would also greatly be appreciated:

<p align=center>
    <a href="https://www.iconomi.com/register?ref=JdFzz">
        <img src="https://img.shields.io/badge/Join-ICONOMI-blue?logo=bitcoin&logoColor=white" alt="ICONOMI - The world’s largest crypto strategy provider">
    </a> <a href="https://www.binance.com/en/register?ref=97611461">
        <img src="https://img.shields.io/badge/Join-BINANCE-yellow?logo=bitcoin&logoColor=white" alt="Binance - The world’s largest crypto exchange">
    </a> <a href="https://en.cryptobadges.io/donate/19LL2LCMZo4bHJgy15q1Z1bfe7mV4bfoWK">
        <img src="https://en.cryptobadges.io/badge/micro/19LL2LCMZo4bHJgy15q1Z1bfe7mV4bfoWK" alt="Donate Bitcoin">
    </a> <a href="https://www.buymeacoffee.com/Rikj000">
        <img src="https://img.shields.io/badge/-Buy%20me%20a%20Coffee!-FFDD00?logo=buy-me-a-coffee&logoColor=black" alt="Buy me a Coffee as a way to sponsor this project!">
    </a>
</p>

## ⚠️ Disclaimer
 - This Framework & Strategy are still experimental and under heavy development. It is not recommended running it live at this moment.
 - Always make sure to understand & test your MoniGoMani configuration until you trust it, before even thinking about going live!
 - I am in no way responsible for your live results! You are always responsible for your own MoniGoMani configuration!
 - MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/Documentation/Docs-MoniGoMani.md#how-to-optimize-monigomani) after doing manual changes!
 - You need to [optimized](https://github.com/Rikj000/MoniGoMani/blob/main/Documentation/Docs-MoniGoMani.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!
<hr>

## Table of Contents
- [Motivation](#motivation)
- [⚠️ Disclaimer](#️-disclaimer)
- [Table of Contents](#table-of-contents)
- [The Idea & Theory](#the-idea--theory)
- [Feature List](#feature-list)
- [Getting Started](#getting-started)
- [Go-To Commands](#go-to-commands)
- [Got Test Results - Ideas - Config Improvements?](#got-test-results---ideas---config-improvements)
- [Planned](#planned)
- [ChangeLog](#changelog)
- [Freqtrade](#freqtrade)
  - [Supported Exchanges](#supported-exchanges)
- [ICONOMI](#iconomi)
    - [Recommended ICONOMI Strategies](#recommended-iconomi-strategies)


## The Idea & Theory
**MoniGoMani** is more than just a conventional strategy, it's a **Framework** that aims to help you **"easily"** find a profitable strategy configuration in any market through our [partially automated optimization process](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani)!
Without the need to do any more real programming! :rocket:

However, you will need to know about [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/) and some Technical Analysis, to be able to tell if the MGM setup \*[HyperOpt](https://www.freqtrade.io/en/latest/hyperopt/) found over the tested timerange is valid or not, this is not just an easy copy/paste!

MGM (MoniGoMani) derives itself from other strategies by its use of something I called **weighted signals**.
Each signal has its own weight allocated to it & a total buy/sell signal needed is defined too.
MGM will loop through all signals, if they trigger it will add up the weight and eventually it will check if it's bigger than what's needed in total over a candle lookback window (to take previous signals into consideration). If the grand total of the sum of weighted signals is bigger then what is required it will buy/sell.

An **interface** has been implemented so the indicators and weighted signals used by MGM can easily be tweaked in just a few lines of code! :tada:

The beauty lies in using MGM in combination with **HyperOpting**. Most of the parameters in MGM have been made HyperOptable thus it can be used to find an "ideal" weight division and setting configuration for you in any kind of market that that represents the data upon which you test.
It will also teach us what works where & what doesn't since MoniGoMani first **detects Downwards/Sideways/Upwards trends** and then does all the above individually for each kind of trend *(Creating basically 3 individual strategies in 1, for each kind of trend one)*.

Further it has an embedded [Open Trade Unclogger](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#open-trade-unclogger) which will do various HyperOptable checks upon the open trades to see if there are "bad" ones to quickly unclog at small losses, so it can continue on the hunt for good trades more rapidly! :rocket:

\****HyperOpting:** A form of machine learning where you [BackTest](https://www.freqtrade.io/en/latest/backtesting/) a lot of times to find the most ideal values)*

## Feature List
- Partially [Automated Optimization Process](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani)
- All HyperOpt Results can easily be applied and removed with the use of some [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#go-to-commands)
- Configurable Buy/Sell Signal Weight Influence Tables for Downwards/Sideways/Upwards trends, each table **currently** has 10 Buy & 10 Sell signals implemented ***(HyperOptable!)***:
  - [ADX](https://www.investopedia.com/terms/a/adx.asp)
  - [MACD](https://www.investopedia.com/terms/m/macd.asp)
  - [MFI](https://www.investopedia.com/terms/m/mfi.asp)
  - [RSI](https://www.investopedia.com/terms/r/rsi.asp)
  - [SMA](https://www.investopedia.com/terms/s/sma.asp) Short [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross
  - [EMA](https://www.investopedia.com/terms/e/ema.asp) Short [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross
  - [SMA](https://www.investopedia.com/terms/s/sma.asp) Long [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross
  - [EMA](https://www.investopedia.com/terms/e/ema.asp) Long [Death](https://www.investopedia.com/terms/d/deathcross.asp)/[Golden](https://www.investopedia.com/terms/g/goldencross.asp) Cross
  - [Bollinger Band](https://www.investopedia.com/terms/b/bollingerbands.asp) Re-Entrance
  - [VWAP](https://www.investopedia.com/terms/v/vwap.asp) Cross
- [Weighted Signal Interface](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#weighted-signal-interface) to easily change the weighted signals being used
- Configurable Total Buy/Sell Signal Percentages for Downwards/Sideways/Upwards trends ***(HyperOptable!)***
- Configurable LookBack Windows for Total Buy/Sell Signal Percentages for Downwards/Sideways/Upwards trends ***(HyperOptable!)***
- Configurable Signal Triggers Needed within their respective LookBack Windows for Downwards/Sideways/Upwards trends ***(HyperOptable!)***
- Configurable [Trading During Trends](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#trading-during-trends) (Downwards/Sideways/Upwards) for Buys/Sells
- Configurable [Open Trade Unclogger](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#open-trade-unclogger), if enabled it attempts to unclog the bot when it's stuck with losing trades & unable to trade more new trades ***(HyperOptable!)*** :rocket:
- [TimeFrame-Zoom](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#timeframe-zoom) during BackTesting/HyperOpting to prevent profit exploitation! *(Read: [BackTesting-Traps](https://brookmiles.github.io/freqtrade-stuff/2021/04/12/backtesting-traps/))*
- [Configurable HyperOptable Stoploss](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#stoploss-spaces) to fine-tune where HyperOpt should look
- Custom Long Continuously decreasing ROI Table generation with configurable `roi_table_step_size`
- [Precision Setting](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#precision-setting) to alter the step-size used during HyperOpting
- 2 [Custom HyperLoss Functions](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#custom-hyperloss-functions):
  - [WinRatioAndProfitRatioLoss](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/WinRatioAndProfitRatioLoss.py): Attempts to optimise for the best profit **and** stability (Returns smaller number for better results)
  - [UncloggedWinRatioAndProfitRatioLoss](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/UncloggedWinRatioAndProfitRatioLoss.py): Same as WinRatioAndProfitRatioLoss but has a configurable Percentage of loss to ignore while HyperOpting (Small losses are a by-product of the Unclogger)
- [Top Volume & All Tradable StaticPairList Downloading](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#download-staticpairlists) to easily fetch and apply a good StaticPairList
- [Total Overall Signal Importance Calculator](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#total-overall-signal-importance-calculator) for Total Average Signal Importance Calculation upon the HyperOpt Results (With some really handy subcommands)
- Pre-Configured Main/Sub Plot Configurations for visualization of all indicators used in FreqUI
- Turn On/Off **All** Individual Weighted Signal DataFrame entries for easy debugging in an IDE or better speed while dry/live running or HyperOpting

## Getting Started
Take a good read at the [**MGM_DOCUMENTATION.md**](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md), the current place where you can find all MoniGoMani Documentation!

## Go-To Commands
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

## Got Test Results - Ideas - Config Improvements?
- Feel free to join our community [**MoniGoMani** on Matrix](https://matrix.to/#/+moni-go-mani:matrix) or [**CryptoStonksShallRise** on Discord](https://discord.gg/xFZ9bB6vEz), there you can follow/participate in the **Official MoniGoMani Channels**:
  - `📢︱moni-go-mani` *(All Official MGM Releases & important messages can be followed here)*
  - `✨︱git-updates` *(All GitHub Commits can be followed here)*
  - `🗞︱github-discussions` *(All conversations tied to GitHub Issues & Pull Requests can be followed here)*
  - `🖥︱development` *(Channel for discussing development on MGM. exclusive for MoniGoMani Developers)*
  - `👑︱testing-elite` *(Channel for members that have proven to be true additions to the community. Exclusive for MoniGoMani Testing MVP and above))*
  - `🛠︱testing` *(Your go-to channel for partaking in the community. Feel free to drop your test results / config files / ideas here)*
  - `❔︱help` *(Be sure to take your time to read the [Documentation](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md) thoroughly before asking questions though!)*
  - `🎉︱setup-releases` *(Release your personal profitable MGM configurations/HyperOpted versions here)*
  - `🗄︱cluster-results` *(Automated Ph3nol Cluster Releases. Exclusive to the MoniGoMani Cluster Maintainer & MoniGoMani Developers, for now!)*

More general chats for `📈︱technical-analysis`, `🤖︱freqtrade`, `📊︱iconomi` and `🍉︱random` discussion are also available there :slightly_smiling_face:

## Planned
MoniGoMani's planned section lives under the [**Issues**](https://github.com/Rikj000/MoniGoMani/issues) section!
*(Don't be scared GitHub likes to pick bad names for things, but also don't abuse this for common questions though!)*
This is where we'll keep track of all **New Feature, Feature Enhancements and BugFixes** and it should be the ideal place to follow the status of the project more in depth or to contribute more directly towards it! :handshake:

- [**All Open Issues**](https://github.com/Rikj000/MoniGoMani/issues)
- [**All Things Planned**](https://github.com/Rikj000/MoniGoMani/issues?q=is%3Aissue+is%3Aopen+label%3APlanned)
- [**All Known Bugs**](https://github.com/Rikj000/MoniGoMani/issues?q=is%3Aissue+is%3Aopen+label%3A%22Bug+-+Fix+Needed%22)

To keep track of what's exactly planned for the next release you can also check the [**Milestones**](https://github.com/Rikj000/MoniGoMani/milestones) section!

You can also check out the [**MoniGoMani - Global Development Progress**](https://github.com/Rikj000/MoniGoMani/projects/1?fullscreen=true) board, which gives a clear overview of all what is `Planned`, `In Progress` & `Done`!

## ChangeLog
MoniGoMani's ChangeLog can be read under the [**Releases**](https://github.com/Rikj000/MoniGoMani/releases/) section!

## Freqtrade
**Freqtrade** is the well known `open source crypto day-trading bot` that makes this strategy possible!
It's completely free to use and alter and has many amazing features.
Big thank you to **xmatthias** and everyone who helped on it!
- **[Official Freqtrade Website](https://www.freqtrade.io/en/latest/)**
- **[Official Freqtrade GitHub Repository](https://github.com/freqtrade/freqtrade)**
- **[Official Freqtrade Discord Server](https://discord.gg/j84KnP57kW)**

### Supported Exchanges

Please read Freqtrade's [exchange specific notes](https://www.freqtrade.io/en/latest/exchanges/) to learn about eventual, special configurations needed for each exchange.
| Exchange | Join | Freqtrade Support | CCXT Certified | Discount |
|:--------:|:----:|:-----------------:|:--------------:|:--------:|
| [![binance](https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg)](https://www.binance.com/en/register?ref=97611461) | [Binance](https://www.binance.com/en/register?ref=97611461) | [![Freqtrade Support](https://img.shields.io/badge/Freqtrade-Supported-blue.svg)](https://www.freqtrade.io/en/latest/#supported-exchange-marketplaces) | [![CCXT Certified](https://img.shields.io/badge/CCXT-Certified-green.svg)](https://github.com/ccxt/ccxt/wiki/Certification) | [![Sign up with Binance using my referral link for a 5% discount!](https://img.shields.io/static/v1?label=Fee&message=%2d5%25&color=orange)](https://www.binance.com/en/register?ref=97611461) |
| [![ftx](https://user-images.githubusercontent.com/1294454/67149189-df896480-f2b0-11e9-8816-41593e17f9ec.jpg)](https://ftx.com/#a=33116566) | [FTX](https://ftx.com/#a=33116566) | [![Freqtrade Support](https://img.shields.io/badge/Freqtrade-Supported-blue.svg)](https://www.freqtrade.io/en/latest/#supported-exchange-marketplaces) | [![CCXT Certified](https://img.shields.io/badge/CCXT-Certified-green.svg)](https://github.com/ccxt/ccxt/wiki/Certification) | [![Sign up with FTX using my referral link for a 5% discount!](https://img.shields.io/static/v1?label=Fee&message=%2d5%25&color=orange)](https://ftx.com/#a=33116566) |
| [![kraken](https://user-images.githubusercontent.com/51840849/76173629-fc67fb00-61b1-11ea-84fe-f2de582f58a3.jpg)](https://www.kraken.com) | [Kraken](https://www.kraken.com) | [![Freqtrade Support](https://img.shields.io/badge/Freqtrade-Supported-blue.svg)](https://www.freqtrade.io/en/latest/#supported-exchange-marketplaces) | [![CCXT Certified](https://img.shields.io/badge/CCXT-Certified-green.svg)](https://github.com/ccxt/ccxt/wiki/Certification) |
| [![bittrex](https://user-images.githubusercontent.com/51840849/87153921-edf53180-c2c0-11ea-96b9-f2a9a95a455b.jpg)](https://bittrex.com/Account/Register?referralCode=JCC-AWM-VU1) | [Bittrex](https://bittrex.com/Account/Register?referralCode=JCC-AWM-VU1) | [![Freqtrade Support](https://img.shields.io/badge/Freqtrade-Supported-blue.svg)](https://www.freqtrade.io/en/latest/#supported-exchange-market$places) |
| [![bitvavo](https://user-images.githubusercontent.com/1294454/83165440-2f1cf200-a116-11ea-9046-a255d09fb2ed.jpg)](https://bitvavo.com/?a=2D64A068E5) | [Bitvavo](https://bitvavo.com/?a=2D64A068E5) | [![Freqtrade Support](https://img.shields.io/badge/Freqtrade-Community_Tested-blue.svg)](https://www.freqtrade.io/en/latest/#community-tested) | [![CCXT Certified](https://img.shields.io/badge/CCXT-Certified-green.svg)](https://github.com/ccxt/ccxt/wiki/Certification) | |
| [![kucoin](https://user-images.githubusercontent.com/51840849/87295558-132aaf80-c50e-11ea-9801-a2fb0c57c799.jpg)](https://www.kucoin.com/ucenter/signup?rcode=rJ2VUZ3) | [KuCoin](https://www.kucoin.com/ucenter/signup?rcode=rJ2VUZ3) | [![Freqtrade Support](https://img.shields.io/badge/Freqtrade-Community_Tested-blue.svg)](https://www.freqtrade.io/en/latest/#community-tested) | |


## ICONOMI
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

#### Recommended ICONOMI Strategies
- [**Crypto Knowledge Pool**](https://www.iconomi.com/asset/BTCETHTEST?ref=JdFzz) (CKP): A community influenced strategy
- [**CKP's Telegram Chat**](https://telegram.me/CKP_Robot?start=1684098549): If you want to vote if the coins will go up or down and hear about interesting news or ask questions. When I wrote this they we're right about 65% of the time. The manager will take the results into consideration when altering the strategy.
- [**Knepala**](https://www.iconomi.com/asset/KNEPALA?ref=JdFzz): The personal strategy of the owner of CKP, most of the time it does even better than CKP itself.
- Look on [ICONOMI](https://www.iconomi.com/register?ref=JdFzz) for more strategies you deem interesting :slightly_smiling_face:
