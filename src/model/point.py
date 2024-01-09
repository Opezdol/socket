from typing import Literal

POINT = Literal[
    "USDT",
    "BTC",
    "LTC",
    "DASH",
    "ADA",
    "ATOM",
    "ALGO",
    "DOGE",
    "XRP",
    "BCH",
    "DOT",
    "FIL",
]
RELATION: dict[POINT, list[POINT]] = {
    ## dict[str:set]
    "LTC": [
        "ADA",
        "DASH",
        "ATOM",
        "DOGE",
        "ALGO",
        "XRP",
        "BCH",
        "FIL",
    ],
    "ATOM": ["ADA", "DOGE", "ALGO", "DOT", "XRP", "BCH", "FIL"],
    "DASH": ["ADA", "DOGE", "ATOM", "ALGO"],
    "ADA": ["DOGE", "ALGO"],
    "DOT": ["FIL"],
}
RELATION2: dict[POINT, list[POINT]] = {
    ## dict[str:set]
    "LTC": [
        "ADA",
        "DASH",
        "ATOM",
        "DOGE",
        "ALGO",
        "XRP",
        "BCH",
        "FIL",
    ],
}
