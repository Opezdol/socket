import asyncio
import os
import websockets
import json
from datetime import datetime

# My handcrafted classes
###########################
from data_input import Data
from db_model import Market, RelativeModel
from user_thread import User_Thread

######## My globbal constants #######
url = "wss://ws.okx.com:8443/ws/v5/public"
instrm_url = "https://www.okx.com/api/v5/public/instruments"
params = (
    "DASH-USDT",
    "LTC-USDT",
    "ADA-USDT",
    "ATOM-USDT",
    "DOGE-USDT",
    "ALGO-USDT",
    "BCH-USDT",
    "XRP-USDT",
    "DOT-USDT",
)
## TODO
## ADD%
## LTC/XPR ATOM/DOT ATOM/XRP LTC/BCH ATOM/BCH

relations = {
    ## dict[str:set]
    "LTC": {"ADA", "DASH", "ATOM", "DOGE", "ALGO", "XRP", "BCH"},
    "ATOM": {"ADA", "DOGE", "ALGO", "DOT", "XRP", "BCH"},
    "DASH": {"ADA", "DOGE", "ATOM", "ALGO"},
    "ADA": {"DOGE", "ALGO"},
}
######### Global def end ###########


async def subscribe(params: set, ws: websockets.WebSocketClientProtocol) -> None:
    req = [dict(channel="tickers", instId=name) for name in params]
    subs = dict(
        op="subscribe",
        args=req,
    )
    await ws.send(json.dumps(subs))
    async for msg in ws:
        print(msg)
        break


async def listen_market(m: Market) -> None:
    async with websockets.connect(url) as ws:
        # subscribe to SPOT channel
        await subscribe(m.pairs, ws)
        print(f"Connected: {datetime.now().isoformat()[11:19]}")
        # on recv messages
        async for msg in ws:
            data = Data().model_validate_json(msg)
            if data.data:
                message = data.data[0]
                # save value of recvd info to market snapshot
                m[message.key] = message.last
                # print(f"Key: {message.key}, value {message.last}")
                # print(m)


async def print_market(m: Market, r: RelativeModel) -> None:
    while True:
        r.fill(m)
        os.system("clear")
        print(r)
        await asyncio.sleep(2)


async def _user_raw() -> str:
    async for cmd in User_Thread():
        return cmd


async def get_user_cmd(r: RelativeModel) -> None:
    while True:
        cmd = await _user_raw()
        try:
            vctr = int(cmd)
            value = await _user_raw()
            r.fill_user(ind=vctr, value=float(value))
        except Exception as e:
            print(f"ERROR: {e} during conversion to intger @: self.get_user_cmd")
            if cmd == "q":
                r.save_user()
                loop = asyncio.get_running_loop()
                loop.stop()
                loop.close()
                print("Bye!")
            elif cmd == "c":
                r.clear_user()
                print("User values cleared!!")
            else:
                print("I dont know that command. ")


async def main():
    m = Market(pairs=params)
    r = RelativeModel(relations=relations)
    await asyncio.gather(listen_market(m), print_market(m, r), get_user_cmd(r))


asyncio.run(main())
