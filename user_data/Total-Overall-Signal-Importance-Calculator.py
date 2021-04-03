# Total Overall Signal Importance Calculator for MoniGoMani v0.7.2
# ----------------------------------------------------------------
# Paste the results from your HyperOpt over below `buy_params` & `sell_params` arrays
# Then execute: `python ./user_data/Total-Overall-Signal-Importance-Calculator.py` from your favorite
# terminal / CLI to calculate the overall importance of the signals being used.
# The higher the score of a signal the better

# Buy hyperspace params:
buy_params = {
    '.trade_buys_when_downwards': True,
    '.trade_buys_when_sideways': False,
    '.trade_buys_when_upwards': True,
    '_downwards_trend_total_buy_signal_needed': 10,
    '_sideways_trend_total_buy_signal_needed': 58,
    '_upwards_trend_total_buy_signal_needed': 27,
    'downwards_trend_adx_strong_up_buy_weight': 70,
    'downwards_trend_bollinger_bands_buy_weight': 53,
    'downwards_trend_ema_long_golden_cross_buy_weight': 43,
    'downwards_trend_ema_short_golden_cross_buy_weight': 8,
    'downwards_trend_macd_buy_weight': 96,
    'downwards_trend_rsi_buy_weight': 33,
    'downwards_trend_sma_long_golden_cross_buy_weight': 43,
    'downwards_trend_sma_short_golden_cross_buy_weight': 96,
    'downwards_trend_vwap_cross_buy_weight': 88,
    'sideways_trend_adx_strong_up_buy_weight': 81,
    'sideways_trend_bollinger_bands_buy_weight': 17,
    'sideways_trend_ema_long_golden_cross_buy_weight': 67,
    'sideways_trend_ema_short_golden_cross_buy_weight': 90,
    'sideways_trend_macd_buy_weight': 62,
    'sideways_trend_rsi_buy_weight': 18,
    'sideways_trend_sma_long_golden_cross_buy_weight': 37,
    'sideways_trend_sma_short_golden_cross_buy_weight': 25,
    'sideways_trend_vwap_cross_buy_weight': 34,
    'upwards_trend_adx_strong_up_buy_weight': 1,
    'upwards_trend_bollinger_bands_buy_weight': 77,
    'upwards_trend_ema_long_golden_cross_buy_weight': 88,
    'upwards_trend_ema_short_golden_cross_buy_weight': 62,
    'upwards_trend_macd_buy_weight': 77,
    'upwards_trend_rsi_buy_weight': 84,
    'upwards_trend_sma_long_golden_cross_buy_weight': 59,
    'upwards_trend_sma_short_golden_cross_buy_weight': 93,
    'upwards_trend_vwap_cross_buy_weight': 72
}

# Sell hyperspace params:
sell_params = {
    '.trade_sells_when_downwards': False,
    '.trade_sells_when_sideways': True,
    '.trade_sells_when_upwards': False,
    '_downwards_trend_total_sell_signal_needed': 26,
    '_sideways_trend_total_sell_signal_needed': 89,
    '_upwards_trend_total_sell_signal_needed': 95,
    'downwards_trend_adx_strong_down_sell_weight': 51,
    'downwards_trend_bollinger_bands_sell_weight': 94,
    'downwards_trend_ema_long_death_cross_sell_weight': 37,
    'downwards_trend_ema_short_death_cross_sell_weight': 98,
    'downwards_trend_macd_sell_weight': 27,
    'downwards_trend_rsi_sell_weight': 31,
    'downwards_trend_sma_long_death_cross_sell_weight': 40,
    'downwards_trend_sma_short_death_cross_sell_weight': 63,
    'downwards_trend_vwap_cross_sell_weight': 19,
    'sideways_trend_adx_strong_down_sell_weight': 62,
    'sideways_trend_bollinger_bands_sell_weight': 0,
    'sideways_trend_ema_long_death_cross_sell_weight': 33,
    'sideways_trend_ema_short_death_cross_sell_weight': 29,
    'sideways_trend_macd_sell_weight': 51,
    'sideways_trend_rsi_sell_weight': 84,
    'sideways_trend_sma_long_death_cross_sell_weight': 22,
    'sideways_trend_sma_short_death_cross_sell_weight': 72,
    'sideways_trend_vwap_cross_sell_weight': 88,
    'upwards_trend_adx_strong_down_sell_weight': 3,
    'upwards_trend_bollinger_bands_sell_weight': 88,
    'upwards_trend_ema_long_death_cross_sell_weight': 33,
    'upwards_trend_ema_short_death_cross_sell_weight': 93,
    'upwards_trend_macd_sell_weight': 91,
    'upwards_trend_rsi_sell_weight': 23,
    'upwards_trend_sma_long_death_cross_sell_weight': 90,
    'upwards_trend_sma_short_death_cross_sell_weight': 17,
    'upwards_trend_vwap_cross_sell_weight': 30
}

########################################################################################################################
#                                             END OF COPY-PASTE SECTION                                                #
########################################################################################################################

trend_amount = 3

total_overall_buy_weights = {
    'adx_strong_up':
        (buy_params["downwards_trend_adx_strong_up_buy_weight"] +
         buy_params["sideways_trend_adx_strong_up_buy_weight"] +
         buy_params["upwards_trend_adx_strong_up_buy_weight"]) / trend_amount,
    'bollinger_bands':
        (buy_params["downwards_trend_bollinger_bands_buy_weight"] +
         buy_params["sideways_trend_bollinger_bands_buy_weight"] +
         buy_params["upwards_trend_bollinger_bands_buy_weight"]) / trend_amount,
    'ema_long_golden_cross':
        (buy_params["downwards_trend_ema_long_golden_cross_buy_weight"] +
         buy_params["sideways_trend_ema_long_golden_cross_buy_weight"] +
         buy_params["upwards_trend_ema_long_golden_cross_buy_weight"]) / trend_amount,
    'ema_short_golden_cross':
        (buy_params["downwards_trend_ema_short_golden_cross_buy_weight"] +
         buy_params["sideways_trend_ema_short_golden_cross_buy_weight"] +
         buy_params["upwards_trend_ema_short_golden_cross_buy_weight"]) / trend_amount,
    'macd':
        (buy_params["downwards_trend_macd_buy_weight"] +
         buy_params["sideways_trend_macd_buy_weight"] +
         buy_params["upwards_trend_macd_buy_weight"]) / trend_amount,
    'rsi':
        (buy_params["downwards_trend_rsi_buy_weight"] +
         buy_params["sideways_trend_rsi_buy_weight"] +
         buy_params["upwards_trend_rsi_buy_weight"]) / trend_amount,
    'sma_long_golden_cross':
        (buy_params["downwards_trend_sma_long_golden_cross_buy_weight"] +
         buy_params["sideways_trend_sma_long_golden_cross_buy_weight"] +
         buy_params["upwards_trend_sma_long_golden_cross_buy_weight"]) / trend_amount,
    'sma_short_golden_cross':
        (buy_params["downwards_trend_sma_short_golden_cross_buy_weight"] +
         buy_params["sideways_trend_sma_short_golden_cross_buy_weight"] +
         buy_params["upwards_trend_sma_short_golden_cross_buy_weight"]) / trend_amount,
    'vwap_cross':
        (buy_params["downwards_trend_vwap_cross_buy_weight"] +
         buy_params["sideways_trend_vwap_cross_buy_weight"] +
         buy_params["upwards_trend_vwap_cross_buy_weight"]) / trend_amount

}

total_overall_sell_weights = {
    'adx_strong_down':
        (sell_params["downwards_trend_adx_strong_down_sell_weight"] +
         sell_params["sideways_trend_adx_strong_down_sell_weight"] +
         sell_params["upwards_trend_adx_strong_down_sell_weight"]) / trend_amount,
    'bollinger_bands':
        (sell_params["downwards_trend_bollinger_bands_sell_weight"] +
         sell_params["sideways_trend_bollinger_bands_sell_weight"] +
         sell_params["upwards_trend_bollinger_bands_sell_weight"]) / trend_amount,
    'ema_long_death_cross':
        (sell_params["downwards_trend_ema_long_death_cross_sell_weight"] +
         sell_params["sideways_trend_ema_long_death_cross_sell_weight"] +
         sell_params["upwards_trend_ema_long_death_cross_sell_weight"]) / trend_amount,
    'ema_short_death_cross':
        (sell_params["downwards_trend_ema_short_death_cross_sell_weight"] +
         sell_params["sideways_trend_ema_short_death_cross_sell_weight"] +
         sell_params["upwards_trend_ema_short_death_cross_sell_weight"]) / trend_amount,
    'macd':
        (sell_params["downwards_trend_macd_sell_weight"] +
         sell_params["sideways_trend_macd_sell_weight"] +
         sell_params["upwards_trend_macd_sell_weight"]) / trend_amount,
    'rsi':
        (sell_params["downwards_trend_rsi_sell_weight"] +
         sell_params["sideways_trend_rsi_sell_weight"] +
         sell_params["upwards_trend_rsi_sell_weight"]) / trend_amount,
    'sma_long_death_cross':
        (sell_params["downwards_trend_sma_long_death_cross_sell_weight"] +
         sell_params["sideways_trend_sma_long_death_cross_sell_weight"] +
         sell_params["upwards_trend_sma_long_death_cross_sell_weight"]) / trend_amount,
    'sma_short_death_cross':
        (sell_params["downwards_trend_sma_short_death_cross_sell_weight"] +
         sell_params["sideways_trend_sma_short_death_cross_sell_weight"] +
         sell_params["upwards_trend_sma_short_death_cross_sell_weight"]) / trend_amount,
    'vwap_cross':
        (sell_params["downwards_trend_vwap_cross_sell_weight"] +
         sell_params["sideways_trend_vwap_cross_sell_weight"] +
         sell_params["upwards_trend_vwap_cross_sell_weight"]) / trend_amount
}

total_overall_weights = {
    'adx_strong_up_down':
        (total_overall_buy_weights["adx_strong_up"] + total_overall_sell_weights["adx_strong_down"]) / 2,
    'bollinger_bands':
        (total_overall_buy_weights["bollinger_bands"] + total_overall_sell_weights["bollinger_bands"]) / 2,
    'ema_long_golden_death_cross':
        (total_overall_buy_weights["ema_long_golden_cross"] + total_overall_sell_weights["ema_long_death_cross"]) / 2,
    'ema_short_golden_death_cross':
        (total_overall_buy_weights["ema_short_golden_cross"] + total_overall_sell_weights["ema_short_death_cross"]) / 2,
    'macd':
        (total_overall_buy_weights["macd"] + total_overall_sell_weights["macd"]) / 2,
    'rsi':
        (total_overall_buy_weights["rsi"] + total_overall_sell_weights["rsi"]) / 2,
    'sma_long_golden_death_cross':
        (total_overall_buy_weights["sma_long_golden_cross"] + total_overall_sell_weights["sma_long_death_cross"]) / 2,
    'sma_short_golden_death_cross':
        (total_overall_buy_weights["sma_short_golden_cross"] + total_overall_sell_weights["sma_short_death_cross"]) / 2,
    'vwap_cross':
        (total_overall_buy_weights["vwap_cross"] + total_overall_sell_weights["vwap_cross"]) / 2
}

initial_offset = 40
print("Total Overall Signal Importance:")
print("--------------------------------")
for signal, importance in total_overall_weights.items():
    offset = '{:<1s}{:>' + str(initial_offset - len(str(signal))) + 's}'
    print(offset.format(str(signal) + ":", str(round(importance, 2)) + "%"))
print("")
print("Total Overall Buy Signal Importance:")
print("------------------------------------")
for signal, importance in total_overall_buy_weights.items():
    offset = '{:<1s}{:>' + str(initial_offset - len(str(signal))) + 's}'
    print(offset.format(str(signal) + ":", str(round(importance, 2)) + "%"))
print("")
print("Total Overall Sell Signal Importance:")
print("-------------------------------------")
for signal, importance in total_overall_sell_weights.items():
    offset = '{:<1s}{:>' + str(initial_offset - len(str(signal))) + 's}'
    print(offset.format(str(signal) + ":", str(round(importance, 2)) + "%"))
