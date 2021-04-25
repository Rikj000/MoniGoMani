#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Binance all tradable pairs retriever """

# Binance all tradable pairs retriever
__author__ = "PoCk3T"
__copyright__ = "The GNU General Public License v3.0"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse
import json

import requests

url = 'https://api2.binance.com/api/v3/exchangeInfo'


def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Binance all tradable pairs retriever')
    parser.add_argument('-q', '--quote',
                        help='<Optional> Quote of the Binance pairs to retrieve (example, use "USDT" to retrieve all '
                             'pairs like LTC/USDT, ETH/USDT, etc..); default is BTC',
                        required=False, default="BTC")
    args = parser.parse_args()
    currency = args.quote

    resp = requests.get(url=url)
    data = resp.json()

    pairs_with_given_quote = sorted(
        ["/{}".format(currency).join(str(d['symbol']).rsplit(currency, 1)) for d in data['symbols'] if
         d['quoteAsset'] == currency and d['status'] == "TRADING" and d["isSpotTradingAllowed"] == True and d[
             'isMarginTradingAllowed'] == True])
    print(json.dumps(pairs_with_given_quote, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
