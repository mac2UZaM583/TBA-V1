from onion.domain.g_settings_bt import settings_
from onion.app.infrastructure.g_df_test import g_df_test
from onion.infrastructure.visual import g_visualize

import numpy as np

def main():
    # from onion.app.domain.g_.global_ import g_symbols_f
    # g_symbols_f()
    # все в цикле плю
    data = g_df_test(settings_)
    # print(data[["BT", "BT/ balance"]])

    g_visualize(
        x=data.index,
        y=data["close"],
        markers=(data["predicted_label"], data["BT"]),
        markers_settings=[
            (
                dict(
                    class_=-1,
                    color="red",
                    name="Sell",
                ),
                dict(
                    class_=1,
                    color="green",
                    name="Buy",
                )
            ),
            (
                dict(
                    class_=1,
                    color="blue",
                    name="in_position"
                ),
                dict(
                    class_=0,
                    color="pink",
                    name="not_in_position"
                ),
                # dict(
                #     class_=2,
                #     color="yellow",
                #     name="avg_order"
                # )
            ),
        ],
        # add=(
        #     dict(
        #         x=np.arange(data["BT/ balance"].count()),
        #         y=data["BT/ balance"].iloc[-data["BT/ balance"].count():],
        #         name="balance",
        #     ),
        # )
    )
    g_visualize(
        x=np.arange(data["BT/ balance"].count()),
        y=data["BT/ balance"].iloc[-data["BT/ balance"].count():],
    )
    # print(data["BT/ balance"].iloc[-data["BT/ balance"].count():])
if __name__ == "__main__":
    main()

# настроить pnl_percent
# отображение баланса
#
