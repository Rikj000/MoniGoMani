# Total Overall Signal Importance Calculator for MoniGoMani v0.8.0
# ----------------------------------------------------------------
# Paste the results from your HyperOpt over below `buy_params` & `sell_params` arrays
# Then execute: `python ./user_data/Total-Overall-Signal-Importance-Calculator.py` from your favorite
# terminal / CLI to calculate the overall importance of the signals being used.
# The higher the score of a signal the better

########################################################################################################################
#                                  START OF HYPEROPT BUY/SELL RESULTS COPY-PASTE SECTION                               #
########################################################################################################################

# Buy hyperspace params:
buy_params = {
    'buy___trades_when_downwards': True,
    'buy___trades_when_sideways': False,
    'buy___trades_when_upwards': True,
    'buy__downwards_trend_total_signal_needed': 2,
    'buy__sideways_trend_total_signal_needed': 29,
    'buy__upwards_trend_total_signal_needed': 19,
    'buy_downwards_trend_adx_strong_up_weight': 76,
    'buy_downwards_trend_bollinger_bands_weight': 94,
    'buy_downwards_trend_ema_long_golden_cross_weight': 55,
    'buy_downwards_trend_ema_short_golden_cross_weight': 32,
    'buy_downwards_trend_macd_weight': 18,
    'buy_downwards_trend_rsi_weight': 94,
    'buy_downwards_trend_sma_long_golden_cross_weight': 69,
    'buy_downwards_trend_sma_short_golden_cross_weight': 81,
    'buy_downwards_trend_vwap_cross_weight': 41,
    'buy_sideways_trend_adx_strong_up_weight': 15,
    'buy_sideways_trend_bollinger_bands_weight': 53,
    'buy_sideways_trend_ema_long_golden_cross_weight': 83,
    'buy_sideways_trend_ema_short_golden_cross_weight': 85,
    'buy_sideways_trend_macd_weight': 40,
    'buy_sideways_trend_rsi_weight': 1,
    'buy_sideways_trend_sma_long_golden_cross_weight': 80,
    'buy_sideways_trend_sma_short_golden_cross_weight': 63,
    'buy_sideways_trend_vwap_cross_weight': 65,
    'buy_upwards_trend_adx_strong_up_weight': 18,
    'buy_upwards_trend_bollinger_bands_weight': 61,
    'buy_upwards_trend_ema_long_golden_cross_weight': 18,
    'buy_upwards_trend_ema_short_golden_cross_weight': 81,
    'buy_upwards_trend_macd_weight': 48,
    'buy_upwards_trend_rsi_weight': 94,
    'buy_upwards_trend_sma_long_golden_cross_weight': 70,
    'buy_upwards_trend_sma_short_golden_cross_weight': 99,
    'buy_upwards_trend_vwap_cross_weight': 31
}
# Sell hyperspace params:
sell_params = {
    'sell___trades_when_downwards': False,
    'sell___trades_when_sideways': True,
    'sell___trades_when_upwards': True,
    'sell__downwards_trend_total_signal_needed': 11,
    'sell__sideways_trend_total_signal_needed': 41,
    'sell__upwards_trend_total_signal_needed': 87,
    'sell_downwards_trend_adx_strong_down_weight': 33,
    'sell_downwards_trend_bollinger_bands_weight': 21,
    'sell_downwards_trend_ema_long_death_cross_weight': 92,
    'sell_downwards_trend_ema_short_death_cross_weight': 96,
    'sell_downwards_trend_macd_weight': 1,
    'sell_downwards_trend_rsi_weight': 20,
    'sell_downwards_trend_sma_long_death_cross_weight': 62,
    'sell_downwards_trend_sma_short_death_cross_weight': 30,
    'sell_downwards_trend_vwap_cross_weight': 73,
    'sell_sideways_trend_adx_strong_down_weight': 43,
    'sell_sideways_trend_bollinger_bands_weight': 76,
    'sell_sideways_trend_ema_long_death_cross_weight': 72,
    'sell_sideways_trend_ema_short_death_cross_weight': 44,
    'sell_sideways_trend_macd_weight': 21,
    'sell_sideways_trend_rsi_weight': 24,
    'sell_sideways_trend_sma_long_death_cross_weight': 27,
    'sell_sideways_trend_sma_short_death_cross_weight': 86,
    'sell_sideways_trend_vwap_cross_weight': 60,
    'sell_upwards_trend_adx_strong_down_weight': 56,
    'sell_upwards_trend_bollinger_bands_weight': 1,
    'sell_upwards_trend_ema_long_death_cross_weight': 80,
    'sell_upwards_trend_ema_short_death_cross_weight': 72,
    'sell_upwards_trend_macd_weight': 46,
    'sell_upwards_trend_rsi_weight': 8,
    'sell_upwards_trend_sma_long_death_cross_weight': 18,
    'sell_upwards_trend_sma_short_death_cross_weight': 83,
    'sell_upwards_trend_vwap_cross_weight': 10
}

########################################################################################################################
#                                   END OF HYPEROPT BUY/SELL RESULTS COPY-PASTE SECTION                                #
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
    'adx_strong_down':-sc BTC
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
