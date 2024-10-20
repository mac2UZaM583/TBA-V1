from onion.domain.session_ import session_

from asyncio import (
    run as arun,
    to_thread as ato_thread,
    gather as agather,
)
import numpy as np
from time import time

def g_klines(
    symbol,
    qty,
    interval=1,
    float_=True,
):
    async def async_g_klines():
        start = time() * 1000
        limits = np.append(np.full(qty // 1000, 1000), qty % 1000)
        data = np.concatenate(await agather(*(
            ato_thread(lambda i=i: session_.get_kline(
                category="linear",
                symbol=symbol,
                interval=interval,
                limit=limits[i],
                end=str(int(start - (i * 60_000_000)))
            )["result"]["list"])
            for i in range(len(limits))
            if limits[i] > 0
        )))[::-1]
        return np.float64(data) if float_ else data
    return arun(async_g_klines())
