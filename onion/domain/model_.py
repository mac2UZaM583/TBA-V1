from onion.domain.g_settings_bt import settings_ml
from onion.domain.utils import g_print_load

from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd

def g_y_train(
    data,
    feauture_main={"name": "RSI", "sell": 70, "buy": 30},
    features_add={}
):
    feauture_main["name"] = "INDCS/ " + feauture_main["name"]
    for key_, item_ in frozenset(features_add.items()):
        features_add["INDCS/ " + key_] = features_add.pop(key_)
    main_sell = data[feauture_main["name"]] > feauture_main["sell"]
    main_buy =  data[feauture_main["name"]] < feauture_main["buy"]

    if features_add:
        invert_func = lambda v, bool_: np.invert(v) if bool_ else v
        main_sell, main_buy = [
            np.logical_and(side, np.all(cond, axis=0))
            for side, cond in zip(
                (main_sell, main_buy),
                zip(*[[*cond] for cond in [
                    invert_func(
                        (
                            (data[feature] > thresholds[0]),
                            ((data[feature] < thresholds[1]) if thresholds[1] != None else (data[feature] > thresholds[0]))
                        ),
                        thresholds[2]
                    )
                    for feature, thresholds in features_add.items()
                ]])
            )
        ]
    return pd.Series(np.where(main_sell, -1, np.where(main_buy, 1, 0)))

def g_clean_x(x):
    return pd.DataFrame(
        SimpleImputer(strategy="mean")\
            .fit_transform(x.replace({-np.inf: np.nan, np.inf: np.nan})),
        columns=x.columns
    )

def g_train_test_split(x, y,):
    x = g_clean_x(x)
    return (lambda v, len_: [
        v[i][len_:] if i % 2 != 0
        else v[i][:len_]
        for i in range(4)
    ])((x, x, y, y), -1)

from itertools import count
@g_print_load()
def g_knn_predict(
    x_train,
    x_test,
    y_train,
    n_neighbors=3
):
    return KNeighborsClassifier(n_neighbors=n_neighbors)\
        .fit(x_train, y_train)\
        .predict(x_test)
