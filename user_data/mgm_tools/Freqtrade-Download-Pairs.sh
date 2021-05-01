#!/bin/bash

###
# set your dirs accordingly
###
FQT_DIR="/opt/freqtrade"
LOG_DIR="${FQT_DIR}/user_data/logs"
TMP_DIR="/tmp"

###
# define exchanges as array (a b c)
# EXCHANGES=(binance coinex huobipro ftx gateio)
# define one ore more quotecoins as array (USDT ETH BTC)
# QUOTECOINS=(USDT ETH BTC)
###
EXCHANGES=(binance bitpanda coinex)
QUOTECOINS=(ETH)

###
# define timeframes as string "5m 1h 1d"
# define days as int
###
TIMEFRAMES="5m 1h"
DAYS=1

### PID FILE CHECK NOT TO START ANOTHER DOWNLOAD ######################################################################
PIDFILE=/var/run/fqtpairdownload.pid

if [ -f $PIDFILE ]
then
  PID=$(cat $PIDFILE)
  ps -p $PID > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    echo "another instance is already running"
    exit 1
  else
    ## Process not found assume not running
    echo $$ > $PIDFILE
    if [ $? -ne 0 ]
    then
      echo "Could not create PID file"
      exit 1
    fi
  fi
else
  echo $$ > $PIDFILE
  if [ $? -ne 0 ]
  then
    echo "Could not create PID file"
    exit 1
  fi
fi

### MAIN LOGIC  #######################################################################################################

# switch to freqtrade venv
cd ${FQT_DIR};
source .env/bin/activate ; 

# loop through exchanges
for EXCHANGE in ${EXCHANGES[@]}
do
  # loop through quote coins
  for COIN in ${QUOTECOINS[@]}
  do
    COIN=${COIN^^} # upcase it because its case sensitive!
    TMP_DATE=$(date +%s)
    TMP_FILE=${TMP_DIR}/${TMP_DATE}_${EXCHANGE}_${COIN}.json
    LOG_FILE=${LOG_DIR}/${TMP_DATE}_pair_download_${EXCHANGE}_${COIN}.log
    echo "listing ${EXCHANGE} ${COIN} pairs into ${TMP_FILE}"
    freqtrade list-pairs --exchange ${EXCHANGE} --quote ${COIN} --print-json > ${TMP_FILE} 2>/dev/null
    # sanity check, if json is empty (exchange under maintenance or wrong stakecoin)
    PAIR_COUNT=$(jq length ${TMP_FILE})
    if [[ $PAIR_COUNT -gt 1 ]]
    then
      echo "exchange ${EXCHANGE} has currently ${PAIR_COUNT} pairs for ${COIN} - starting download for timeframes = ${TIMEFRAMES}, days = ${DAYS}"
      START=$(date +%s)
      # >>> main magic! :)
      freqtrade download-data --pairs-file ${TMP_FILE} --days ${DAYS} --timeframes ${TIMEFRAMES} --exchange ${EXCHANGE} --logfile ${LOG_FILE} 2>/dev/null
      END=$(date +%s)
      DIFF=$(echo "${END} - ${START}" | bc)
      echo "exchange ${EXCHANGE} pair download for ${COIN} completed in ${DIFF}s"
    else
      echo "exchange ${EXCHANGE} has currently no pairs available for ${COIN}"
    fi
    # clear out temp json
    rm ${TMP_FILE}
  done 
done

# PID remove
rm $PIDFILE