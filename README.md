# **Current `MoniGoMani` status @ `v0.4.1`** with:
- Configurable & HyperOptable Buy/Sell Signal Weight Influence Tables
- Configurable & HyperOptable Total Buy/Sell Signal Percentages
- Turn On/Off Weighted Signals for easy debugging/better speed
- 10 Buy & 10 Sell signals implemented:
  - ADX + Up/Down
  - Up/Down
  - RSI
  - MACD
  - SMA Short Death/Golden Cross 
  - EMA Short Death/Golden Cross 
  - SMA Long Death/Golden Cross 
  - EMA Long Death/Golden Cross 
  - Bollinger Band Re-Entrance
  - VWAP Cross

### **Changelog / Backtest Results**:   
*(Testing rough 2 week -4.83% market time period, default coin pairs, 75% Total Buy, 25% Total Sell)*
- v0.0.1 (20-03-2021 - Weight Table, RSI)  -15% profit...
- v0.1.0 (21-03-2021 - Buy/Sell Weight Table, Total Buy/Sell Signal %, ADX, Up/Down, MACD) -8% profit..
- v0.2.0 (22-03-2021 - SMA Death/Golden Cross, BugFixed Signals) -0.29% profit!
- v0.2.1 (23-03-2021 - Refactored to SMA Long Death/Golden Cross + EMA Long Death/Golden Cross) **1.15% profit!**
- v0.2.2 (23-03-2021 - SMA and EMA Short Death/Golden Cross) 1.15% profit
- v0.2.3 (24-03-2021 - Bollinger Band Re-Entrance afer upward/downward breakout) 1.16% profit
- v0.3.0 (24-03-2021 - 0 weight = No Weighted Signal DataFrame entry)
- v0.3.1 (24-03-2021 - Turn On/Off all Weighted Signal DataFrame entries with a true/false)
- v0.3.2 (24-03-2021 - VWAP Cross) 1.24% profit
- v0.4.0 (25-03-2021 - Added HyperOpt for Weight Tables) **62.88% profit** (HyperOpt Result..)
- v0.4.1 (25-03-2021 - HyperOpt Params Real -> Integer, SortinoHyperOptLossDaily) **1322.78% profit - 124.6** (2 month HyperOpt Result, Mid Januari - Mid March)

### **Planned / Ideas:**
- Upward / Downward / Straight trend specific strats?
- Other/Better indicators? 