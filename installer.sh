#!/bin/bash
#
##################
#
# Usage: curl -s "https://raw.githubusercontent.com/topscoder/MoniGoMani/feature/optimizations/installer.sh" | bash
#
##################
# FIXME: think about windows/unix/mac support

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

echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  Welcome aboard! Let's get started with Freqtrade and MoniGoMani ..."
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

# Ensure that python3 is installed
command -v python3 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED} Python 3 is not installed. Can't proceed. Sorry!"
    exit 1
fi

echo "${GREEN}  ✅ Python 3 is installed."

# Ensure that git is installed
command -v git > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "${RED}    Git is not installed. Can't proceed. Sorry!"
    exit 1
fi

echo "${GREEN}  ✅ Git is installed."
echo ""

TEMP_DIR=$(mktemp -d /tmp/mgm.XXXXXXXXX)

# Ensure that install folder doesn't exist
# FIXME: Or, shall we delete it in that case and re-install?
if [ -d "$INSTALL_DIR" ]; then
    echo "${RED}    Target folder '$INSTALL_DIR' already exists. Can't proceed, sorry!"
    exit 1
fi

echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  Downloading Freqtrade..."
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
git clone -b "$FREQTRADE_BRANCH" "$FREQTRADE_REPO_URL" "$INSTALL_DIR"

echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "${WHITE}  Downloading MoniGoMani..."
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
echo "${WHITE}  Installing MoniGoMani Strategy..."
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

for mgm_file_entry in "${install_files[@]}";
do
    # TODO
    # Check if target file already exists
    # Or check if target directory already exists
    # Ask to overwrite or not
    echo "  ... copy $mgm_file_entry"
    cp -r "$TEMP_DIR/$mgm_file_entry" "$INSTALL_DIR/$mgm_file_entry"
done

echo ""
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "   ${CYAN}Freqtrade and MoniGoMani are installed! We hope you enjoy your ride."
echo "   ${CYAN}Get started with:${WHITE} python3 $INSTALL_DIR/mgm-hurry up"
echo "${WHITE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
