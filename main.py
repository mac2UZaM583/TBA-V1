from onion.app.domain.g_.global_ import g_symbols_f
from onion.domain.g_settings_bt import settings_
from onion.infrastructure.cycle_test_async import cycle_tests
from onion.infrastructure.visual import g_report, g_visualize
from onion.app.domain.g_.global_ import g_symbols_f

import numpy as np
import asyncio
import pickle
import pandas as pd
import os

async def main():

    await cycle_tests(["SUIUSDT", "ETHUSDT"])
    
    # func
    data_pack = {}
    dir = "data_pack"
    for file in os.listdir(dir):
        with open(f"{dir}/{file}", "rb") as f:
            data_pack[file.rstrip(".pickle")] = pickle.load(f)
            print(data_pack[file.rstrip(".pickle")].iloc[180_000:190_000]["BT/ balance"])
    
    # настроить получение данных отдельно из каждого файла и отображение на графике
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

if __name__ == "__main__":
    asyncio.run(main())
