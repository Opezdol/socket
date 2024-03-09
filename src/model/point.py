from typing import Literal

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
    "GPT",
    "CETUS",
    "ORDI",
    "ETC",
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
        "ORDI",
    ],
    "ATOM": ["ADA", "DOGE", "ALGO", "DOT", "XRP", "BCH", "FIL", "REN"],
    "ADA": ["DOGE", "ALGO"],
    "DOT": ["FIL", "MATIC", "REN"],
    "FIL": ["MATIC", "REN"],
    "MATIC": [
        "REN",
    ],
    "GPT": ["CETUS"],
    "XRP": [
        "CETUS",
        "GPT",
    ],
    "ETC": ["CETUS", "GPT"],
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
