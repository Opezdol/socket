from pydantic import BaseModel, Field
import pandas as pd
from typing import Optional
from datetime import datetime
from .point import Point
from .tick import Tick


class Market(BaseModel):
    # let us consider Point["USDT"] of Market as a base point in n-dimentional space
    #
    base: Point = Point["USDT"]
    _cache: dict[Point, Tick] = {}
    # ts: datetime = None

    def get_keys(self) -> list[str]:
        return [
            (item + "-" + self.base.name)
            for item in Point.keys()
            if not self.base.name == item
        ]

    def __getitem__(self, key: str) -> Tick:
        """Get last price of instrumen on market"""
        try:
            return self._cache[Point[key]]
        except KeyError:
            print(f"ERROR: From __getitem__.Market. {key} - not found")
            return None  # type: ignore

    def __setitem__(self, key: str, pnt: Tick):
        """Update last price of instrument over market"""
        # Entry point from str-keys to Point(Flag) keys
        self._cache[Point[key]] = pnt
        # self.ts = pnt.ts

    def __str__(self) -> str:
        return f"Market data: \n{self._cache}"


class RelativeModel:
    # I wnt a diagonal matrix with columns named Point.keys
    # && rows named Point.keys
    # but i dont need string representation of Point class.
    # maybe values as keys, or just use Pandas.DataFrame
    df: pd.DataFrame = pd.DataFrame(index=Point.keys(), columns=Point.keys())
    # dfdx: Optional[pd.DataFrame]

    def fill(self, m: Market):
        """Calculate relative cost && fill DataFrame with data"""
        pnts = [pnt for pnt in Point.keys() if not pnt == m.base.name]
        data = {}
        for pnt1 in pnts:
            data[pnt1] = {}
            for pnt2 in pnts:
                try:
                    if pnt1 == pnt2:
                        data[pnt1][pnt2] = m[pnt1].sell
                        continue
                    res = m[pnt1].sell / m[pnt2].buy
                    data[pnt1][pnt2] = res
                except AttributeError:
                    print(f"ERROR: RelativeModel.fill:  {pnt1} {pnt2} keys")
        last = pd.DataFrame.from_dict(data, orient="index")
        # self.dfdx = (last - self.df) / self.df * 1000
        self.df = last

    def json(self):
        return self.df.to_json()

    def __str__(self) -> str:
        return str(self.df)
