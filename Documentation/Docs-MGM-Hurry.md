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
    </a> <a href="https://monigomani.readthedocs.io/">
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
 - This Framework & Strategy are still experimental and under heavy development. It is not recommended running it live at this moment.
 - Always make sure to understand & test your MoniGoMani configuration until you trust it, before even thinking about going live!
 - I am in no way responsible for your live results! You are always responsible for your own MoniGoMani configuration!
 - MoniGoMani should always be [re-optimized](https://monigomani.readthedocs.io/Docs-MoniGoMani/#how-to-optimize-monigomani) after doing manual changes!
 - You need to [optimized](https://monigomani.readthedocs.io/Docs-MoniGoMani/#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!
<hr>


<p align="center">
<img src="https://user-images.githubusercontent.com/86197446/123507408-6d624900-d669-11eb-9606-4a022bc4a117.png" width="300" height="289" align="center">
</p>

MGM-Hurry is a command line tool to speedup & simplify the setup & usage of [Freqtrade](https://www.freqtrade.io/en/stable/) in combination with the [MoniGoMani](https://github.com/Rikj000/MoniGoMani) FrameWork & Strategy.
Setting it all up requires some knowledge of the entire process, until you found MGM-Hurry! 💨


## Table of Contents
---

- [⚠️ Disclaimer](#️-disclaimer)
- [## Table of Contents](#-table-of-contents)
- [## `mgm-hurry` Command Usage](#-mgm-hurry-command-usage)
  - [`mgm-hurry --help`](#mgm-hurry---help)
  - [`mgm-hurry version`](#mgm-hurry-version)
  - [`mgm-hurry up`](#mgm-hurry-up)
  - [`mgm-hurry install_freqtrade`](#mgm-hurry-install_freqtrade)
    - [Options](#options)
  - [`mgm-hurry install_mgm`](#mgm-hurry-install_mgm)
    - [Options](#options-1)
  - [`mgm-hurry setup`](#mgm-hurry-setup)
  - [`mgm-hurry cleanup`](#mgm-hurry-cleanup)
  - [`mgm-hurry download_static_pairlist`](#mgm-hurry-download_static_pairlist)
    - [Options](#options-2)
  - [`mgm-hurry download_candle_data`](#mgm-hurry-download_candle_data)
    - [Option](#option)
  - [`mgm-hurry hyperopt`](#mgm-hurry-hyperopt)
    - [Options](#options-3)
  - [`mgm-hurry backtest`](#mgm-hurry-backtest)
    - [Options](#options-4)
  - [`mgm-hurry plot_stats`](#mgm-hurry-plot_stats)
    - [Option](#option-1)
  - [`mgm-hurry importance_report`](#mgm-hurry-importance_report)
    - [Option](#option-2)
  - [`mgm-hurry export_csv`](#mgm-hurry-export_csv)
    - [Option](#option-3)
  - [`mgm-hurry hyperopt_show_epoch`](#mgm-hurry-hyperopt_show_epoch)
    - [Options](#options-5)
  - [`mgm-hurry hyperopt_show_results`](#mgm-hurry-hyperopt_show_results)
    - [Options](#options-6)
  - [`mgm-hurry start_trader`](#mgm-hurry-start_trader)
    - [Option](#option-4)
- [## Example timeranges](#-example-timeranges)
- [Developer Notes](#developer-notes)
- [### Virtual Environment](#-virtual-environment)
- [### Continuous Integration](#-continuous-integration)
- [### Module headers](#-module-headers)

## `mgm-hurry` Command Usage
---

⚠️ A [shell alias](https://monigomani.readthedocs.io/Docs-VeryQuickStart/#shell-alias) has been configured for these shorter example commands.
If you haven't done that optional step then you will need to prefix all your commands with `python3 -m pipenv run ./mgm-hurry ...` in the root installation folder instead of just being able to run `mgm-hurry ...` anywhere!


### `mgm-hurry --help`
Displays information about the commands and their usage.
General usage format: `python3 mgm-hurry [command] [options]`


### `mgm-hurry version`
Displays the currently installed MoniGoMani & Freqtrade versions on `source` installations.


### `mgm-hurry up`
Quick start command, launches an interactive wizard which guides you through the entire process of:
- Installing & configuring Freqtrade
- Installing & configuring MoniGoMani
- Configuring exchange API
- Configuring Telegram bot API
- Generating a static pairlist
- Downloading historic candle data for HyperOpting & BackTesting
- Running required HyperOpt runs
- BackTesting your setup
- And finally start trading!


### `mgm-hurry install_freqtrade`
Individual command to install & update Freqtrade.
#### Options
- **`--target_dir`:** *(Optional)* Specify where you wish to install Freqtrade
    - ***Defaults to:** The current directory*
- **`--branch`:** *(Optional)* Specify the Freqtrade branch you wish to install
    - ***Defaults to:** The `develop` branch, can also be `stable` branch for less bleeding edge but generally more stable version*
- **`--commit`:** *(Optional)* Specify a specific Freqtrade commit you wish to utilize *(Can be a specific commit or `latest`)*
    - ***Defaults to:** The latest supported / recommended commit for MoniGoMani*


### `mgm-hurry install_mgm`
Individual command to install & update MoniGoMani.
#### Options
- **`--target_dir`:** *(Optional)* Specify where you wish to install MoniGoMani
    - ***Defaults to:** The current directory*
- **`--branch`:** *(Optional)* Specify the MoniGoMani branch you wish to install
    - ***Defaults to:** The `development` branch, can also be `main` branch for less bleeding edge but generally more stable version*
- **`--commit`:** *(Optional)* Specify a specific MoniGoMani commit you wish to utilize *(Can be a specific commit or `latest`)*
    - ***Defaults to:** The latest MoniGoMani commit*


### `mgm-hurry setup`
Setup command, launches an interactive wizard which lets you configure Freqtrade & MoniGoMani.


### `mgm-hurry cleanup`
Cleans up HyperOpt Result `.json` files so you can easily start a fresh HyperOpt.


### `mgm-hurry download_static_pairlist`
Retrieve and apply a current **Top-Volume-StaticPairList.json** file *(Using [RetrieveTopVolumeStaticPairList.json](https://github.com/Rikj000/MoniGoMani/blob/development/user_data/mgm_tools/RetrieveTopVolumeStaticPairList.json))*.
The retrieved StaticPairList contains the top X pairs with the most trading volume at that point in time.
#### Options
- **`--stake_currency`:** The stake currency to find the list of.
    - ***Defaults to:** Value in `.hurry` or `USDT`*
- **`--exchange`:** The exchange to read the data from.
    - ***Defaults to:** Value in `.hurry` or `binance`*
- **`--pairlist_length`:** Amount of pairs wish to use in your pairlist.
    - ***Defaults to:** Prompts you for the amount*
- **`--min_days_listed`:** The minimal days that coin pairs need to be listed on the exchange.
    - ***Defaults to:** Defaults to the amount of days in between now and the start of the timerange in `.hurry` minus the `startup_candle_count`.*


### `mgm-hurry download_candle_data`
Downloads candle data for a given timerange with the aid of an interactive prompt.
#### Option
- **`--timerange`:** *(Optional)* Specify the timerange for which you want to download candle data
    - Needs to be of the format `--timerange=yyyymmdd-yyyymmdd` or `--timerange=down/side/up`
    - ***Defaults to:** The `timerange` defined in your `.hurry` file.*


### `mgm-hurry hyperopt`
[HyperOpt](https://www.freqtrade.io/en/latest/hyperopt/) *(HyperSpace Parameter Optimization, a form of machine learning)* magic that will make your life easier!
Runs HyperOpt process to find out the most positive settings.
#### Options
- **`--timerange`:** *(Optional)* Specify the timerange upon which you want to HyperOpt
    - Needs to be of the format `--timerange=yyyymmdd-yyyymmdd` or `--timerange=down/side/up`
    - ***Defaults to:** The `timerange` defined in your `.hurry` file.*
- **`--strategy`:** *(Optional)* Specify the Strategy which you want to HyperOpt
    - **Defaults to:** The `strategy` defined in the `hyperopt` section of your `.hurry` file.
- **`--loss`:** *(Optional)* Specify the [HyperOptLoss](https://monigomani.readthedocs.io/Docs-HyperOptLoss-Functions) which you want to use during HyperOpting
    - **Defaults to:** The `loss` defined in the `hyperopt` section of your `.hurry` file.
- **`--spaces`:** *(Optional)* Specify the HyperOpt [spaces](https://www.freqtrade.io/en/latest/hyperopt/#running-hyperopt-with-smaller-search-space) which you want to use during HyperOpting (Example: `"buy sell stoploss"`)
    - **Defaults to:** The `spaces` defined in the `hyperopt` section of your `.hurry` file.
- **`--enable_protections`:** *(Optional)* Specify if HyperOpt should use [Protections](https://www.freqtrade.io/en/latest/includes/protections/)
    - **Defaults to:** `True`. Provide `False` to disable protections
- **`--random_state`:** *(Optional)* Specify the random state that HyperOpt will use.
    - This is needed to be able to get [reproducible results](https://www.freqtrade.io/en/latest/hyperopt/#reproducible-results) when doing comparison tests
- **`--apply_best_results`:** *(Optional)* Automatically apply the latest epoch found in the "best" HyperOpt Results table after a HyperOpt in the form of a `.json` file that the strategy will automatically load & use if found.
    - For MoniGoMani this will be the `mgm-hyperopt-results.json` file found in the `user_data` folder.
    - For other strategies this will be a `<strategy-name>.json` file found in the `user_data/strategies` folder
    - **Defaults to:** `True`. Provide `False` to disable automatic creation of a HyperOpt Results `.json` file.
- **`--clean_start`:** *(Optional)* Perform [`mgm-hurry cleanup`](#mgm-hurry-cleanup) before starting HyperOpt.
- **`--do_backtest`:** *(bool, Optional)* Do a BackTest after the HyperOpt?
    - **Defaults to:** True.
- **`--plot_stats`:** *(bool, Optional)* Plot a QuantStats report after the BackTest?
    - **Defaults to:** True.
- **`--importance_report`:** *(bool, Optional)* Calculate a Signal Importance Report for MoniGoMani after the HyperOpt?
    - **Defaults to:** True.
- **`--export_csv`:** *(bool, Optional)* Export the HyperOpt Results into a `.csv` SpreadSheet after the HyperOpt?
    - **Defaults to:** True.
- **`--output_file_name`:** *(Optional)* Custom filename for the `.log` file being created.
    - **Defaults to:** `HyperOptResults-<Strategy-Name>-<Current-DateTime>`
- **`--epochs`:** *(Optional)* Amount of epochs to HyperOpt over.
    - **Defaults to:** Value defined in `.hurry`
- **`--jobs`:** *(Optional)* Amount of parallel workers (CPU cores) to use
    - **Defaults to:** Automatic detection *(Amount used will depend on the amount of cores available on your system)*
- **`--min_trades`: Minimal amount of trades wished to be reached.
    - **Defaults to:** Not used.


### `mgm-hurry backtest`
Runs BackTest process to find out more about the results found by HyperOpt.
#### Options
- **`--timerange`:** *(Optional)* The target timerange for backtesting.
    - **Defaults to:** timerange in `.hurry`.
- **`--strategy`:** *(Optional)* Specify the Strategy which you want to BackTest
    - **Defaults to:** The `strategy` defined in the `hyperopt` section of your `.hurry` file.
- **`--enable_protections`:** *(Optional)* Whether or not to enable protections.
    - **Defaults to:** True.
- **`--output_file_name`:** *(Optional)* Custom name for the '.log' file being created.
    - **Defaults to:** Defaults to `BackTestResults-<Strategy-Name>-<Current-DateTime>`

### `mgm-hurry plot_stats`
Plot the stats report from a BackTest into detail html file.
#### Option
- **`--choose_results`:** *(Optional)* Launches a prompt to easily choose a certain backtest result file. If 'False' then the last BackTest result will be used.
    - **Defaults to:** 'True' mean an interactive prompt to choose a 'backtest-result-<timestamp>.json' file.
- **`--strategy`:** *(Optional)* Specify the Strategy of backTest result
    - **Defaults to:** The `strategy` defined in the `hyperopt` section of your `.hurry` file.
- **`--output_file_name`:** *(Optional)* Custom name for the `.html` file being created.
    - **Defaults to:** Defaults to `PlotProfitResults-<Strategy-Name>-<Current-DateTime>`


### `mgm-hurry importance_report`
Runs the TotalOverallSignalImportanceCalculator process to find out which signals reached more importance in your MoniGoMani results found by HyperOpt.
#### Option
- **`--output_file_name`:** *(Optional)* Custom name for the `.log` file being created.
    - **Defaults to:** Defaults to `SignalImportanceResults-MoniGoManiHyperStrategy-<Current-DateTime>`


### `mgm-hurry export_csv`
Export the `.fthypt` results to an easy to interpret/sort/filter `.csv` SpreadSheet.
#### Option
- **`--output_file_name`:** *(Optional)* Custom name for the `.csv` file being created.
    - **Defaults to:** Defaults to `CsvResults-<Strategy-Name>-<Current-DateTime>`
- **`--fthypt`:** *(Optional)* Launches a prompt to easily choose a certain `.fthypt` file or a specific `.fthypt` by providing it's name.
    - **Defaults to:** The last known `.fthypt` file. Provide `True` to launch a prompt to easily choose a specific. `.fthypt` file.


### `mgm-hurry hyperopt_show_epoch`
Prints & applies the HyperOpt Results for an epoch of choice.
#### Options
- **`--epoch`:** ***(Mandatory)*** Provide the epoch from which you wish to print the results.
- **`--strategy`:** *(Optional)* Strategy used
    - **Defaults to:** Value in `.hurry`.
- **`--apply`:** *(Optional)* Apply the printed HyperOpt Results
    - **Defaults to:** `True`. Provide `False` to only print the results
- **`--fthypt`:** *(Optional)* Launches a prompt to easily choose a certain `.fthypt` file or a specific `.fthypt` by providing it's name.
    - **Defaults to:** The last known `.fthypt` file. Provide `True` to launch a prompt to easily choose a specific. `.fthypt` file.


### `mgm-hurry hyperopt_show_results`
Launches a prompt to easily choose a certain `.fthypt` file to print epochs from.
#### Options
- **`--only_best`:** *(Optional)* Show only best epochs.
    - **Defaults to:** `True`. Provide `False` to disable filter.
- **`--only_profitable`:** *(Optional)* Show only profitable epochs.
    - **Defaults to:** `False`. Provide `True` to enable filter.


### `mgm-hurry start_trader`
Start the trader. Your ultimate goal!
#### Option
- **`--dry_run`:** *(Optional)* Run the trader in Dry-Run mode.
    - **Defaults to:** `True`. Provide `False` to run in Live-Run mode.


## Example timeranges
---
Here are some examples of timeranges for each different market type (bearish, bullish etc).

|Trend    |Timerange            |
|-------- |-------------------- |
|Downtrend| `20210509-20210524` |
|Uptrend  | `20210127-20210221` |
|Sidetrend| `20210518-20210610` |
|Final    | `20210425-20210610` |

## Developer Notes


### Virtual Environment
---

It's adviced to use an isolated environment for this project. (Probably each project)
Using `pipenv` makes this super easy.

```powershell
brew install pipenv
```

>Install pip packages from Pipfile in isolated environment

```powershell
pipenv install -d  # -d to install dev dependencies also
```

>Execute commands in the environment is as easy as `pipenv run <your command>`

### Continuous Integration
---

We use GitHub Actions online (and `pre-commit` local) to run CI procedures after each push and PR. It runs code styling checks and unit tests. To run these checks on your machine it is adviced to use `pre-commit`.


> Install `pre-commit` tool
Installing a git pre-commit hook as configured in `.pre-commit-config.yaml`

```powershell
brew install pre-commit
```
*Note; this example uses [Homebrew](https://brew.sh/) to install `pre-commit` but you are free to use your preferred package manager.*

> Install the pre-commit script.
```powershell
pipenv run pre-commit install
```

> Run pre-commit only on files in current changeset.
```powershell
pipenv run pre-commit run
```

> Run pre-commit on all files in the repo.
```powershell
pipenv run pre-commit run -a
```

### Module headers
---

To generate a module header (ascii art), you need to run the following command:

```powershell
$ python3
$ from art import tprint
$ tprint("Whatever you want")
```

Copy and paste the ASCII art output 🍻
