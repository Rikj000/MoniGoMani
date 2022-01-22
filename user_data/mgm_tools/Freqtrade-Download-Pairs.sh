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
EXCHANGES=(binance bitpanda coinex kraken)
QUOTECOINS=(ETH)

###
# define timeframes as string "5m 1h 1d"
# define days as int
###
TIMEFRAMES="5m 1h"
DAYS=1

###
# Parallel downloads - This, for now, is Kraken-only
# if you would like to tweak parallel downloads for Kraken, set this appropriately
# they rate limit by IP & quote pair, so even though they're quite aggressive on rate limits
# doing this in parallel by pair doesn't get rate limited IME, by default, one process per core
# since Kraken requires that the trade data is downloaded to generate candles > 720 but nprocs *2
# or even more parallelism is probably just fine on architectures like x64 with SMT, etc
#
# I have added this with a bit of thought towards allowing by-exchange parallelism if other exchanges
# have similar rate limiting, but this is outside my experience with other exchanges right now
###
PARALLEL_REQS_KRAKEN=`nproc`
PARALLEL_REQS_DEFAULT=1
PARALLEL_INSTALLED=1
if ! command -v parallel &> /dev/null
then
    PARALLEL_INSTALLED=0
    echo "GNU Parallel doesn't appear to be installed or in the PATH, parallel downloads will not be used"
    echo "Install GNU parallel (https://www.gnu.org/software/parallel/) to utilize parallel downloads when supported"
fi


### PID FILE CHECK NOT TO START ANOTHER DOWNLOAD ######################################################################
PIDFILE=/var/run/fqtpairdownloadeur.pid

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
. .env/bin/activate ; 

# loop through exchanges
for EXCHANGE in ${EXCHANGES[@]}
do
  # Kraken is odd, you need to dl-trades (see freqtrade's discussion on this in their download-data docs), check for this extra opt
  if [[ ${EXCHANGE,,} == *"kraken"* ]]
  then
    EXCHG_SPECIFIC_OPTS="--dl-trades"
    PARALLEL_REQS=${PARALLEL_REQS_KRAKEN}
  else
    PARALLEL_REQS=$PARALLEL_REQS_DEFAULT
  fi
  
  if [[ PARALLEL_REQS -gt 1  && PARALLEL_INSTALLED == 0 ]] 
  then
        echo "You have asked for $PARALLEL_REQS parallel downloads, but GNU Parallel doesn't appear to be installed"
        echo "or is not in the PATH, parallel downloads will not be used until this is fixed."
        echo "Install GNU parallel and ensure it is in the PATH (https://www.gnu.org/software/parallel/) to utilize parallel downloads when supported"
        PARALLEL_REQS=1
  fi
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
      if [[ ${PARALLEL_INSTALLED} == 1 ]]
      then
        jq -c -r '.[]' ${TMP_FILE} | parallel -j${PARALLEL_REQS} freqtrade download-data ${EXCHG_SPECIFIC_OPTS} --days ${DAYS} --timeframes ${TIMEFRAMES} --exchange ${EXCHANGE} --logfile ${LOG_FILE} --pairs {} 2>/dev/null
      else
        freqtrade download-data ${EXCHG_SPECIFIC_OPTS} --days ${DAYS} --timeframes ${TIMEFRAMES} --exchange ${EXCHANGE} --logfile ${LOG_FILE} --pair-file ${TMP_FILE}
      fi
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
