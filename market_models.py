from enum import Enum
from typing import Literal, get_args
from pydantic import BaseModel, Field
from datetime import datetime

#
# class Point(str, Enum):
#     btc = "BTC"
#     ltc = "LTC"
#     dash = "DASH"
#     ada = "ADA"
#     atom = "ATOM"
#     algo = "ALGO"
#     doge = "DOGE"
#     xrp = "XRP"
#     bch = "BCH"


POINT = Literal["BTC", "LTC", "DASH", "ADA", "ATOM", "ALGO", "DOGE", "XRP", "BCH"]


class Moneda(BaseModel):
    base: POINT
    rel: dict[POINT, float | None] = {}

    def ___init__(self, **kwargs):
        super().__init__(**kwargs)
        print("INit")
        for key in get_args(POINT):
            print(key)
            self.rel[key] = 6.9

    def __post_init__(self):
        print("Postinit")


"""
    def __getitem__(self, key: POINT) -> float | None:
        '''Get last price of instrumen on market'''
        try:
            return self.rel[key]
        except KeyError:
            print(f"ERROR: KeyError {key}")
            return None

    def __setitem__(self, key: POINT, value: float) -> None:
        '''Update last price of instrument over market'''
        try:
            self.rel.update({key: value})
        except KeyError:
            print(f"ERROR: KeyError {key}")
            return None
"""


class Deal(BaseModel):
    id: int | None
    ts: datetime
    dir: tuple[POINT, POINT]
    sold: float
    buy: float

    @property
    async def rel(self) -> float:
        return self.sold / self.buy


class Market(BaseModel):
    base: str = Field(default="USDT", repr=False)


def main():
    m = Moneda(base="BTC")
    m["DASH"] = 133.0
    print(m)
    print(m["LTC"])
    print(m["LiklTC"])
    print(m.rel)


if __name__ == "__main__":
    main()
