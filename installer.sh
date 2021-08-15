#!/bin/bash
#
##################
#
# This file contains the installation procedure to get up and running with
# Freqtrade and the MoniGoMani HyperStrategy.
# 
# Usage: curl -s "https://raw.githubusercontent.com/topscoder/MoniGoMani/feature/optimizations/installer.sh" | bash
# Arguments (optional):
# -fr (freqtrade)
#
##################
# TODO: support arguments for branch and commit hash
# TODO: test at *nix and *indows


INSTALL_DIR="freqtrade-mgm"

FREQTRADE_REPO_URL="https://github.com/freqtrade/freqtrade.git"
FREQTRADE_BRANCH="develop"

MGM_REPO_URL="https://github.com/topscoder/MoniGoMani.git"
MGM_BRANCH="feature/optimizations"

##################

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
RED='\033[0;31m'
NC='\033[0m'

confirm() {
    local _prompt _default _response

    if [ "$1" ]; then _prompt="$1"; else _prompt="Are you sure?"; fi
    if [ "$2" ]; then _prompt="$_prompt $2"; else _prompt="$_prompt [y/n]"; fi

    # Loop forever until the user enters a valid response (Y/N or Yes/No).
    while true; do
        read -r -p "$_prompt " _response        
        case "$_response" in
        [Yy][Ee][Ss]|[Yy]) # Yes or Y (case-insensitive).
            REPLY="0"
            return $REPLY
            ;;
        [Nn][Oo]|[Nn])  # No or N.
            REPLY="1"
            return $REPLY
            ;;
        [Hh])  # H or h. H stands for Half.
            REPLY="2"
            return $REPLY
            ;;
        *) # Anything else (including a blank) is invalid.
            ;;
        esac
    done
}

echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
echo "${WHITE}  ⛱️  Welcome aboard! Let's get started ..."
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

# Ensure that python3 is installed
command -v python3 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED}  🙉  Python3 is not installed. Can't proceed. Sorry!"
    exit 1
fi

echo "${GREEN}  ✅  Python3 is installed."

# Ensure that git is installed
command -v git > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED}  🙉  Git is not installed. Can't proceed. Sorry!"
    exit 1
fi

echo "${GREEN}  ✅  Git is installed."

TEMP_DIR=$(mktemp -d /tmp/mgm.XXXXXXXXX)

echo ""
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  ⚙️  Downloading Freqtrade..."
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

# Figure out to overwrite install-folder or not.
INSTALL_FT="true"
if [ -d "$INSTALL_DIR" ]; then
    echo "${RED}  ⚠️  Target folder '$INSTALL_DIR' already exists."
    echo "${WHITE}      [y] to overwrite (Warning: '$INSTALL_DIR' will be truncated without another warning!)"
    echo "${WHITE}      [h] to continue, skip overwrite '$INSTALL_DIR'"
    echo "${WHITE}      [n] to cancel (You choose 🥚 for your 💰)"
    echo ""
    confirm "  👉  What do you want to do?" "(y/h/n)"
    echo ""

    if [ "$REPLY" == "0" ] # 0 = Yes
    then
        # Can't turn back times!
        echo "${WHITE}  🚮  Removing '$INSTALL_DIR' ... "
        rm -Rf "$INSTALL_DIR"
    fi

    if [ "$REPLY" == "1" ] # 1 = No
    then
        echo "      cancel."
        echo ""
        echo "${WHITE}  😽  KTHXBAI  "
        echo ""
        exit 1
    fi

    if [ "$REPLY" == "2" ] # 2 = Half
    then
        # Skip installing freqtrade
        INSTALL_FT="false"
    fi
fi

if [ "$INSTALL_FT" == "true" ]
then
    git clone -b "$FREQTRADE_BRANCH" "$FREQTRADE_REPO_URL" "$INSTALL_DIR"
else
    echo "${GREEN} SKIP."
fi

echo ""
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  ⚙️  Downloading MoniGoMani..."
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

git clone -b "$MGM_BRANCH" "$MGM_REPO_URL" "$TEMP_DIR"

install_files=(
    'mgm-hurry' 
    '.hurry'
    'user_data/mgm-config-private.example.json' 
    'user_data/mgm-config.example.json' 
    'user_data/hyperopts'       # entire directory
    'user_data/mgm_pair_lists'  # entire directory
    'user_data/mgm_tools'       # entire directory
    'user_data/strategies'
)

echo ""
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  ⚙️  Installing MoniGoMani Strategy..."
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

OVERWRITE_ALL="false"
USER_CHOSEN="false"

for mgm_file_entry in "${install_files[@]}";
do
    if [ -e "$mgm_file_entry" ]; 
    then 
        if [ "$USER_CHOSEN" == "false" ]; 
        then
            confirm "It looks like some of the MGM files already exist. Do you want to overwrite all?" "(y/n)"
        
            if [ "$REPLY" == "0" ]; # 0 = Yes
            then
                OVERWRITE_ALL="true"
            fi
        fi
        USER_CHOSEN="true"
    fi

    if [ "$OVERWRITE_ALL" == "true" ];
    then
        echo "  Copy $mgm_file_entry ... "

        # force overwrite
        cp -rf "$TEMP_DIR/$mgm_file_entry" "$INSTALL_DIR/$mgm_file_entry"    
    else
        # -i asks per file to overwrite or not
        cp -ri "$TEMP_DIR/$mgm_file_entry" "$INSTALL_DIR/$mgm_file_entry"
    fi
done

echo ""
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
echo "  🎉  ${CYAN}Freqtrade and MoniGoMani are installed! We hope you enjoy your ride."
echo "  🎉  ${CYAN}Get started with: ${YELLOW}python3 $INSTALL_DIR/mgm-hurry up"
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
