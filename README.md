```
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.7.0 by Rikj000                         ###
    ##                          ----------------------------                          ##
    #               Isn't that what we all want? Our money to go many?                 #
    #          Well that's what this Freqtrade strategy hopes to do for you!           #
    ##       By giving you/HyperOpt a lot of signals to alter the weight from         ##
    ###           ------------------------------------------------------             ###
    ##        Big thank you to xmatthias and everyone who helped on Freqtrade,        ##
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

**WARNING: MoniGoMani should always be HyperOpted unless you really know what you are doing when manually allocating weights!**   
**MoniGoManiHyperOpted already has a decent hyperopt applied to it!**   

# **Current `MoniGoMani` status @ `v0.7.0`** with:
- Configurable & HyperOptable Buy/Sell Signal Weight Influence Tables for Downwards/Sideways/Upwards trends
- Configurable & HyperOptable Total Buy/Sell Signal Percentages for Downwards/Sideways/Upwards trends
- Turn On/Off Trading on Downwards/Sideways/Upwards trends for Buys/Sells (HyperOptable)
- Turn On/Off Individual Weighted Signal DataFrame entries for easy debugging/better speed
- Each Table has 9 Buy & 9 Sell signals implemented each Configurable & HyperOptable:
  - ADX + Strong Up/Strong Down
  - RSI
  - MACD
  - SMA Short Death/Golden Cross 
  - EMA Short Death/Golden Cross 
  - SMA Long Death/Golden Cross 
  - EMA Long Death/Golden Cross 
  - Bollinger Band Re-Entrance
  - VWAP Cross
- Main/Sub Plot Configurations for all indicators used (Handy for FreqUI but requires Docker `freqtrade:develop_plot` & `technical` dependencies)

### Go-To Commands:
For HyperOpting:
```bash
freqtrade hyperopt --config ./user_data/config.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all --hyperopt MoniGoManiHyperOpt --strategy MoniGoMani -e 1000 --timerange 20210101-20210316
```
For BackTesting:
```bash
freqtrade backtesting --strategy MoniGoManiHyperOpted --config ./user_data/config.json --timerange 20210101-20210316
```

### **ChangeLog**:  
[View the ChangeLog](https://github.com/Rikj000/MoniGoMani#changelog)

### **Planned**:   
*Ordered by current schedule/priority*
- Add FreqUI to the MGM DockerFile
- Huge code refactor that will change the original `trend` array to the new `buy_params` & `sell_params` (added in `v0.7.0`) throughout all MGM code
- [Refactor to be compliant for Auto-HyperOptable Strategies](https://github.com/freqtrade/freqtrade/pull/4596)
- [MultiThreaded Dataframe indicator checking](https://www.machinelearningplus.com/python/parallel-processing-python/) if possible for speed improvements
- Settings to enable/disable HyperOpting for individual `buy_params` & `sell_params`
- **Other & Better indicators!** MoniGoMani has been designed so signals can easily be inserted / swapped out. So try to learn from the HyperOpt Weight Table Results, which signals usually score high and which often score low. That will tell us which signals work really well and which don't
- **Maybe!** An additional results table that will tell us how good which signals usually score high and which often score low (when a hyperopt has been done), that would save a lot of hassle in finding **Other & Better indicators**.
- Individual `BTC_config.json` & `USDT_config.json` files, aswell as individual `BTC_MoniGoManiHyperOpted.py` & `USDT_MoniGoManiHyperOpted.py` releases

### Got Test Results / Ideas / Config Improvements?
- Feel free to join [**CryptoStonksShallRise**](https://discord.gg/qmmzzsxg) on Discord there you can follow/participate in the official channels:
  - `#moni-go-mani-updates`
  - `#moni-go-mani-testing`

### Need help getting started?
[View the VeryQuickStart](https://github.com/Rikj000/MoniGoMani#veryquickstart)

### **Freqtrade**:   
The Bot that makes this strategy possible: https://github.com/freqtrade/freqtrade   
Big thank you to **xmatthias** and everyone who helped on it!