 # Very Quick Start Quide
1) [Download](https://github.com/Rikj000/MoniGoMani/releases) the latest `MoniGoMani` release and unzip it somewhere. Or clone the `main` branch through git.
2) Install [Docker Desktop](https://www.docker.com/get-started)
3) Open and edit `MoniGoMani/user_data/config.json`   
([VSCodium](https://vscodium.com/) is open source and comes pre-installed with good color codes to make it easier to read .json or .log files, and many more too)   

    2.A. Follow [these 4 easy steps](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) to create your own Telegram bot and fetch it's api-token, fill `token` under `telegram` up with this. Make sure to start a conversation with your bot  
    2.B. Say `/start` to `@userinfobot` on Telegram to get your Chat ID, fill `chat_id` under `telegram` up with this.   
    2.C. Generate a strong key/password for `jwt_secret_key` under `api_server`   
    2.D. Choose and fill in a `username` and `password` also under `api_server`   
4) Open a terminal window and navigate to where you put `MoniGoMani` and type `docker-compose up --build` to build and start the bot.
5) ~~Open a terminal window and navigate to where you put `FreqUI` and type `docker-compose build` to build the Docker container.   
When it's done building type `docker-compose up -d` to run it.~~ (This still assumes you cloned FreqUI seperately, MGM should soon be updated so FreqUI will be embedded into the same Docker container by default)

That's it you successfully setup Freqtrade, connected to Telegram, with FreqUI! Congratulations :partying_face:   

## Total Overall Signal Importance Calculator
Paste the `buy_params` & `sell_params` results from your HyperOpt over in the `/user_data/Total-Overall-Signal-Importance-Calculator.py` file.   
Then execute: `python ./user_data/Total-Overall-Signal-Importance-Calculator.py` from your favorite terminal / CLI to calculate the overall importance of the signals being used.   
The higher the score of a signal the better!   
Share these results in [#moni-go-mani-testing](https://discord.gg/xFZ9bB6vEz) so we can improve the signals, please don't forget to mention your `stake_currency`!   

## Some more good info
- [Freqtrade's official website](https://www.freqtrade.io/en/latest/) is **THE BEST** place to learn how to work with the bot! Be sure to check it out
- [Investopedia](https://www.investopedia.com/) is a really good site to learn how to interpret buy/sell signals, just look up the indicator you'd like to understand with the search icon in the top right.
- FreqUI is configured to run under `http://localhost:8081`   
- Your logs will come under `MoniGoMani/user-data/logs/`   
- `MoniGoMani/Some Test Results/` should always contains some test results from each release   
- All my HyperOpt Results so far can be found under `MoniGoMani/user-data/hyperopt_results/`   
- The actual Strategy files are under `MoniGoMani/user-data/strategies/` & The HyperOpt file under `MoniGoMani/user-data/hyperopts`   

## Go-To Commands:
For Hyper Opting:
```bash
freqtrade hyperopt --config ./user_data/config.json --hyperopt-loss SortinoHyperOptLossDaily --spaces all --hyperopt MoniGoManiHyperOpt --strategy MoniGoMani -e 1000 --timerange 20210101-20210316
```
For Back Testing:
```bash
freqtrade backtesting --strategy MoniGoManiHyperOpted --config ./user_data/config.json --timerange 20210101-20210316
```
For Total Signal Importance Calculator:
```bash
python ./user_data/Total-Overall-Signal-Importance-Calculator.py
```

**WARNING: MoniGoMani should always be HyperOpted unless you really know what you are doing when manually allocating weights!**   
**MoniGoManiHyperOpted already has a decent hyperopt applied to it!**   