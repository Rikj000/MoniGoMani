#!/bin/bash
#
######################################################
#
# This file contains the installation procedure to get up and running with
# Freqtrade and the MoniGoMani HyperStrategy.
#
#######################################################
#
# Requirements
#  - Unix distro, macOS, or a POSIX compliant Windows WSL distro
#    (bash, command, mktemp, pwd, rm, sh, /dev/null)
#  - Python 3.8+
#  - Git
#  - Pip3 python package manager
#
# Windows Specific Notes
#   This script uses UNIX command line tools to run.
#   Please ensure you installed Windows Subsystem for Linux.
#   See: https://aka.ms/wslstore
#
#######################################################
#
# Usage
#   bash <(curl -s "https://raw.githubusercontent.com/Rikj000/MoniGoMani/development/installer.sh")
#
######################################################


usage() {

    cat << EOF

  Usage:
    bash installer.sh [options]

  Example:
    bash installer.sh --dir="./targetdir" --ft_branch="feature/xyz" --mgm_commit="abcd1337"

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
FREQTRADE_COMMIT="3503fdb4"

MGM_REPO_URL="https://github.com/Rikj000/MoniGoMani.git"
MGM_BRANCH="development"
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
echo ""
echo "${WHITE}  🚦  Requirements check"
echo "${WHITE}  ======================"
echo ""


# Ensure that python3 is installed
command -v python3 >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED}  🙉  Python3 is not installed. Can't proceed. See: https://realpython.com/installing-python/"
    exit 1
fi

echo "${GREEN}  ✅  Python3 is installed."

# Ensure that pip3 is installed
command -v pip3 >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED}  🙉  Pip3 is not installed. Can't proceed. See: https://pypi.org/project/pip/"
    exit 1
fi

echo "${GREEN}  ✅  Pip3 is installed."

# Ensure that git is installed
command -v git >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED}  🙉  Git is not installed. Can't proceed. See: https://gist.github.com/derhuerst/1b15ff4652a867391f03"
    exit 1
fi

echo "${GREEN}  ✅  Git is installed."
echo ""

confirm "👉  Are you ready to proceed?" "(y/n)"

if [ "$REPLY" == "1" ] # 1 = No
then
    do_exit
    exit 1
fi


echo ""
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  ⚙️  Downloading MGM-Hurry..."
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

git clone -n "$MGM_REPO_URL" "$INSTALL_DIR"

if [ "$MGM_COMMIT" != "" ]; then
    cd $INSTALL_DIR \
        && git checkout -b "detached_by_installer" "$MGM_COMMIT" \
        && cd $CWD
else
    cd $INSTALL_DIR \
        && git checkout "$MGM_BRANCH" \
        && cd $CWD
fi


echo ""
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  ⚙️  Installing MGM-Hurry..."
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

cd $INSTALL_DIR && \
    pip install -r requirements.txt && \
    python3 ./mgm-hurry up


echo ""
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
echo "  🎉  ${CYAN}You are all set! We hope you enjoy your ride."
echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
