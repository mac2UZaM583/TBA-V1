from onion.domain.session_ import session_
from onion.domain.g_settings_bt import settings_ml

from asyncio import (
    to_thread as aio_to_thread,
    gather as aio_gather,
    sleep as aio_sleep
)
import numpy as np
from time import time

async def g_klines(
    symbol,
    qty,
    interval=1,
    float_=True,
):
    start = time() * 1000
    limits = np.append(np.full(qty // 1000, 1000), qty % 1000)
    data = np.concatenate(await aio_gather(*(
        aio_to_thread(lambda i=i: session_.get_kline(
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

async def g_klines_symbols(
    symbols,
    *g_klines_args,
    **g_klines_kwargs,
):
    return np.array(await aio_gather(*[
        g_klines(*g_klines_args, **g_klines_kwargs,)
        for symbol in symbols
    ]))

async def g_symbols_f(
    volume_24=200_000,
    index_volatility_24=0.9,
    deviations=0.05,
):
    symbols_non_time =  np.array([
        el["symbol"]
        for el in session_.get_tickers(category="linear")["result"]["list"]
        if (
            (
                (float(el["lowPrice24h"]) + float(el["highPrice24h"])) / 2 * float(el["volume24h"]) >= volume_24 and
                abs(index_volatility_24 / (float(el["lowPrice24h"]) / float(el["highPrice24h"])) - 1) <= 0.05
            ) and
            "USDC" not in el["symbol"]
        )
    ])
    klines_week = int(settings_ml["klines_all"] / 60 / 24 / 7 * 1.3)
    klines_week = klines_week if klines_week > 1 else 2
    tasks = {
        symbol: aio_to_thread(lambda v=symbol: session_.get_kline(
            category="linear",
            interval="W",
            symbol=symbol,
            limit=klines_week
        )["result"]["list"])
        for symbol in symbols_non_time
    }
    symbols_plu = np.array([
        symbol
        for symbol, v_ in zip(tasks.keys(), (await aio_gather(*tasks.values())))
        if len(v_) >= klines_week and not print(len(v_), klines_week)
    ])
    # print(symbols_plu, klines_week)
    return symbols_plu
