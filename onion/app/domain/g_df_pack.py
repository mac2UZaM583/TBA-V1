from onion.domain.indicators import g_indicators_data
from onion.domain.data_processing import g_klines_splitting, g_df_range_create
from onion.domain.model_ import (
    g_y_train,
    g_train_test_split,
    g_knn_predict
)
from onion.domain.g_settings_bt import settings_ml
from onion.app.domain.g_.global_ import g_klines

def g_df_pack():
    data = g_indicators_data(
        g_klines_splitting(g_klines(
            "SUIUSDT",
            settings_ml["qty_klines"],
            float_=True
        )),
        in_need_l1={
            "RSI": dict(period=14,),
            "ADX": dict(period=14,),
            "CCI": dict(period=21,),
            "WT": dict(period=14,),
            "TSI": dict(period=14,),
        },
        in_need_l2={"LD": dict(bars_back=500,)},
    )
    x_train, x_test, y_train, y_test = g_train_test_split(
        data[[column for column in data.columns if "INDCS/ " in column]],
        g_y_train(
            data,
            feauture_main={"name": "RSI", "sell": 70, "buy": 30},
            features_add={
                "ADX": (20, 40, True),
                "TSI": (0.8, -0.8, False)
            }
        ),
        test=True,
    )
    return g_df_range_create(
        data=data,
        columns=["train_label", "predicted_label"],
        range_=(x_train.index, x_test.index),
        replace=(y_train, g_knn_predict(x_train, x_test, y_train,))
    )
