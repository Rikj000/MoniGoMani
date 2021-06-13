#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import argparse
import json

import requests
# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

# Binance All Tradable Pairs Retriever
# ====================================
__author__ = 'PoCk3T & Rikj000'
__copyright__ = 'The GNU General Public License v3.0'
url = 'https://api2.binance.com/api/v3/exchangeInfo'


def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Binance All Tradable Pairs Retriever')
    parser.add_argument('-q', '--quote',
                        help=f'<Optional> Quote of the Binance pairs to retrieve (example, use "BTC" to retrieve all '
                             f'pairs like ADA/BTC, ETH/BTC, etc..); default is USDT', required=False, default='USDT')
    args = parser.parse_args()
    currency = args.quote

    resp = requests.get(url=url)
    data = resp.json()

    pairs_with_given_quote = \
        sorted(['/{}'.format(currency).join(str(d['symbol']).rsplit(currency, 1)) for d in data['symbols']
                if d['quoteAsset'] == currency
                and d['status'] == 'TRADING'
                and d['isSpotTradingAllowed'] is True
                # and d['isMarginTradingAllowed'] is True
                ])
    print(json.dumps(pairs_with_given_quote, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
