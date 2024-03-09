from typing import Literal
from enum import Enum, auto

# https://youtube.com/shorts/8PqbChgNDcw?si=88jjV9yuwMnr9x5I
POINT = Literal[
    "USDT",
    "BTC",
    "LTC",
    "ADA",
    "ATOM",
    "ALGO",
    "DOGE",
    "XRP",
    "BCH",
    "DOT",
    "FIL",
    "MATIC",
    "REN",
]


class Point(Enum):
    USDT = auto()
    BTC = auto()
    LTC = auto()
    ADA = auto()
    ATOM = auto()
    ALGO = auto()
    DOGE = auto()
    XRP = auto()
    BCH = auto()
    DOT = auto()
    FIL = auto()
    MATIC = auto()
    REN = auto()


RELATION: dict[POINT, list[POINT]] = {
    ## dict[str:set]
    "LTC": [
        "ADA",
        "ATOM",
        "DOGE",
        "ALGO",
        "XRP",
        "BCH",
        "FIL",
        "REN",
        "MATIC",
        "DOT",
    ],
    "ATOM": ["ADA", "DOGE", "ALGO", "DOT", "XRP", "BCH", "FIL", "REN"],
    "ADA": ["DOGE", "ALGO"],
    "DOT": ["FIL", "MATIC", "REN"],
    "FIL": ["MATIC", "REN"],
    "MATIC": [
        "REN",
    ],
}
RELATION2: dict[POINT, list[POINT]] = {
    ## dict[str:set]
    "LTC": [
        "ADA",
        "ATOM",
        "DOGE",
        "ALGO",
        "XRP",
        "BCH",
        "FIL",
    ],
}
