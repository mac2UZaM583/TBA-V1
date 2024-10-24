import numpy as np
import pandas as pd

def g_rsi(data, period=14):
    delta = data['close'].diff()
    return 100 - (100 / (
        1
        +
        (delta.where(delta > 0, 0))
            .rolling(window=period)
            .mean()
        /
        (-delta.where(delta < 0, 0))\
            .rolling(window=period)\
            .mean()\
            .replace(0, delta.mean())
    ))

def g_adx(data, period=14):
    atr = pd.DataFrame({
        'tr1': data["high"] - data["low"],
        'tr2': np.abs(data["high"] - data["close"].shift()),
        'tr3': np.abs(data["low"] - data["close"].shift())
    })\
        .max(axis=1)\
        .rolling(window=period)\
        .mean()
    low_diff, high_diff = map(lambda v: v.diff(), (data["low"], data["high"]))
    calculate_di = lambda v1, v2: 100 * (
        pd.Series(np.where((v1 > v2) & (v1 > 0), v1, 0))
            .rolling(window=period)
            .mean()
        / atr
    )
    minus_di = calculate_di(low_diff, high_diff)
    plus_di = calculate_di(high_diff, low_diff)

    return (100 * (np.abs(plus_di - minus_di) / (plus_di + minus_di)))\
        .rolling(window=period)\
        .mean()

def g_cci(data, period=20):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    sma = typical_price.rolling(window=period).mean()
    return (typical_price - sma) / (0.015 * (typical_price - sma)\
        .abs()\
        .rolling(window=period)\
        .mean())

def g_williams_r(data, period=14):
    highest_high = data["high"].rolling(window=period).max()
    return -100 * (highest_high - data["close"]) / (
        highest_high -
        data["low"]
            .rolling(window=period)
            .min()
    )

def g_tsi(data, period=14,):
    return data["close"]\
        .rolling(window=period)\
        .corr(pd.Series(np.arange(len(data["close"]))))

def g_lorentzian_distances(feature_arrs,bars_back,):
    return np.sum([
        feature_arr\
            .fillna(feature_arr.mean())\
            .rolling(window=bars_back)\
            .apply(lambda v: np.log(1 + np.abs(v.iloc[0] - v.iloc[-1])))
        for feature_arr in feature_arrs
    ], axis=0)

def g_indicators_data(
    data,
    in_need_l1={},
    in_need_l2={}
):
    choise_l1 = {
        "RSI": lambda: g_rsi(data, **in_need_l1["RSI"]),
        "ADX": lambda: g_adx(data, **in_need_l1["ADX"]),
        "CCI":lambda: g_cci(data, **in_need_l1["CCI"]),
        "WT": lambda: g_williams_r(data, **in_need_l1["WT"]),
        "TSI": lambda: g_tsi(data, **in_need_l1["TSI"])
    }
    choise_l2 = {
        "LD": lambda *args, **kwargs: g_lorentzian_distances(*args, **kwargs)
    }
    for el in in_need_l1:
        data[el] = choise_l1[el]()
    l1 = [data[el] for el in in_need_l1]
    for el in in_need_l2:
        data[el] = choise_l2[el](l1, **in_need_l2[el])
    return data.rename(columns={
        name: "INDCS/ " + name
        for name in list(in_need_l1.keys()) + list(in_need_l2.keys())
    })
