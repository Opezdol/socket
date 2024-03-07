from typing import Literal

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
