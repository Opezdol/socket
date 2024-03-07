from datetime import datetime
import json
import websockets
import asyncio
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model.market import Market, RelativeModel
from model.tick import Tick


######## My globbal constants #######
url = "wss://ws.okx.com:8443/ws/v5/public"
instrm_url = "https://www.okx.com/api/v5/public/instruments"


async def print_market(m: Market, r: RelativeModel) -> None:
    while True:
        await asyncio.sleep(2)
        r.fill(m)
        print(m)
        print(r)


async def listen_market(m: Market) -> None:
    """Enter point of websocket connetion. Makes subscibe and fills
    Market._cache with data from dataflow in ws."""
    async with websockets.connect(url) as ws:
        # subscribe to SPOT channel
        await subscribe(m.get_keys(), ws)
        print(f"Connected: {datetime.now().isoformat()[11:19]}")
        # on recv messages
        async for msg in ws:
            dta = json.loads(msg)
            tick = Tick(**dta["data"][0])
            m[tick.name] = tick


async def subscribe(params: list[str], ws: websockets.WebSocketClientProtocol) -> None:
    req = [dict(channel="tickers", instId=name) for name in params]
    subs = dict(
        op="subscribe",
        args=req,
    )
    print(json.dumps(subs))
    await ws.send(json.dumps(subs))
    _ = len(params)
    i = 0

    async for msg in ws:
        print(msg)
        i += 1
        if i > _:
            break


async def run_cli():
    m = Market()
    r = RelativeModel()
    await asyncio.gather(listen_market(m), print_market(m=m, r=r))


if __name__ == "__main__":
    asyncio.run(run_cli())
