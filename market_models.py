from enum import Enum
from typing import Literal, Optional, get_args
from pydantic import BaseModel, Field, computed_field
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


POINT = Literal[
    "USDT", "BTC", "LTC", "DASH", "ADA", "ATOM", "ALGO", "DOGE", "XRP", "BCH"
]


class Moneda(BaseModel):
    base: POINT
    rel: dict[POINT, float | None] = {}

    #
    # def ___init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     print("INit")
    #     print(f"Args of POINT: {get_args(POINT)}")
    #     for key in get_args(POINT):
    #         print(key)
    #         self.rel[key] = 6.9
    #
    def __post_init__(self):
        print("Postinit")

    def __getitem__(self, key: POINT) -> float | None:
        """Get last price of instrumen on market"""
        try:
            return self.rel[key]
        except KeyError:
            print(f"\tERROR: KeyError while getting item {key}")
            print(f"\tERROR: Creating key: {key}")
            self.rel[key] = 69
            return self.rel[key]

    def __setitem__(self, key: POINT, value: float) -> None:
        """Update last price of instrument over market"""
        try:
            self.rel.update({key: value})
        except KeyError:
            print(f"ERROR: KeyError while setting item {key}")
            return None


class Deal(BaseModel):
    # id: int | None
    ts: datetime
    dir: tuple[POINT, POINT]
    sold: float
    bought: float

    @computed_field(repr=True)  # type: ignore[misc]
    @property
    def price(self) -> float:
        return self.bought / self.sold

    class Config:
        extra = "allow"
        json_encoders = {float: lambda v: round(v, 2)}


class Market(BaseModel):
    base: str = Field(default="USDT", repr=False)


def main():
    m = Moneda(base="BTC")
    m["DASH"] = 133.0
    print(m)
    print(m["LTC"])
    # print(m["LiklTC"])
    print(m.rel)


if __name__ == "__main__":
    main()
