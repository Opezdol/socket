from sqlmodel import SQLModel
from datetime import datetime
from .point import POINT


class Tick(SQLModel):
    instId: str
    askPx: float
    askSz: float
    bidPx: float
    bidSz: float
    low24h: float
    high24h: float
    ts: datetime

    @property
    def name(self) -> POINT:
        return self.instId.split(sep="-")[0]

    @property
    def buy(self) -> float:
        return self.bidPx

    @property
    def sell(self) -> float:
        return self.askPx
