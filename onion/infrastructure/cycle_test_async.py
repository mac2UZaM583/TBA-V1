from onion.app.infrastructure.g_df_test import g_df_test
from onion.app.domain.g_.global_ import g_symbols_f

import numpy as np
import pandas as pd
import asyncio

async def cycle_tests(symbols):
    tasks = {
        symbol: g_df_test(symbol)
        for symbol in \
        ["SUIUSDT", "ETHUSDT", "ATOMUSDT", "SAFEUSDT", "SANDUSDT", "UNIUSDT", "1INCHUSDT"]
        # symbols
    }
    return {
        symbol: result
        for symbol, result in zip(tasks.keys(), (await asyncio.gather(*tasks.values())))
    }
