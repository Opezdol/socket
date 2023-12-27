from pydantic import BaseModel
from datetime import datetime


class Msg(BaseModel):
    # data of spot ticker
    ts: datetime
    instType: str
    instId: str
    last: float
    lastSz: float
    askPx: float
    askSz: float
    bidPx: float
    bidSz: float

    @property
    def key(self):
        return self.instId.split(sep="-")[0]


class Data(BaseModel):
    # input raw json data
    event: str | None = None
    arg: dict | None = None
    data: list[Msg] | None = None


# {"arg":{"channel":"tickers","instId":"ALGO-USDT"},"data":[{"instType":"SPOT","instId":"ALGO-USDT","last":"0.2308","lastSz":"294.627384","askPx":"0.2308","askSz":"14823.405652","bidPx":"0.2306","bidSz":"5400","open24h":"0.2341","high24h":"0.2428","low24h":"0.2264","sodUtc0":"0.2383","sodUtc8":"0.2377","volCcy24h":"4697011.3597649356","vol24h":"20004419.531701","ts":"1703581248404"}]}
# I can use it. It is genious
# https://jsontopydantic.com

# class Arg(BaseModel):
#     channel: str
#     instId: str
#
# class Datum(BaseModel):
#     instType: str
#     instId: str
#     last: str
#     lastSz: str
#     askPx: str
#     askSz: str
#     bidPx: str
#     bidSz: str
#     open24h: str
#     high24h: str
#     low24h: str
#     sodUtc0: str
#     sodUtc8: str
#     volCcy24h: str
#     vol24h: str
#     ts: str
#
#
# class Model(BaseModel):
#     arg: Arg
#     data: List[Datum]
