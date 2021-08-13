#!/bin/bash
#
##################
#
# Usage: curl -s "https://raw.githubusercontent.com/topscoder/MoniGoMani/feature/optimizations/mgm-launcher.sh" | bash
#
##################

MGM_GIT_REPO="https://github.com/topscoder/MoniGoMani.git"
MGM_GIT_BRANCH="feature/optimizations"
MGM_TARGET_FOLDER="monigomani"

##################

CYAN='\033[0;36m'
NC='\033[0m'

command -v python3 > /dev/null 2>&1

# Ensure that python3 is available
if [ $? -ne 0 ]; then
    echo -e "${CYAN}Python 3 is not available. Can't proceed. Sorry!"
    exit 1
fi

# Ensure that target folder doesn't exist
if [ -d "$MGM_TARGET_FOLDER" ]; then
    echo -e "${CYAN}Sorry, but target folder '$MGM_TARGET_FOLDER' already exists. Can't proceed. Sorry!"
    exit 1
fi

git clone -b $MGM_GIT_BRANCH $MGM_GIT_REPO $MGM_TARGET_FOLDER

cd "$MGM_TARGET_FOLDER"

python3 -m pip install --upgrade pip
# python3 -m pip install -r requirements-mgm-dev.txt # For developers who commit code.
python3 -m pip install -r requirements-mgm.txt # For every other user.


echo ""
echo -e "${CYAN}Thank you! We hope you enjoy your ride."
echo ""
echo -e "${CYAN}Get started with:${NC} python3 ./mgm-hurry up"
