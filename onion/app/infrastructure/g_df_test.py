from onion.domain.g_settings_bt import settings_bt, settings_ml
from onion.domain.data_processing import g_df_range_create
from onion.app.domain.g_df_pack import g_df_pack

import numpy as np
import pickle
import os

# onion.domain
def g_df_save(
    symbol, 
    data, 
    dir="data_pack",
):
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(f"{dir}/{symbol}_data.pickle", "wb") as f:
        pickle.dump(data, f) 

async def g_df_test(symbol):
    def g_zeroing_out(
        qty=4,
        add=(),
        in_=0
    ):
        return (*np.full(qty, in_), *add)

    def g_avg_module():
        # the modular system allows me to
        # use implicit modification of variable values
        nonlocal\
            price_open_avg,\
            price_last,\
            price_last,\
            side_pos,\
            side_predict,\
            qty,\
            data

        qty_new =(
            (abs(price_open_avg / price_last - 1)
            * settings_bt["leverage"])
            * qty
            * settings_bt["avg_sttngs"]["power"]
        ) \
            * side_pos * side_predict \
            + qty
        price_open_avg = (
            (price_open_avg * qty) +
            (price_last * (qty_new - qty))
        ) / qty_new
        qty = qty_new
        data.loc[i, "BT"] = 2

    def g_sl_module():
        nonlocal\
            in_position,\
            balance,\
            qty,\
            data\

        balance -= qty
        (
            in_position,
            qty,
            data.loc[i, "BT"]
        ) = g_zeroing_out(qty=3)

    def g_tp_module():
        nonlocal\
            in_position,\
            balance,\
            qty,\
            data\

        balance += qty * settings_bt["tp"] * settings_bt["leverage"]
        (
            in_position,
            qty,
            data.loc[i, "BT"]
        ) = g_zeroing_out(qty=3)

    def g_close_module():
        nonlocal\
            in_position,\
            balance,\
            qty,\
            data\

        balance += qty * settings_bt["tp"] * settings_bt["leverage"]
        (
            in_position,
            qty,
            data.loc[i, "BT"]
        ) = g_zeroing_out(qty=3)

    def g_open_module():
        nonlocal\
            in_position,\
            balance,\
            qty,\
            data,\
            price_open_avg,\
            side_pos

        in_position = 1
        data.loc[i, "BT"] = in_position
        side_pos = side_predict
        price_open_avg = price_last
        qty = balance * settings_bt["balance_sttngs"]["used"]

    # data = await g_df_pack(symbol)
    data_pack = {}
    dir = "data_pack"
    for file in os.listdir(dir):
        with open(f"{dir}/{file}", "rb") as f:
            data_pack[file.rstrip(".pickle")] = pickle.load(f)
    data = data_pack[symbol + "_data"]
    data[["BT", "BT/ balance"]] = np.nan

    (
        in_position,
        side_pos,
        price_open_avg,
        qty,
        balance,
    ) = g_zeroing_out(add=(settings_bt["balance_sttngs"]["balance"],))

    for i, el in (
        lambda start_=settings_ml["klines_train_used"]: enumerate(
            data[["close", "predicted_label"]].iloc[start_:].values,
            start=start_
        )
    )():
        price_last, side_predict = el
        data.loc[i, "BT/ balance"] = balance

        if in_position:
            pnl_percent = price_open_avg / price_last - 1
            {
                # sl module
                (
                    qty >= (balance * settings_bt["sl"]) and
                    pnl_percent * settings_bt["leverage"] <= (-1)
                ): g_sl_module,

                # tp module
            all((abs(pnl_percent) >= settings_bt["tp"], (
                (pnl_percent > 0 > side_pos) or
                (side_pos > 0 > pnl_percent)
            ))): g_tp_module,

            # avg module
            (
                side_predict != 0 and
                not np.isnan(side_predict) and
                qty < balance * settings_bt["sl"]
            ): g_avg_module,

            # close module
            qty <= 0: g_close_module,
            }.get(True, lambda: 0)()
        elif (
            side_predict and
            not np.isnan(side_predict)
        ):
            g_open_module()
    
    g_df_save(symbol, data)
