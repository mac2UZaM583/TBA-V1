from onion.domain.g_settings_bt import settings_ml

from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd

def g_train_test_split(
    x,
    y,
    test=False,
    train_size=settings_ml["train_size"],
):
    cutback = np.max([
        index
        for column in x.columns
        for index in x[column].index[x[column].isna()]
    ]) + 1
    x = x[cutback:]
    y = y[cutback:]
    split_func = lambda v, len_: [
        v[i][len_:]
        if i % 2 != 0
        else v[i][:len_]
        for i in range(4)
    ]
    tple = (x, x, y, y)
    if test:
        return split_func(tple, int(len(x) * train_size))
    return split_func(tple, -1)

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
        # fill_func =
        main_sell, main_buy = [
            np.logical_and(side, np.all(cond, axis=0))
            for side, cond in zip(
                (main_sell, main_buy),
                zip(*[[*cond] for cond in [
                    invert_func((
                        (data[feature] > thresholds[0]),
                        ((data[feature] < thresholds[1]) if thresholds[1] != None else (data[feature] > thresholds[0]))
                    ), thresholds[2])
                    for feature, thresholds in features_add.items()
                ]])
            )
        ]
    return pd.Series(np.where(main_sell, -1, np.where(main_buy, 1, 0)))

def g_knn_predict(
    x_train,
    x_test,
    y_train,
    n_neighbors=3
):
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(x_train, y_train)
    return knn.predict(x_test)
