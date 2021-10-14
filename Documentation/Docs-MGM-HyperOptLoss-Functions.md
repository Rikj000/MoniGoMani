<p align="left">
    <a href="https://matrix.to/#/+moni-go-mani:matrix.org">
        <img src="https://img.shields.io/matrix/MoniGoMani-Testing:matrix.org?label=Matrix%20Community&logo=matrix" alt="Join MoniGoMani on Matrix">
    </a>  <a href="https://discord.gg/xFZ9bB6vEz">
        <img src="https://img.shields.io/discord/819237123009150977?label=Discord%20Server&logo=discord" alt="Join MoniGoMani on Discord">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases">
        <img src="https://img.shields.io/github/downloads/Rikj000/MoniGoMani/total?label=Total%20Downloads&logo=github" alt="Total Releases Downloaded from GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases/latest">
        <img src="https://img.shields.io/github/v/release/Rikj000/MoniGoMani?include_prereleases&label=Latest%20Release&logo=github" alt="Latest Official Release on GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/blob/development/LICENSE">
        <img src="https://img.shields.io/github/license/Rikj000/MoniGoMani?label=License&logo=gnu" alt="GNU General Public License">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/wiki">
        <img src="https://img.shields.io/badge/Docs-MoniGoMani-blue?logo=libreoffice&logoColor=white" alt="The current place where you can find all MoniGoMani Documentation!">
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
- [MoniGoMani HyperOptLoss Functions](#monigomani-hyperoptloss-functions)
  - [MGM_WinRatioAndProfitRatioHyperOptLoss](#mgm_winratioandprofitratiohyperoptloss)
      - [`total_trades_threshold_low`](#total_trades_threshold_low)
  - [MGM_SortinoHyperOptLoss](#mgm_sortinohyperoptloss)
      - [`total_trades_threshold_low`](#total_trades_threshold_low-1)
  - [MGM_WeightedMultiParameterHyperOptLoss](#mgm_weightedmultiparameterhyperoptloss)
    - [Usage notes](#usage-notes)
      - [Disable Weights](#disable-weights)
      - [Longer & More Trades](#longer--more-trades)
      - [Logging](#logging)


# MoniGoMani HyperOptLoss Functions
MoniGoMani Ships with 3 Custom HyperOptLoss Objective Functions which can be found under `user_data/hyperopts/`:

| HyperOptLoss Name | Application |
| ----------------- | ----------- |
| [MGM_WinRatioAndProfitRatioHyperOptLoss](#mgm_winratioandprofitratiohyperoptloss) | Initial & refinement HyperOpt runs |
| [MGM_SortinoHyperOptLoss](#mgm_sortinohyperoptloss) | Initial & refinement HyperOpt runs |
| [MGM_WeightedMultiParameterHyperOptLoss](#mgm_weightedmultiparameterhyperoptloss) | Only refinement HyperOpt Runs |

These contain configurable parameters. All of their settings can be tweaked from within your [mgm-config](https://github.com/Rikj000/MoniGoMani/blob/development/user_data/mgm-config.json) under the `monigomani_hyperoptloss_settings` section to make up for a more robust strategy.

## MGM_WinRatioAndProfitRatioHyperOptLoss
MGM_WinRatioAndProfitRatioHyperOptLoss HyperOpt Objective function. Returns smaller number for better results. *(More negative = better)*

This function optimizes for both best `profit` & stability. On stability, the final score has an incentive, through `win_ratio`, to make more winning deals out of all deals done.

#### `total_trades_threshold_low`
It will also punish the HyperOpt if the trades found in an epoch are below the configured `total_trades_threshold_low` as a way to prevent over-fitting on too low trades with too high average duration.
 *(Setting can be found under the `total_trades` section in the `monigomani_hyperoptloss_settings` section inside [mgm-config](https://github.com/Rikj000/MoniGoMani/blob/development/user_data/mgm-config.json))*

## MGM_SortinoHyperOptLoss
MGM_SortinoHyperOptLoss HyperOpt Objective function. Returns smaller number for better results. *(More negative = better)*

This function calculates the Sortino ratio, a variation of the Sharpe ratio that differentiates harmful volatility from total overall volatility by using standard deviation of negative results downside deviation, instead of the total standard deviation of results. 
The Sortino ratio takes a result and subtracts the risk-free rate, and then divides that amount by the downside deviation.

#### `total_trades_threshold_low`
It has been customized to also punish the HyperOpt if the trades found in an epoch are below the configured `total_trades_threshold_low` as a way to prevent over-fitting on too low trades with too high average duration.
 *(Setting can be found under the `total_trades` section in the `monigomani_hyperoptloss_settings` section inside [mgm-config](https://github.com/Rikj000/MoniGoMani/blob/development/user_data/mgm-config.json))*


## MGM_WeightedMultiParameterHyperOptLoss
MGM_WeightedMultiParameterHyperOptLoss Customizable HyperOpt Objective function. Returns smaller number for better results. *(More negative = better)*

This HyperOptLoss Function is a **final refinement** HyperOptLoss Function utilized by MoniGoMani.
It allows the user to choose possible Parameter Weight Objective Configurations, which represent the columns from the HyperOpt output table,
Each of these influence the outcome of the final Objective.

All settings for the `MGM_WeightedMultiParameterHyperOptLoss` function can be found in your [mgm-config]([mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/development/user_data/mgm-config.json)) under the `MGM_WeightedMultiParameterHyperOptLoss` section of the `monigomani_hyperoptloss_settings` section.

Following **parameter sections** can be configured to fine-tune your MoniGoMani Configuration further for more desired results:

| Parameter section    | Optimize direction |
| :------------------- | -----------------: |
| **total_trades**     | lower              |
| **win_ratio**        | higher             |
| **average_profit**   | higher             |
| **total_profit**     | higher             |
| **average_duration** | lower              |
| **max_drawdown**     | lower              |

Each parameter section contains following **parameter settings** to control the punish/reward system for them:

| Parameter name               | Description |
| :--------------------------- | :---------- |
| **parameter_weight**         | Defines the amount of influence weight that this parameter section has on the HyperOpt Results in percentages. With 100% being the base influence weight *(aka x1)*, adjusting to 200% would make this section x2 as important as the other parameter sections with the default weight. |
| **expected_parameter**       | Parameter value that is expected to be found. |
| **parameter_threshold_high** | Highest parameter value that should be allowed to be found. |
| **parameter_threshold_low**  | Lowest parameter value that should be allowed to be found. |

HyperOpt is **punished** if the found parameter value is not in between the defined high/low threshold values, the farther off the expected value, the harder the punishment.
HyperOpt is **rewarded** if the found parameter value is between the defined high/low threshold values, giving more rewards regarding the desired optimize direction *(`higher` or `lower`)*

### Usage notes
- Set the `expected_parameter` & `threshold` values to something that makes sense!
*(There's no point setting `expected_profit` to 9000% thinking that it'll magically make you a lambo owner...)*
- A good way of using the `expected_profit` value is if you have an optimized MoniGoMani configuration and you know it can make `X` profit, but you want to see if you can push it that extra bit more, so maybe set the `expected_profit` to `X + 25%`
- Or if your optimized MoniGoMani configuration leaves you with a drawdown of `150%`. You can try setting the `expected_drawdown` to `90%`, to see if HyperOpt can narrow down your signals to reach a better drawdown.

#### Disable Weights
If any of the `parameter_weight` settings don't matter to you, then just set it's corresponding `parameter_weight` value to **0** and it will be disabled.
#### Longer & More Trades
This function makes the assumption that you want shorter and less trades, if you for example want it to HyperOpt towards longer and more trades, then adjust the `optimize_direction` parameters inside the `MGM_WeightedMultiParameterHyperOptLoss.py` file to `higher` or `lower` accordingly. *(This has not been tested yet!)*
#### Logging
If `use_mgm_logging` & `mgm_log_levels`'s `info` both are set to `true`, then the found parameters *(and their found weights)* will be printed out to the console. This can be very helpful for working out expected parameters, or to see why HyperOpt thinks an epoch that looks good to you isn't actually that great! Recommended to use with `--print-all`.