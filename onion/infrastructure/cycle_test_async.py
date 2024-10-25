
from onion.app.infrastructure.g_df_test import g_df_test
from onion.app.domain.g_.global_ import g_symbols_f

import numpy as np
import pandas as pd
import asyncio

async def cycle_tests(symbols):
    await asyncio.gather(*[
        g_df_test(symbol)
        for symbol in symbols
    ])

