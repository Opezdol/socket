from datetime import datetime
from pydantic import BaseModel


class Tick(BaseModel):
    instId: str
    askPx: float
    askSz: float
    bidPx: float
    bidSz: float
    low24h: float
    high24h: float
    ts: datetime

    @property
    def name(self) -> str:
        return self.instId.split(sep="-")[0]

    @property
    def buy(self) -> float:
        return self.bidPx

    @property
    def sell(self) -> float:
        return self.askPx
