
<p align="center">
<img src="https://user-images.githubusercontent.com/86197446/123507408-6d624900-d669-11eb-9606-4a022bc4a117.png" width="300" height="289" align="center">
</p>

Hurry is a CLI tool to speed setting up [Freqtrade](https://www.freqtrade.io/en/stable/) with [MoniGoMani](https://github.com/Rikj000/MoniGoMani) HyperStrategy & co. Setting it all up requires some knowledge of the entire process, until you found Hurry 💨. You will get up and running (or, trading) in no time!

## Requirements

* Python 3.8+ is required
* Install required Python packages using the [PIP package manager](https://pip.pypa.io/en/stable/installing/):

```shell
  pip3 install -r https://raw.githubusercontent.com/topscoder/hurry-cli/master/requirements.txt
```

## Installation instructions

To install Hurry CLI:

```shell
  curl "https://raw.githubusercontent.com/topscoder/hurry-cli/master/hurry" --output hurry
```

### Pro tip

Add an alias in your shell config (eg. ~/.zshrc) so you can use Hurry as `hurry` everywhere :)

```shell
  alias hurry="python3 /path/to/hurry-cli/hurry"
```

Or, if you use [`fish-shell`](https://fishshell.com) than `hurry.fish` is your friend.
Copy `hurry.fish` to your fish functions folder (`~/.config/fish/functions/hurry.fish`) and you are ready to roll!

## Quick start

**Hurry up! Time is money**

Hurry includes an interactive wizard which guides you through the entire process of:

* Installing and configuring Freqtrade
* Installing and configuring MGM
* Configuring exchange API
* Configuring Telegram bot API
* Generating a static pairlist
* Downloading historic candle data for hyperopting and backtesting
* Running required hyperopt runs
* Backtesting your setup
* And finally start trading!

All you need to do is run:

``` shell
python3 hurry up
```

## Usage

```shell

  $ python3 hurry --help

  Usage: python3 hurry [command] [options]

  CLI tool for Freqtrade and MGM Hyper Strategy.

  Options:
    -h, --help    display help for command

  Commands:
    up
    install_freqtrade       [--branch=develop] [--target_dir=.]
    install_mgm             [--branch=development] [--target_dir=.]
    setup
    cleanup
    download_static_pairlist
    download_candle_data    [--timerange=yyyymmdd-yyyymmdd OR --timerange=down|up|side]
    hyperopt                [--timerange=yyyymmdd-yyyymmdd OR --timerange=down|up|side]
    hyperopt_show_results   [--only_best=True] [--only_profitable=False]
    hyperopt_show_epoch     num
    hyperopt_apply_epoch    num
    start_trader            [--dry_run=true]

```

### Examples

```shell
$ hurry up
 _                                       _  _
| |__   _   _  _ __  _ __  _   _    ___ | |(_)
| '_ \ | | | || '__|| '__|| | | |  / __|| || |
| | | || |_| || |   | |   | |_| | | (__ | || |
|_| |_| \__,_||_|   |_|    \__, |  \___||_||_|
                           |___/

1970-01-01 13:37:00 __main__[7594] DEBUG 👉 Freqtrade binary: `source ./.env/bin/activate; freqtrade`
1970-01-01 13:37:00 __main__[7594] WARNING 🤷‍♂️ No MGM installation found.
? 💨 Do you want to install Freqtrade? Yes
? 💨 Do you want to install MGM? Yes
? 💨 Do you want to configure it now? Yes
? 💨 Do you want to download candle data now? Yes
? 💨 Do you want to generate a static pairlist now? Yes
? 💨 Do you want to hyperopt now? Yes
? 💨 Do you want to backtest now? Yes
? 💨 Do you want to start trading? No

...

```

```shell
$ hurry setup
 _                                       _  _
| |__   _   _  _ __  _ __  _   _    ___ | |(_)
| '_ \ | | | || '__|| '__|| | | |  / __|| || |
| | | || |_| || |   | |   | |_| | | (__ | || |
|_| |_| \__,_||_|   |_|    \__, |  \___||_||_|
                           |___/

1970-01-01 13:37:00 __main__[6466] DEBUG 👉 Freqtrade binary: `source ./.env/bin/activate; freqtrade`
1970-01-01 13:37:00 __main__[6466] DEBUG 👉 MGM strategy and config found √
1970-01-01 13:37:00 __main__[6466] INFO 💨 💨 💨
1970-01-01 13:37:00 __main__[6466] INFO 👉 Setup
1970-01-01 13:37:00 __main__[6466] INFO 💨 💨 💨
1970-01-01 13:37:00 __main__[6466] INFO 🤓 Let's answer some questions to make your life easier.
? Which way you want to use Freqtrade? source
? Please enter the default timerange you want to use 20210127-20210221
? Which HyperOpt Strategy do you want to use? MoniGoManiHyperStrategy
? Which HyperOpt Loss do you want to use? WinRatioAndProfitRatioLoss
? Which spaces do you want to HyperOpt? ['buy', 'sell']
? Please enter the default quotation you want to use USDT
? Please enter the amount of epochs you want to HyperOpt 75
? Do you want to also setup your exchange? No
1970-01-01 13:37:00 __main__[6466] INFO 🍺 Configuration data written to .hurry file
? Do you want to also setup your Telegram bot?  No

...
```

## Development

Some developer notes. Never forget.

### Yapf formatting

```shell
yapf hurry --diff
yapf hurry > hurry.diff
yapf -i hurry
```

### Generate pydoc

```shell
python3 -m pydoc -w ./hurry
```

### Timerange examples

|Trend    |Timerange            |
|-----    |---------            |
|Downtrend| `20210509-20210524` |
|Uptrend  | `20210127-20210221` |
|Sidetrend| `20210518-20210610` |
|Final    | `20210425-20210610` |