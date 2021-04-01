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
    '_downwards_trend_total_buy_signal_needed': 70,
    '_sideways_trend_total_buy_signal_needed': 35,
    '_upwards_trend_total_buy_signal_needed': 97,
    'downwards_trend_adx_strong_up_buy_weight': 47,
    'downwards_trend_bollinger_bands_buy_weight': 47,
    'downwards_trend_ema_long_golden_cross_buy_weight': 4,
    'downwards_trend_ema_short_golden_cross_buy_weight': 13,
    'downwards_trend_macd_buy_weight': 92,
    'downwards_trend_rsi_buy_weight': 64,
    'downwards_trend_sma_long_golden_cross_buy_weight': 94,
    'downwards_trend_sma_short_golden_cross_buy_weight': 37,
    'downwards_trend_vwap_cross_buy_weight': 41,
    'sideways_trend_adx_strong_up_buy_weight': 75,
    'sideways_trend_bollinger_bands_buy_weight': 40,
    'sideways_trend_ema_long_golden_cross_buy_weight': 37,
    'sideways_trend_ema_short_golden_cross_buy_weight': 74,
    'sideways_trend_macd_buy_weight': 30,
    'sideways_trend_rsi_buy_weight': 81,
    'sideways_trend_sma_long_golden_cross_buy_weight': 73,
    'sideways_trend_sma_short_golden_cross_buy_weight': 67,
    'sideways_trend_vwap_cross_buy_weight': 48,
    'upwards_trend_adx_strong_up_buy_weight': 98,
    'upwards_trend_bollinger_bands_buy_weight': 15,
    'upwards_trend_ema_long_golden_cross_buy_weight': 27,
    'upwards_trend_ema_short_golden_cross_buy_weight': 24,
    'upwards_trend_macd_buy_weight': 99,
    'upwards_trend_rsi_buy_weight': 1,
    'upwards_trend_sma_long_golden_cross_buy_weight': 62,
    'upwards_trend_sma_short_golden_cross_buy_weight': 82,
    'upwards_trend_vwap_cross_buy_weight': 79
}

# Sell hyperspace params:
sell_params = {
    '.trade_sells_when_downwards': True,
    '.trade_sells_when_sideways': True,
    '.trade_sells_when_upwards': False,
    '_downwards_trend_total_sell_signal_needed': 91,
    '_sideways_trend_total_sell_signal_needed': 79,
    '_upwards_trend_total_sell_signal_needed': 90,
    'downwards_trend_adx_strong_down_sell_weight': 42,
    'downwards_trend_bollinger_bands_sell_weight': 84,
    'downwards_trend_ema_long_death_cross_sell_weight': 85,
    'downwards_trend_ema_short_death_cross_sell_weight': 75,
    'downwards_trend_macd_sell_weight': 12,
    'downwards_trend_rsi_sell_weight': 0,
    'downwards_trend_sma_long_death_cross_sell_weight': 12,
    'downwards_trend_sma_short_death_cross_sell_weight': 100,
    'downwards_trend_vwap_cross_sell_weight': 83,
    'sideways_trend_adx_strong_down_sell_weight': 19,
    'sideways_trend_bollinger_bands_sell_weight': 85,
    'sideways_trend_ema_long_death_cross_sell_weight': 45,
    'sideways_trend_ema_short_death_cross_sell_weight': 96,
    'sideways_trend_macd_sell_weight': 92,
    'sideways_trend_rsi_sell_weight': 13,
    'sideways_trend_sma_long_death_cross_sell_weight': 100,
    'sideways_trend_sma_short_death_cross_sell_weight': 34,
    'sideways_trend_vwap_cross_sell_weight': 13,
    'upwards_trend_adx_strong_down_sell_weight': 22,
    'upwards_trend_bollinger_bands_sell_weight': 95,
    'upwards_trend_ema_long_death_cross_sell_weight': 79,
    'upwards_trend_ema_short_death_cross_sell_weight': 20,
    'upwards_trend_macd_sell_weight': 56,
    'upwards_trend_rsi_sell_weight': 82,
    'upwards_trend_sma_long_death_cross_sell_weight': 41,
    'upwards_trend_sma_short_death_cross_sell_weight': 53,
    'upwards_trend_vwap_cross_sell_weight': 91
}

total_overall_buy_weights = {
    'adx_strong_up':
        buy_params["downwards_trend_adx_strong_up_buy_weight"] +
        buy_params["sideways_trend_adx_strong_up_buy_weight"] +
        buy_params["upwards_trend_adx_strong_up_buy_weight"],
    'bollinger_bands':
        buy_params["downwards_trend_bollinger_bands_buy_weight"] +
        buy_params["sideways_trend_bollinger_bands_buy_weight"] +
        buy_params["upwards_trend_bollinger_bands_buy_weight"],
    'ema_long_golden_cross':
        buy_params["downwards_trend_ema_long_golden_cross_buy_weight"] +
        buy_params["sideways_trend_ema_long_golden_cross_buy_weight"] +
        buy_params["upwards_trend_ema_long_golden_cross_buy_weight"],
    'ema_short_golden_cross':
        buy_params["downwards_trend_ema_short_golden_cross_buy_weight"] +
        buy_params["sideways_trend_ema_short_golden_cross_buy_weight"] +
        buy_params["upwards_trend_ema_short_golden_cross_buy_weight"],
    'macd':
        buy_params["downwards_trend_macd_buy_weight"] +
        buy_params["sideways_trend_macd_buy_weight"] +
        buy_params["upwards_trend_macd_buy_weight"],
    'rsi':
        buy_params["downwards_trend_rsi_buy_weight"] +
        buy_params["sideways_trend_rsi_buy_weight"] +
        buy_params["upwards_trend_rsi_buy_weight"],
    'sma_long_golden_cross':
        buy_params["downwards_trend_sma_long_golden_cross_buy_weight"] +
        buy_params["sideways_trend_sma_long_golden_cross_buy_weight"] +
        buy_params["upwards_trend_sma_long_golden_cross_buy_weight"],
    'sma_short_golden_cross':
        buy_params["downwards_trend_sma_short_golden_cross_buy_weight"] +
        buy_params["sideways_trend_sma_short_golden_cross_buy_weight"] +
        buy_params["upwards_trend_sma_short_golden_cross_buy_weight"],
    'vwap_cross':
        buy_params["downwards_trend_vwap_cross_buy_weight"] +
        buy_params["sideways_trend_vwap_cross_buy_weight"] +
        buy_params["upwards_trend_vwap_cross_buy_weight"]

}

total_overall_sell_weights = {
    'adx_strong_down':
        (sell_params["downwards_trend_adx_strong_down_sell_weight"] +
         sell_params["sideways_trend_adx_strong_down_sell_weight"] +
         sell_params["upwards_trend_adx_strong_down_sell_weight"]) / 3,
    'bollinger_bands':
        (sell_params["downwards_trend_bollinger_bands_sell_weight"] +
         sell_params["sideways_trend_bollinger_bands_sell_weight"] +
         sell_params["upwards_trend_bollinger_bands_sell_weight"]) / 3,
    'ema_long_death_cross':
        (sell_params["downwards_trend_ema_long_death_cross_sell_weight"] +
         sell_params["sideways_trend_ema_long_death_cross_sell_weight"] +
         sell_params["upwards_trend_ema_long_death_cross_sell_weight"]) / 3,
    'ema_short_death_cross':
        (sell_params["downwards_trend_ema_short_death_cross_sell_weight"] +
         sell_params["sideways_trend_ema_short_death_cross_sell_weight"] +
         sell_params["upwards_trend_ema_short_death_cross_sell_weight"]) / 3,
    'macd':
        (sell_params["downwards_trend_macd_sell_weight"] +
         sell_params["sideways_trend_macd_sell_weight"] +
         sell_params["upwards_trend_macd_sell_weight"]) / 3,
    'rsi':
        (sell_params["downwards_trend_rsi_sell_weight"] +
         sell_params["sideways_trend_rsi_sell_weight"] +
         sell_params["upwards_trend_rsi_sell_weight"]) / 3,
    'sma_long_death_cross':
        (sell_params["downwards_trend_sma_long_death_cross_sell_weight"] +
         sell_params["sideways_trend_sma_long_death_cross_sell_weight"] +
         sell_params["upwards_trend_sma_long_death_cross_sell_weight"]) / 3,
    'sma_short_death_cross':
        (sell_params["downwards_trend_sma_short_death_cross_sell_weight"] +
         sell_params["sideways_trend_sma_short_death_cross_sell_weight"] +
         sell_params["upwards_trend_sma_short_death_cross_sell_weight"]) / 3,
    'vwap_cross':
        (sell_params["downwards_trend_vwap_cross_sell_weight"] +
         sell_params["sideways_trend_vwap_cross_sell_weight"] +
         sell_params["upwards_trend_vwap_cross_sell_weight"]) / 3
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
