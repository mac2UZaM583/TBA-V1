from onion.app.domain.g_.global_ import g_symbols_f
from onion.domain.g_settings_bt import settings_
from onion.infrastructure.cycle_test_async import cycle_tests
from onion.infrastructure.visual import g_report, g_visualize
from onion.app.domain.g_.global_ import g_symbols_f

import numpy as np
import asyncio

async def main():
    # from onion.app.domain.g_.global_ import g_symbols_f
    # print(asyncio.run(g_symbols_f()))

    data_pack = await cycle_tests(await g_symbols_f())
    # g_report(
    #     arrs_balance=[el["BT/ balance"] for el in data_pack.values()],
    #     arr_symbols=[symbol for symbol in data_pack]
    # )
    # data = data_pack["WAVESUSDT"]
    # g_visualize(
    #     x=data.index,
    #     y=data["close"],
    #     markers=(data["predicted_label"], data["BT"]),
    #     markers_settings=[
    #         (
    #             dict(
    #                 class_=-1,
    #                 color="rgb(202,73,73)",
    #                 name="Sell",
    #             ),
    #             dict(
    #                 class_=1,
    #                 color="rgb(74,138,139)",
    #                 name="Buy",
    #             )
    #         ),
    #         (
    #             dict(
    #                 class_=1,
    #                 color="rgb(114,115,203)",
    #                 name="in_position"
    #             ),
    #             dict(
    #                 class_=0,
    #                 color="rgb(180,88,58)",
    #                 name="not_in_position"
    #             ),
    #             # dict(
    #             #     class_=2,
    #             #     color="yellow",
    #             #     name="avg_order"
    #             # )
    #         ),
    #     ],
    #     # add=(
    #     #     dict(
    #     #         x=np.arange(data["BT/ balance"].count()),
    #     #         y=data["BT/ balance"].iloc[-data["BT/ balance"].count():],
    #     #         name="balance",
    #     #     ),
    #     # )
    # )
    from random import randint
    g_visualize(
        traces=tuple(
            dict(
                x=np.arange(data_pack[symbol]["BT/ balance"].count()),
                y=data_pack[symbol]["BT/ balance"].dropna(),
                name=symbol,
                line=dict(color=f"rgb{tuple([228] + [randint(58, 159) for _ in range(2)])}"),
            )
            for symbol in data_pack
        )
    )
    # print(data["BT/ balance"].iloc[-data["BT/ balance"].count():])
if __name__ == "__main__":
    asyncio.run(main())

# отображение изменение баланса по всем монетам из списка
#
