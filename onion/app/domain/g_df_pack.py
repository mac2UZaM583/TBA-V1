from onion.domain.indicators import g_indicators_data
from onion.domain.data_processing import g_klines_splitting, g_df_range_create
from onion.domain.model_ import (
    g_y_train,
    g_train_test_split,
    g_knn_predict,
    g_clean_x
)
from onion.domain.g_settings_bt import settings_ml
from onion.app.domain.g_.global_ import g_klines, g_klines_symbols, g_symbols_f

from asyncio import (
    run as aiorun,
    gather as aiogather,
    create_task
)
import numpy as np
import pandas as pd
import pickle
    
def g_rolling_apply(
    arr, 
    window, 
    func,
):
    len_arr = len(arr)
    result = np.empty(len_arr)
    result[:window] = np.nan

    for i in range(window, len_arr):
        result[i] = func(arr[i-window:i])
    return result

async def g_df_pack(symbol):
    data = g_indicators_data(
        data=g_klines_splitting(await g_klines(
            symbol=symbol,
            float_=True,
            qty=settings_ml["klines_all"],
        )),
        in_need_l1={
            "RSI": dict(period=14,),
            "ADX": dict(period=14,),
            "CCI": dict(period=21,),
            "WT": dict(period=14,),
            "TSI": dict(period=14,),
        },
        in_need_l2={"LD": dict(bars_back=100,)},
    )
    data["train_label"] = g_y_train(
        data,
        feauture_main={"name": "RSI", "sell": 70, "buy": 30},
        features_add={
            "ADX": (20, 40, True),
            "TSI": (0.8, -0.8, False)
        }
    )
    indcs_colums = [column for column in data.columns if "INDCS" in column]
    data[indcs_colums] = g_clean_x(data[indcs_colums])
    data["predicted_label"] = g_rolling_apply(
        arr=data[indcs_colums + ["train_label"]],
        window=settings_ml["klines_train_used"],
        func=lambda v: g_knn_predict(
            x_train=v[indcs_colums].iloc[:-1].values,
            x_test=v[indcs_colums].iloc[-1].values.reshape(1, 6),
            y_train=v["train_label"].iloc[:-1].values,
        )
    )
    return data
