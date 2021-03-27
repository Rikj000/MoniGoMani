```
    ####################################################################################
    ####                                                                            ####
    ###                         MoniGoMani v0.5.0 by Rikj000                         ###
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

# **Current `MoniGoMani` status @ `v0.5.0`** with:
- Configurable & HyperOptable Buy/Sell Signal Weight Influence Tables for Upward/Downward trends
- Configurable & HyperOptable Total Buy/Sell Signal Percentages for Upward/Downward trends
- Turn On/Off Weighted Signals for easy debugging/better speed
- Each table has 9 Buy & 9 Sell signals implemented each Configurable & HyperOptable:
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

### **Changelog / Backtest Results**:
*(Testing rough 2 week -4.83% market time period, default coin pairs, 75% Total Buy, 25% Total Sell)*
- v0.0.1 (20-03-2021 - Weight Table, RSI)  -15% profit...
- v0.1.0 (21-03-2021 - Buy/Sell Weight Table, Total Buy/Sell Signal %, ADX, Up/Down, MACD) -8% profit..
- v0.2.0 (22-03-2021 - SMA Death/Golden Cross, BugFixed Signals) -0.29% profit!
- v0.2.1 (23-03-2021 - Refactored to SMA Long Death/Golden Cross + EMA Long Death/Golden Cross) **1.15% profit!** :partying_face:
- v0.2.2 (23-03-2021 - SMA and EMA Short Death/Golden Cross) 1.15% profit
- v0.2.3 (24-03-2021 - Bollinger Band Re-Entrance afer upward/downward breakout) 1.16% profit
- v0.3.0 (24-03-2021 - 0 weight = No Weighted Signal DataFrame entry)
- v0.3.1 (24-03-2021 - Turn On/Off all Weighted Signal DataFrame entries with a true/false)
- v0.3.2 (24-03-2021 - VWAP Cross) 1.24% profit
- v0.4.0 (25-03-2021 - Added HyperOpt for Weight Tables) **62.88% profit** (HyperOpt Result..)
- v0.4.1 (25-03-2021 - HyperOpt Params Real -> Integer, SortinoHyperOptLossDaily) **1322.78% profit** :sunglasses: :chart_with_upwards_trend:  (2 month HyperOpt Result, Mid Januari - Mid March)
- v0.4.2 (27-03-2021 - Main/Sub Plot Configurations for all indicators used)
- v0.5.0 (27-03-2021 - Rewrote Weight tables for Upward/Downward trends, Upward/Downward/Sideways trend detection & Auto table allocation or wait if sideways, Scrapped 0 weight = No Weighted Signal DataFrame entry, Scrapped the configurable Up/Down signals) **2,568.61% profit!** :partying_face: 

### **Planned**:   
- Weighted Tables for SideWays movement
- Other/Better indicators?
