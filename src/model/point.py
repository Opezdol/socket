from enum import Flag, auto

# https://youtube.com/shorts/8PqbChgNDcw?si=88jjV9yuwMnr9x5I


class Point(Flag):
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
    TON = auto()

    @classmethod
    def keys(cls) -> list[str]:
        return [item.name for item in Point]  # type: ignore

    @classmethod
    def len(cls) -> int:
        return Point.keys().__len__()


if __name__ == "__main__":
    print(Point.keys())
    print(Point.len())
