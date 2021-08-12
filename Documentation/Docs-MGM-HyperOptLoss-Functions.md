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
- [MoniGoMani HyperOptLoss Functions](#monigomani-hyperoptloss-functions)
  - [MGM_WeightedMultiParameterHyperOptLoss](#mgm_weightedmultiparameterhyperoptloss)
    - [How to use the MGM_WeightedMultiParameterHyperOptLoss](#how-to-use-the-mgm_weightedmultiparameterhyperoptloss)
      - [`sortino` settings](#sortino-settings)
      - [`parameter_threshold_high/low` settings](#parameter_threshold_highlow-settings)
      - [Other notes](#other-notes)
  - [MGM_GeniusHyperOptLoss](#mgm_geniushyperoptloss)
    - [How to use the MGM_GeniusHyperOptLoss](#how-to-use-the-mgm_geniushyperoptloss)
  - [MGM_WinRatioAndProfitRatioHyperOptLoss](#mgm_winratioandprofitratiohyperoptloss)
  - [MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss](#mgm_uncloggedwinratioandprofitratiohyperoptloss)


# MoniGoMani HyperOptLoss Functions
MoniGoMani Ships with a handful of Custom HyperOptLoss Objective Functions. You can find them under `user_data/hyperopts/`.
Most of these contain configurable parameters. All of these settings can be tweaked from within your [mgm-config]([mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config.json)) under the `monigomani_hyperoptloss_settings` section to make up for a more robust strategy.


## MGM_WeightedMultiParameterHyperOptLoss
MGM_WeightedMultiParameterHyperOptLoss Customizable HyperOpt Objective function. Returns smaller number for better results.
This HyperOptLoss Function is the main HyperOptLoss Function utilized by MoniGoMani.
It allows the user to choose possible Parameter Weight Objective Configurations, each of these influence the outcome of the final Objective.

All settings for the `MGM_WeightedMultiParameterHyperOptLoss` function can be found in your [mgm-config]([mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config.json)) under the `MGM_WeightedMultiParameterHyperOptLoss` section of the `monigomani_hyperoptloss_settings` section.
Following **parameter sections** can be configured to fine-tune your MoniGoMani Configuration further:
- `drawdown`
- `duration`
- `profit`
- `sortino`
- `trades`

Each parameter section contains following **parameter settings**:
- `expected_parameter`
- `parameter_weight`
- `parameter_threshold_high`
- `parameter_threshold_low`

**Example:** If you would want quick trades and don't care too much about risk, then you would set a higher value on the `trades_weight` parameter and a lower value on the `sortino_weight` parameter.

**<span style="color:darkorange">WARNING:</span> Keep weights reasonably low, use 1 as a baseline. Hyperopt doesn't seem to like it when the objective gets close or above 100.** *(See next issue)*
**<span style="color:darkorange">WARNING:</span> If you don't see any "Best epochs" within the first 30 epochs, then the loss function either too sensitive or not sensitive enough.
It's not recommended to continue the hyperopt if this would be the case as it'll never find an optimal epoch. Instead, think about if your weights and expected values make sense.**

### How to use the MGM_WeightedMultiParameterHyperOptLoss
- All values are ratios unless stated otherwise, so `1.65 = 165%`
- Set the `expected_parameter` value to something that makes sense!
*(There's no point setting `expected_profit` to 9000% thinking that it'll magically make you a lambo owner...)*
- A good way of using the `expected_profit` value is if you have an optimized MoniGoMani configuration and you know it can make `X` profit, but you want to see if you can push it that extra bit more, so maybe set the `expected_profit` to `X + 25%`
- Or if your optimized MoniGoMani configuration leaves you with a drawdown of `150%`. You can try setting the `expected_drawdown` to `0.8`, to see if HyperOpt can narrow down your signals to reach a better drawdown.

#### `sortino` settings
If you run a HyperOpt with Freqtrade's own `SortinoHyperOptLossDaily` function, then the objective of that is the inverse of the `MGM_WeightedMultiParameterHyperOptLoss` value.

**Example:** If you ran a hyperopt using `SortinoHyperOptLossDaily` and the best epoch is giving an Objective of -20, then you could set the `expected_sortino` here to `25` to try and get a slightly better value.

#### `parameter_threshold_high/low` settings
These allow you to tell to HyperOpt that certain values are really not good/optimal.
This is done by increasing the Objective a bit more if the found objectives are not within the defined thresholds. These are incredibly useful for narrowing down for optimal results!

It's recommended to start out with a wide range on your thresholds to get an idea of what direction your strategy likes to lean towards. Then use them to further optimize the parameters that you'd like to improve.

**Examples:**
- `profit_threshold_low`: When the profit found is below this value, HyperOpt will be punished by increasing the Objective. Since we see this as very bad.
- `expected_profit = 4.5` *(450% profit expected)* & `profit_threshold_low = 0.5` *(50% of our expected profit, so at least `2.25 (225%)` profit is expected)*. Imagine that a profit of `1.75 (175%)` is found, this is below the defined `profit_threshold_low`, thus HyperOpt gets punished.

**Disable Thresholds:**
If you don't want to use a certain threshold value then you can easily disable them as following:
- `parameter_threshold_low`: Set the value to `0`
- `parameter_threshold_high`: Set the value to something insanely high, like `+1000`

#### Other notes
- **Disable Weights:** If any of the `parameter_weight` settings don't matter to you, then just set it's corresponding `parameter_weight` value to 0 and it will be disabled.
- **Longer & More Trades:** This function makes the assumption that you want shorter and less trades, if you want it to HyperOpt towards longer and more trades, then set the `parameter_flip_objective` parameters inside the `MGM_WeightedMultiParameterHyperOptLoss.py` file to `True`. *(This has not been tested yet!)*
- **Logging:** If `use_mgm_logging` & `mgm_log_levels`'s `info` both are set to `true`, then the found parameters *(and their found weights)* will be printed out to the console. This can be very helpful for working out expected parameters, or to see why HyperOpt thinks an epoch that looks good to you isn't actually that great! Recommended to use with `--print-all`.


## MGM_GeniusHyperOptLoss
MGM_GeniusHyperOptLoss Customizable HyperOpt Objective function. Returns smaller number for better results.
Considers various metrics to fine-tune for a more robust strategy configuration!

All settings for the `MGM_GeniusHyperOptLoss` function can be found in your [mgm-config]([mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config.json)) under the `MGM_GeniusHyperOptLoss` section of the `monigomani_hyperoptloss_settings` section.
Following **parameter sections** can be configured to fine-tune your MoniGoMani Configuration further:
- `sortino`
- `weight`
- `other`

### How to use the MGM_GeniusHyperOptLoss
- `weight` settings: Are used to control how much a certain section influences the Objective function returned by the HyperOptLoss function
- `average_profit_threshold`: Upper threshold of average profit to rely on *(To cut off crazy average profits like +20%)* 
- `ignore_small_profits`: If set to `true` then `small_profits_threshold` will be used to filter out results with small profits *(To take the possible spread into consideration)*


## MGM_WinRatioAndProfitRatioHyperOptLoss
MGM_WinRatioAndProfitRatioHyperOptLoss HyperOpt Objective function. Returns smaller number for better results.

This function optimizes for both best profit & stability. On stability, the final score has an incentive, through `win_ratio`, to make more winning deals out of all deals done.
This might prove to be more reliable for dry and live runs of FreqTrade and prevent over-fitting on best profit only.

## MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss
MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss Customizable HyperOpt Objective function. Returns smaller number for better results.

This function optimizes for both best profit & stability. On stability, the final score has an incentive, through `win_ratio`, to make more winning deals out of all deals done.
This might prove to be more reliable for dry and live runs of FreqTrade and prevent over-fitting on best profit only.

Trades with losses between the `unclogger_profit_ratio_loss_tolerance` are ignored, as those are considered to be a by-product of the MoniGoMani Unclogger. *(Examples: 0% - 2%)*
The setting for the `MGM_UncloggedWinRatioAndProfitRatioHyperOptLoss` function can be found in your [mgm-config]([mgm-config.json](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/mgm-config.json)) under the `MGM_WeightedMultiParameterHyperOptLoss` section of the `monigomani_hyperoptloss_settings` section.