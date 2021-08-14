<p align="left">
    <a href="https://matrix.to/#/+moni-go-mani:matrix.org">
        <img src="https://img.shields.io/matrix/MoniGoMani-Testing:matrix.org?label=Matrix%20Community&logo=matrix" alt="Join MoniGoMani on Matrix">
    </a> <a href="https://discord.gg/xFZ9bB6vEz">
        <img src="https://img.shields.io/discord/819237123009150977?label=Discord%20Server&logo=discord" alt="Join CryptoStonksShallRise on Discord">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases">
        <img src="https://img.shields.io/github/downloads/Rikj000/MoniGoMani/total?label=Total%20Downloads&logo=github" alt="Total Releases Downloaded from GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/releases/latest">
        <img src="https://img.shields.io/github/v/release/Rikj000/MoniGoMani?include_prereleases&label=Latest%20Release&logo=github" alt="Latest Official Release on GitHub">
    </a> <a href="https://github.com/Rikj000/MoniGoMani/blob/main/LICENSE">
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
 - This Framework & Strategy are still experimental and under heavy development. It is not recommended running it live at this moment.
 - Always make sure to understand & test your MoniGoMani configuration until you trust it, before even thinking about going live!
 - I am in no way responsible for your live results! You are always responsible for your own MoniGoMani configuration!
 - MoniGoMani should always be [re-optimized](https://github.com/Rikj000/MoniGoMani/blob/main/Documentation/Docs-MoniGoMani.md#how-to-optimize-monigomani) after doing manual changes!
 - You need to [optimized](https://github.com/Rikj000/MoniGoMani/blob/main/Documentation/Docs-MoniGoMani.md#how-to-optimize-monigomani) your own copy of MoniGoMani while thinking logically, don't follow your computer blindly!
<hr>
   
**<span style="color:blue">TIP:</span> Native installation is recommended since MoniGoMani sometimes requires a specific Freqtrade commit. It's also faster/better than a Docker Container, but Docker is easier to install**   

## Requirements
Make sure that you have all of the following available on your system before proceeding:
- Python 3.8+ is required
- [Pip](https://pypi.org/project/pip/) *(Package manager to install & manage Python packages)*
- [Git](https://git-scm.com/downloads) *(Software version management)*
- [Jq](https://stedolan.github.io/jq/) *(Command-line `.json` processor)*
- [Curl](https://curl.se/) *(Command line data transferring through URLs)*
- [Docker](https://www.docker.com/get-started) *(If you really can't go for a source installation)*
- [VSCodium](https://vscodium.com/) *(Optional - A light weight open-source IDE that comes pre-installed with good color codes to make it easier to read `.json` and `.log` files & many more great features)*

# Very Quick Start:
*Need a more detailed guide? Checkout the [**Official Freqtrade Installation Guide**](https://www.freqtrade.io/en/latest/installation/)!*    


1) Install the required Python packages
    *(Command may vary a bit depending on your systems version of `python` & `pip`)*
    ```powershell
    pip3 install -r https://raw.githubusercontent.com/Rikj000/MoniGoMani/development/requirements.txt
    ```
2) Download `mgm-hurry` in the folder where you want to install `MoniGoMani` and/or `Freqtrade`
    ```powershell
    curl "https://raw.githubusercontent.com/Rikj000/MoniGoMani/development/mgm-hurry" --output "mgm-hurry"
    ```
3) Install & setup `MoniGoMani` and/or `Freqtrade`
    ```powershell
    python3 mgm-hurry up
    ```

That's it you successfully installed `MoniGoMani` and/or `Freqtrade`!
You can now start using `MoniGoMani` for HyperOpting/BackTesting/Dry/Live-running! Congratulations :tada:
This is only the beginning though, now please read the [Docs-MoniGoMani.md](https://github.com/Rikj000/MoniGoMani/blob/development/Documentation/Docs-MoniGoMani.md) & [Docs-MGM-Hurry.md](https://github.com/Rikj000/MoniGoMani/blob/development/Documentation/Docs-MGM-Hurry.md) to learn how to use it properly!

### Pro tip
Add an alias in the config file of your shell *(eg. ~/.zshrc)* so you can use MGM-Hurry as `mgm-hurry` without the need of pre-fixing Python in your commands anymore! :smile:
Following is a non-sticking example line, this needs to be added to your shell config:
```powershell
alias mgm-hurry="python3 /path/to/MoniGoMani/mgm-hurry"
```