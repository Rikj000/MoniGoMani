<p align="left">
    <a href="https://matrix.to/#/+moni-go-mani:matrix.org">
        <img src="https://img.shields.io/matrix/MoniGoMani-Testing:matrix.org?label=Matrix%20Community&logo=matrix" alt="Join MoniGoMani on Matrix">
    </a> <a href="https://discord.gg/xFZ9bB6vEz">
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

## Requirements
Make sure that you have all the following available on your system before proceeding:

- [**Python3**](https://www.python.org/) - Python 3 is required.
- [**Pip3**](https://pypi.org/project/pip/) - Package manager to install & manage Python packages.
- [**Git**](https://git-scm.com/downloads) - Software version management
- [**cURL**](https://curl.se/) - Command line data transferring through URLs, usually already installed
- [**Expect**](https://core.tcl-lang.org/expect/index) - A tool for automating interactive applications
- [**TA-Lib**](https://github.com/mrjbq7/ta-lib) - Technical Analysis Library written in C
- [**VSCodium**](https://vscodium.com/) - *(Optional)* A light weight open-source IDE that comes pre-installed with good color codes to make it easier to read `.json` and `.log` files & many more great features.

#### Additional Debian & Ubuntu requirements:
- [**Switch `sh` to `bash`**](https://unix.stackexchange.com/a/442517) - Run `sudo dpkg-reconfigure dash`, this will ask whether you want dash to be the default system shell. Answer `No` (`Tab` then `Enter`) and bash will become the default instead.
- [**Python-venv**](https://pypi.org/project/virtualenv/) - The installer will prompt you how to install it on your version

#### Additional MacOS (BigSur) requirements:
- Install [brew](https://brew.sh/)
- Install xcode util 12.3
- Install `hdf5` - *`brew install hdf5`*
- Install `c-blosc` - *`brew install c-blosc`*
- Install `tables` - *`pip3 install tables`*

## Installation instructions
MoniGoMani provides an all-in-one setup tool. It will guide you through the entire installation procedure. Not only for MoniGoMani, but Freqtrade also. You want the entire package, right? You will be up & HyperOpting (or Dry/Live Running) in no time! 🤙

To run the `installer.sh`, just run the following command:
```powershell
/usr/bin/env sh <(curl -s "https://raw.githubusercontent.com/Rikj000/MoniGoMani/development/installer.sh")
```

### Shell Alias
Add an alias in the config file of your shell *(eg. `~/.bashrc`)*, then you can use MGM-Hurry everywhere as simply `mgm-hurry ...`! 😄
Without a shell alias you will be limited to only being able to use MGM-hurry in its installation folder with `python3 -m pipenv run python3 ./mgm-hurry ...` prefixed to it.

The `ìnstaller.sh` should ask you during the initial installation if you wish to add a shell alias.
If you did not add it through the installer then you can still manually add the shell alias by executing following commands:

- **For `bash`:**
    ```powershell
    # Replace '/path/to/installation/Freqtrade-MGM/'
    echo "mgm-hurry() { pushd /path/to/installation/Freqtrade-MGM/ &> /dev/null; python3 -m pipenv run python3 ./mgm-hurry "\$@"; popd &> /dev/null; }" >> ~/.bashrc
    ```
- **For `fish`:**
    ```powershell
    mkdir -p ~/.config/fish/functions/; touch ~/.config/fish/functions/mgm-hurry.fish;
    echo "function mgm-hurry" >> ~/.config/fish/functions/mgm-hurry.fish
    # Replace '/path/to/installation/Freqtrade-MGM/'
    echo "pushd /path/to/installation/Freqtrade-MGM/ &> /dev/null; python3 -m pipenv run python3 ./mgm-hurry \$argv; popd &> /dev/null;" >> ~/.config/fish/functions/mgm-hurry.fish
    echo "end" >> ~/.config/fish/functions/mgm-hurry.fish
    ```

For other shells you'll have to look up where it's config file is stored & add a similar alias there.

### After installation
After installation all you need to do to get started is run:
```powershell
mgm-hurry up
```

That's it you successfully installed `MoniGoMani` and/or `Freqtrade`!
You can now start using `MoniGoMani` for HyperOpting/BackTesting/Dry/Live-running! Congratulations 🎉
This is only the beginning though, now please read the [Docs-MoniGoMani.md](https://monigomani.readthedocs.io/Docs-MoniGoMani) & [Docs-MGM-Hurry.md](https://monigomani.readthedocs.io/Docs-MGM-Hurry) to learn how to use it properly!

### OS Support Priority list

1. **Linux/Unix** *(MoniGoMani is written on Linux, for Linux!)*
2. **MacOS** *(Thanks to topscoder and other MacOS users)*
3. **WSL** *(Because we have to give those Windows users something..)*
4. **Docker** *(Perhaps someday, but not at this point in time..)*
5. **Windows** *(Such a SpyWare infested OS will **never** receive support for this project!)*
