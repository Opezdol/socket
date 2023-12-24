import asyncio
from user_thread import User_Thread
from pydantic import BaseModel, Field
from datetime import datetime

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
)

relations = {
    "LTC": ("ADA", "DASH", "ATOM", "DOGE", "ALGO"),
    "DASH": ("ADA", "DOGE", "ATOM", "ALGO"),
    "ADA": ("DOGE", "ALGO"),
    "ATOM": ("ADA", "DOGE", "ALGO"),
}
######### Global def end ###########


class Point(BaseModel):
    """
    One intrument reads as point in BaseMarket
    """

    name: str
    instId: str | None = Field(default=None, repr=False)
    last_price: float = 0


class Market(BaseModel):
    base: str = Field(default="USDT", repr=False)
    ts: datetime = Field(default=datetime.now(), repr=True)
    pnt: dict[str, Point] = Field(default=dict(), repr=True)
    points: set[str] = Field(default=set(), repr=False)

    def __init__(self, pairs: tuple, **data) -> None:
        super().__init__(**data)
        # that was sexy I thought...
        # Ok, we take pairs, split them to coins, and filter out base coin
        points = {
            coin
            for pair in pairs
            for coin in pair.split(sep="-")
            if not coin == self.base
        }
        self.points = points
        # print (self.points)
        for key in self.points:
            self.pnt.update({key: Point(name=key)})
            # setattr(self, key, Point(name=key))
        # print(self)

    def __getitem__(self, key: str) -> float:
        """Get last price of instrumen on market"""
        return self.pnt[key].last_price

    def __setitem__(self, name: str, value: float) -> None:
        """Update last price of instrument over market"""
        self.ts = datetime.now()
        self.pnt[name].last_price = value


m = Market(pairs=params)
print(f"Before: \n{m}")
m["DOGE"] = 123129.00
m["LTC"] = 875
m["ADA"] = 8879
print(f"After: \n{m}")
