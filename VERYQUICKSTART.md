# Very Quick Start Dry/Live-Running
1) [Download](https://github.com/Rikj000/MoniGoMani/releases) the latest `MoniGoMani` release and unzip it somewhere. Or clone the `main` branch through git.
2) Install [Docker Desktop](https://www.docker.com/get-started)
3) Open and edit `MoniGoMani/user_data/config-private.json` & `MoniGoMani/user_data/config.json`   
([VSCodium](https://vscodium.com/) is open source and comes pre-installed with good color codes to make it easier to read `.json` or `.log` files, and many more too)   
    3.A. Follow [these 4 easy steps](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) to create your own Telegram bot and fetch it's api-token, fill `token` under `telegram` up with this. Make sure to start a conversation with your bot   
    3.B. Say `/start` to `@userinfobot` on Telegram to get your Chat ID, fill `chat_id` under `telegram` up with this.   
    3.C. Generate a strong key/password for `jwt_secret_key` under `api_server`   
    3.D. Choose and fill in a `username` and `password` also under `api_server`   
4) Open a terminal window and navigate to where you put `MoniGoMani` and type on of the following:   
    - `docker-compose pull` to pull in any updates to the Image if there are any
    - `docker-compose up --build` to build and start the bot & view its log or   
    - `docker-compose up -d`  to build and start the bot in the background.   
    - `docker-compose stop` to stop the bot.   
5) When running the included compose file FreqUI is already included and can be accessed from localhost:8080, 
   login is possible using the `username` and `password` from step 3.D.

That's it you successfully set up Freqtrade, connected to Telegram, with FreqUI! Congratulations :partying_face:   

## Very Quick Start BackTesting/HyperOpting   
*(**For new [Auto-HyperOptable-Strategy](https://github.com/freqtrade/freqtrade/pull/4596) added in v0.8.0**, temporary instructions until merged into Freqtrade)*   
1) Open a terminal window and navigate to where you want to put `Freqtrade rk/hyper-strategy`
2) Type `git clone https://github.com/rokups/freqtrade/tree/rk/hyper-strategy` to clone the custom repo that contains the feature   
3) Type `git checkout remotes/origin/rk/hyper-strategy` to switch to the branch that contains the feature   
4) Type `./setup.sh -i` to install the custom freqtrade from scratch   
5) Type `source ./.env/bin/activate` to activate your virtual environment (Needs to be done every time you open the terminal)   
6) *(Type `./setup.sh -u` to update freqtrade with git pull)*   
7) *(Type `./setup.sh -r` to hard reset the branch)*   

That's it you successfully set up Freqtrade-HyperStrategy, you can now use the new `MoniGoManiHyperStrategy`! Congratulations :partying_face:   
Check the [Go-To Commands](https://github.com/Rikj000/MoniGoMani/blob/main/VERYQUICKSTART.md#go-to-commands) for how to use it.   

## Total Overall Signal Importance Calculator
Paste the `buy_params` & `sell_params` results from your HyperOpt over in the `/user_data/Total-Overall-Signal-Importance-Calculator.py` file.   
Then execute: `python ./user_data/Total-Overall-Signal-Importance-Calculator.py -sc BTC` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better! And now it will also export to a `importance.log` file in the same folder for easy sharing!  
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals!   
   
- Now you must fill in `-sc` or `--staking-currency` with the one you use in `config.json` as `stake_currency` since it really matters
- Optional fill in `-f` or `--file` to submit a custom file name for the log file to be exported
- Optional fill in `-nf` or `--no-file` if you don't want a log file to be exported   
   
## Some more good info
- [Freqtrade's official website](https://www.freqtrade.io/en/latest/) is **THE BEST** place to learn how to work with the bot! Be sure to check it out
- [Investopedia](https://www.investopedia.com/) is really a good site to learn how to interpret buy/sell signals, just look up the indicator you'd like to understand with the search icon in the top right.
- FreqUI is configured to run under `http://localhost:8080`   
- Your logs will come under `MoniGoMani/user-data/logs/`   
- `MoniGoMani/Some Test Results/` should always contains some test results from each release   
- All my HyperOpt Results so far can be found under `MoniGoMani/user-data/hyperopt_results/`   
- The actual Strategy files are under `MoniGoMani/user-data/strategies/` & The HyperOpt file under `MoniGoMani/user-data/hyperopts`   

## Go-To Commands:
For Hyper Opting *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py))*:
```bash
freqtrade hyperopt -c ./user_data/config.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all -s MoniGoManiHyperStrategy -e 1000 --timerange 20210101-20210316
```
For Hyper Opting *(the legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoMani.py) + legacy [MoniGoManiHyperOpt.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/hyperopts/MoniGoManiHyperOpt.py))*:
```bash
freqtrade hyperopt -c ./user_data/config.json -c ./user_data/config-private.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all --hyperopt MoniGoManiHyperOpt -s MoniGoMani -e 1000 --timerange 20210101-20210316
```
For Back Testing *(the new [MoniGoManiHyperStrategy.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperStrategy.py) or [MoniGoManiHyperOpted.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoManiHyperOpted.py) or legacy [MoniGoMani.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/strategies/MoniGoMani.py))*:
```bash
freqtrade backtesting -s MoniGoManiHyperStrategy -c ./user_data/config.json -c ./user_data/config-private.json --timerange 20210101-20210316
```
For Total Average Signal Importance Calculation *(with the [Total-Overall-Signal-Importance-Calculator.py](https://github.com/Rikj000/MoniGoMani/blob/main/user_data/Total-Overall-Signal-Importance-Calculator.py))*:
```bash
python ./user_data/Total-Overall-Signal-Importance-Calculator.py -sc BTC
```

**WARNING: MoniGoMani should always be HyperOpted unless you really know what you are doing when manually allocating weights!**   
**MoniGoManiHyperOpted already has a decent hyperopt applied to it!**   