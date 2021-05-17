<p align="left">
    <a href="https://discord.gg/xFZ9bB6vEz">
        <img src="https://img.shields.io/discord/819237123009150977?label=Discord%20Server&logo=discord" alt="Join CryptoStonksShallRise on Discord">
    </a>
        <a href="https://github.com/Rikj000/MoniGoMani/releases">
        <img src="https://img.shields.io/github/downloads/Rikj000/MoniGoMani/total?label=Total%20Downloads&logo=github" alt="Total Releases Downloaded from GitHub">
    </a>
    <a href="https://github.com/Rikj000/MoniGoMani/releases/latest">
        <img src="https://img.shields.io/github/v/release/Rikj000/MoniGoMani?include_prereleases&label=Latest%20Release&logo=github" alt="Latest Official Release on GitHub">
    </a>
    <a href="https://github.com/Rikj000/MoniGoMani/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Rikj000/MoniGoMani?label=License&logo=gnu" alt="GNU General Public License">
    </a>
    <a href="https://www.freqtrade.io/en/latest/">
        <img src="https://img.shields.io/badge/Trading%20Bot-Freqtrade-blue?logo=probot&logoColor=white" alt="Freqtrade - The open source crypto day-trading bot">
    </a>
        <a href="https://www.iconomi.com/register?ref=JdFzz">
        <img src="https://img.shields.io/badge/Join-ICONOMI-blue?logo=bitcoin&logoColor=white" alt="ICONOMI - The world’s largest crypto strategy provider">
    </a>
</p>

**<span style="color:darkorange">WARNING:</span> I am in no way responsible for your live results! This strategy is still experimental and under development!**   
**<span style="color:darkorange">WARNING:</span> MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) unless you really know what you are doing when manually allocating parameters!**   
**I strongly recommended to [re-optimize](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!**   
   
**<span style="color:blue">TIP:</span> Native installation is faster/better then a Docker VM, but Docker is easier to install**

# Very Quick Start (From Source Code):   
*Need a more detailed guide? Checkout the [**Official Freqtrade Installation Guide**](https://www.freqtrade.io/en/latest/installation/)!*    

1) Install [Git](https://git-scm.com/downloads)   
2) Open a terminal window and navigate to where you want to put `Freqtrade`   
3) Type `git clone https://github.com/freqtrade/freqtrade.git` to clone the Freqtrade repo    
4) Type `git checkout remotes/origin/develop` to switch to the development branch (MoniGoMani often uses some of the latest versions of Freqtrade)   
5) Type `./setup.sh -i` to install Freqtrade from scratch   
6) Type `source ./.env/bin/activate` to activate your virtual environment (Needs to be done every time you open the terminal)   
7) *(Type `./setup.sh -u` to update freqtrade with git pull)*   
8) *(Type `./setup.sh -r` to hard reset the branch)*   
9) [Download](https://github.com/Rikj000/MoniGoMani/releases) the latest `MoniGoMani` release and unzip it in the `Freqtrade` folder. Or clone the `main` branch through git & copy the files over.   
10) Type `freqtrade install-ui` to install FreqUI   
11) Follow step 3 from the *Very Quick Start (With Docker)* below   

That's it you successfully set up Freqtrade natively, connected to Telegram, with FreqUI!   
You can now start using `MoniGoManiHyperStrategy` for hyperopting/backtesting/dry/live-running! Congratulations :partying_face:   
Please read the [MGM_DOCUMENTATION](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md) to learn how to use it properly!   

# Very Quick Start (With Docker):   
*Need a more detailed guide? Checkout the [**Official Freqtrade Docker Quickstart**](https://www.freqtrade.io/en/stable/docker_quickstart/)!*    

1) [Download](https://github.com/Rikj000/MoniGoMani/releases) the latest `MoniGoMani` release and unzip it somewhere. Or clone the `main` branch through git.
2) Install [Docker Desktop](https://www.docker.com/get-started)
3) Open and edit `MoniGoMani/user_data/config-private.json` & `MoniGoMani/user_data/config.json`   
([VSCodium](https://vscodium.com/) is open source and comes pre-installed with good color codes to make it easier to read `.json` or `.log` files, and many more too)   
    3.A. Follow [these 4 easy steps](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) to create your own Telegram bot and fetch it's api-token, fill `token` under `telegram` up in `config-private.json` with this. Make sure to start a conversation with your bot before continuing!   
    3.B. Say `/start` to `@userinfobot` on Telegram to get your Chat ID, fill `chat_id` under `telegram` up in `config-private.json` with this.   
    3.C. Generate a strong key/password for `jwt_secret_key` under `api_server` in `config-private.json`   
    3.D. Choose and fill in a `username` and strong `password` also under `api_server` in `config-private.json`   
4) Open a terminal window and navigate to where you put `MoniGoMani` and type on of the following:   
    - `docker-compose pull` to pull in any updates to the Image if there are any
    - `docker-compose up --build` to build and start the bot & view its log or   
    - `docker-compose up -d`  to build and start the bot in the background.   
    - `docker-compose stop` to stop the bot.   
5) When running the included compose file FreqUI is already included and can be accessed from localhost:8080, 
   login is possible using the `username` and `password` from step 3.D.

That's it you successfully set up Freqtrade through Docker, connected to Telegram, with FreqUI!   
You can now start using `MoniGoManiHyperStrategy` for hyperopting/backtesting/dry/live-running! Congratulations :partying_face:   
Please read the [MGM_DOCUMENTATION](https://github.com/Rikj000/MoniGoMani/blob/main/MGM_DOCUMENTATION.md) to learn how to use it properly!   