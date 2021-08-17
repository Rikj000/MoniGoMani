#!/bin/bash
#
##################
#
# This file contains the installation procedure to get up and running with
# Freqtrade and the MoniGoMani HyperStrategy.
# 
# Usage: sh <(curl -s "https://raw.githubusercontent.com/topscoder/MoniGoMani/feature/optimizations/installer.sh")
#
##################


usage() {

    cat << EOF

  Usage: 
    sh installer.sh [options]

  Example:
    sh installer.sh --dir="./targetdir" --ft_branch="feature/xyz" --mgm_commit="abcd1337"

  Optional options:
    -h, --help                    Show this help.

    --dir=<path>                  Path to directory to install Freqtrade with MGM. Will be created or overwritten when it's existing.

    --ft_url=<url>                URL to Git repository. (eg. https://github.com/freqtrade/freqtrade.git)
    --ft_branch=<branch>          Specific branch to checkout from Git repository. (eg. develop)
    --ft_commit=<commit hash>     Specific commit hash to checkout from Git repository. (note: will skip --ft_branch if set)

    --mgm_url=<url>               URL to Git repository. (eg. https://github.com/Rikj000/MoniGoMani.git)
    --mgm_branch=<branch>         Specific branch to checkout from Git repository. (eg. development)
    --mgm_commit=<commit hash>    Specific commit hash to checkout from Git repository. (note: will skip --mgm_branch if set)

EOF
    
    exit 0
}

# Default values
INSTALL_DIR="./freqtrade-mgm"

FREQTRADE_REPO_URL="https://github.com/freqtrade/freqtrade.git"
FREQTRADE_BRANCH="develop"
FREQTRADE_COMMIT=""

MGM_REPO_URL="https://github.com/topscoder/MoniGoMani.git"
MGM_BRANCH="feature/optimizations"
MGM_COMMIT=""

CWD=`pwd`

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        --dir=*)
        INSTALL_DIR="${arg#*=}"
        shift
        ;;
        --ft_url=*)
        FREQTRADE_REPO_URL="${arg#*=}"
        shift
        ;;
        --ft_branch=*)
        FREQTRADE_BRANCH="${arg#*=}"
        shift
        ;;
        --ft_commit=*)
        FREQTRADE_COMMIT="${arg#*=}"
        shift
        ;;

        --mgm_url=*)
        MGM_REPO_URL="${arg#*=}"
        shift
        ;;
        --mgm_branch=*)
        MGM_BRANCH="${arg#*=}"
        shift
        ;;
        --mgm_commit=*)
        MGM_COMMIT="${arg#*=}"
        shift
        ;;
        -h|--help)
        usage
        shift
        ;;
        *)
        echo ""
        echo "installer.sh -- illegal argument(s)"
        echo ""
        echo "="
        usage
        shift # Remove generic argument from processing
        ;;
    esac
done

##################

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
RED='\033[0;31m'
NC='\033[0m'

confirm() {
    local _prompt _default _response

    _prompt="Are you sure?"
    if [ "$1" ]; then _prompt="$1"; fi

    _prompt2="$_prompt [y/n]"
    if [ "$2" ]; then _prompt2="$_prompt $2"; fi

    # Loop forever until the user enters a valid response (Y/N or Yes/No).
    while true; do
        read -r -p "  $_prompt2 
        
  " _response        
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

do_exit() {
    echo "      cancel."
    echo ""
    echo "${WHITE}  😽  KTHXBAI  "
    echo ""
    exit 1
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

echo ""
echo "${WHITE}  What's the plan?"
echo "${WHITE}  ================"
echo ""
echo "${WHITE}  1) Install Freqtrade: (You will be able to skip overwriting)"
echo "${CYAN}       $FREQTRADE_REPO_URL => $INSTALL_DIR "
echo "${CYAN}       GIT BRANCH => $FREQTRADE_BRANCH "
echo "${CYAN}       GIT COMMIT => $FREQTRADE_COMMIT "
echo "${WHITE}  2) Install MoniGoMani HyperStrategy: (You will be able to skip overwriting each file separate)"
echo "${CYAN}       $MGM_REPO_URL => $INSTALL_DIR "
echo "${CYAN}       GIT BRANCH => $MGM_BRANCH "
echo "${CYAN}       GIT COMMIT => $MGM_COMMIT "
echo "${WHITE}"

confirm "Are you sure you want to continue?" "(y/n)"

if [ "$REPLY" == "1" ] # 1 = No
then
    do_exit
    exit 1
fi

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
        echo ""
        eval 'rm -Rf "$INSTALL_DIR"';
    fi

    if [ "$REPLY" == "1" ] # 1 = No
    then
        do_exit
    fi

    if [ "$REPLY" == "2" ] # 2 = Half
    then
        # Skip installing freqtrade
        INSTALL_FT="false"
    fi
fi

if [ "$INSTALL_FT" == "true" ]
then
    git clone -n "$FREQTRADE_REPO_URL" "$INSTALL_DIR"
    
    if [ "$FREQTRADE_COMMIT" != "" ]; then
        cd $INSTALL_DIR \
            && git checkout -b "detached_by_installer" "$FREQTRADE_COMMIT" \
            && cd $CWD
    else
        cd $INSTALL_DIR \
            && git checkout "$FREQTRADE_BRANCH" \
            && cd $CWD
    fi
else
    echo "${GREEN} SKIP."
fi

echo ""
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  ⚙️  Downloading MoniGoMani..."
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

TEMP_DIR=$(mktemp -d /tmp/mgm.XXXXXXXXX)

git clone -n "$MGM_REPO_URL" "$TEMP_DIR"

if [ "$MGM_COMMIT" != "" ]; then
    cd $TEMP_DIR \
        && git checkout -b "detached_by_installer" "$MGM_COMMIT" \
        && cd $CWD
else
    cd $TEMP_DIR \
        && git checkout "$MGM_BRANCH" \
        && cd $CWD
fi

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
echo "  🎉  ${CYAN}Get started with: ${YELLOW}cd $INSTALL_DIR && python3 ./mgm-hurry up"
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
