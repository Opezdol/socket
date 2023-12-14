# from .moneda import Pair
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json
import websockets
import asyncio


class Msg(BaseModel):
    ts: datetime
    instType: str
    instId: str
    last: float
    lastSz: float
    askPx: float
    askSz: float
    bidPx: float
    bidSz: float


class Data(BaseModel):
    event: str | None = None
    arg: dict | None = None
    data: list[Msg] | None = None


async def main():
    url = "wss://ws.okx.com:8443/ws/v5/public"
    params = [
        dict(channel="tickers", instId="DASH-USDT"),
        dict(channel="tickers", instId="LTC-USDT"),
        dict(channel="tickers", instId="ADA-USDT"),
        dict(channel="tickers", instId="ATOM-USDT"),
        dict(channel="tickers", instId="DOGE-USDT"),
        dict(channel="tickers", instId="ALGO-USDT"),
    ]
    async with websockets.connect(url) as ws:
        print(f"Connected: {datetime.now().isoformat()[11:19]}")
        subs = dict(
            op="subscribe",
            args=params,
        )
        last_ltc = 1
        last_dash = 1
        last_ada = 1
        last_atom = 1
        last_doge = 1
        last_algo = 1

        await ws.send(json.dumps(subs))
        async for msg in ws:
            # print(json.dumps(msg))
            # recived messages with Msg data shoud be send to sorting of monedas
            res = Data.model_validate_json(msg)
            if res.data:
                res = res.data[0]
                if res.instId == "DASH-USDT":
                    last_dash = res.last
                elif res.instId == "LTC-USDT":
                    last_ltc = res.last
                elif res.instId == "ATOM-USDT":
                    last_atom = res.last
                elif res.instId == "DOGE-USDT":
                    last_doge = res.last
                elif res.instId == "ALGO-USDT":
                    last_algo = res.last
                else:
                    print(f"_____________{res.ts.isoformat()[11:19]}__________")
                    print("__ LTC __ ")
                    print(f"My relation LTC/ ADA  {last_ltc/res.last:.2f}")
                    print(f"My relation LTC/ DASH {last_ltc/last_dash:.2f}")
                    print(f"My relation LTC/ ATOM {last_ltc/last_atom:.2f}")
                    print(f"My relation LTC/ DOGE {last_ltc/last_doge:.2f}")
                    print(f"My relation LTC/ ALGO {last_ltc/last_algo:.2f}")
                    print("__ DASH __ ")
                    print(f"My relation DASH/ ADA  {last_dash/res.last:.2f}")
                    print(f"My relation DASH/ DOGE {last_dash/last_doge:.2f}")
                    print(f"My relation DASH/ ATOM {last_dash/last_atom:.2f}")
                    print(f"My relation DASH/ ALGO {last_dash/last_algo:.2f}")
                    print("__ ADA __ ")
                    print(f"My relation ADA/ DOGE {res.last/last_doge:.2f}")
                    print(f"My relation ADA/ ALGO {res.last/last_algo:.2f}")
                    print("__ ATOM __ ")
                    print(f"My relation ATOM/ ADA  {last_atom/res.last:.2f}")
                    print(f"My relation ATOM/ DOGE {last_atom/last_doge:.2f}")
                    print(f"My relation ATOM/ ALGO {last_atom/last_algo:.2f}")


if __name__ == "__main__":
    asyncio.run(main())