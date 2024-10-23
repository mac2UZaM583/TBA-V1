import numpy as np
import pandas as pd

def g_klines_splitting(klines):
    return pd.DataFrame({
        'close': klines[:, 4],
        'high': klines[:, 2],
        'low': klines[:, 3],
    })

def g_df_range_create(
    data,
    columns,
    range_,
    replace,
):
    def g_df_fill(
        data,
        columns,
        value=np.nan
    ):
        for column in columns:
            data[column] = value
        return data

    data = g_df_fill(data, columns)
    for i in range(len(range_)):
        data.loc[range_[i], columns[i]] = replace[i]
    return data
