from onion.domain.g_settings_bt import settings_bt, settings_ml
from onion.domain.data_processing import g_df_range_create
from onion.app.domain.g_df_pack import g_df_pack

import numpy as np

def g_avg_module(
    price_open_avg,
    price_last,
    side_pos,
    side_predict,
    qty,
    qty_power,
    pnl_percent=None,
    balance=None,
    sl=None,
):
    qty_new =(
        (abs(price_open_avg / price_last - 1)
        * settings_bt["leverage"])
        * qty
        * qty_power
    ) \
        * side_pos * side_predict \
        + qty
    if qty_new == 0:
        print(qty)
    return (
        # qty
        qty_new,

        # price_open_avg
        ((price_open_avg * qty) + (price_last * (qty_new - qty))) / qty_new
    )

def g_df_test(dct):
    def g_zeroing_out(
        qty=4,
        add=(),
        in_=0
    ):
        return (*np.full(qty, in_), *add)

    data = g_df_pack()
    data[["BT", "BT/ balance"]] = np.nan

    (
        in_position,
        side_pos,
        price_open_avg,
        qty,
        balance,
    ) = g_zeroing_out(add=(settings_bt["balance_sttngs"]["balance"],))

    for i, el in (
        lambda start_=int(settings_ml["qty_klines"] * settings_ml["train_size"]): enumerate(
            data[["close", "predicted_label"]].iloc[start_:].values,
            start=start_
        )
    )():
        price_last, side_predict = el

        if in_position:
            pnl_percent = price_open_avg / price_last - 1

            # sl module
            if (
                qty >= (balance * settings_bt["sl"]) and
                pnl_percent <= (-100) / settings_bt["leverage"]
            ):
                print(i, "SL MODULE")
                in_position = 0
                balance -= qty
                qty = 0
                data.loc[i, "BT"] = in_position
                data.loc[i, "BT/ balance"] = balance
                continue

            # tp module
            if abs(pnl_percent) >= settings_bt["tp"]:
                if (pnl_percent > 0 > side_pos) or (side_pos > 0 > pnl_percent):
                    in_position = 0
                    balance += qty * settings_bt["tp"] * settings_bt["leverage"]
                    qty = 0
                    data.loc[i, "BT"] = in_position
                    data.loc[i, "BT/ balance"] = balance
                    continue

            # close module
            if qty <= 0:
                in_position = 0
                balance += qty * settings_bt["tp"] * settings_bt["leverage"]
                qty = 0
                data.loc[i, "BT"] = in_position
                data.loc[i, "BT/ balance"] = balance
                continue

            # avg module
            if side_predict:
                qty, price_open_avg = g_avg_module(
                    price_open_avg,
                    price_last,
                    side_pos,
                    side_predict,
                    qty,
                    settings_bt["avg_sttngs"]["power"],
                )
                data.loc[i, "BT"] = 2
                continue

            # print(i, qty, price_open_avg, price_last)
        elif side_predict and not np.isnan(side_predict):
            in_position = 1
            data.loc[i, "BT"] = in_position
            data.loc[i, "BT/ balance"] = balance
            side_pos = side_predict
            price_open_avg = price_last
            qty = balance * settings_bt["balance_sttngs"]["used"]

        data.loc[i, "BT/ balance"] = balance
    return data
