from pydantic import BaseModel, Field
from datetime import datetime
from .point import POINT, RELATION
from .tick import Tick
from typing import get_args


class Market(BaseModel):
    base: POINT = "USDT"
    _keys: list[POINT] = list(get_args(POINT))
    _cache: dict[POINT, Tick] = {}

    def get_keys(self) -> list[str]:
        return [(key + "-" + self.base) for key in self._keys if not key == self.base]

    def __getitem__(self, key: POINT) -> Tick | None:
        """Get last price of instrumen on market"""
        try:
            return self._cache[key]
        except KeyError:
            print(f"ERROR: From __getitem__.Market. {key} - not found")
            return None

    def __setitem__(self, key: POINT, pnt: Tick):
        """Update last price of instrument over market"""
        self._cache[key] = pnt

    def __str__(self) -> str:
        return str(self._cache)


class RelativeModel(BaseModel):
    relations: dict[POINT, list] = Field(default=RELATION, repr=False)
    db: dict[POINT, dict[POINT, float]] = Field(default={}, repr=True)

    def __init__(self, **data):
        print("INIT")
        super().__init__(**data)
        self.init_db()

    def init_db(self):
        for pnt1 in self.relations.keys():
            self.db[pnt1] = {}
            for pnt2 in self.relations[pnt1]:
                self.db[pnt1][pnt2] = 69.0

    def fill(self, m: Market):
        """Calculate relative cost && fill Model with data"""
        for pnt1 in self.relations.keys():
            for pnt2 in self.relations[pnt1]:
                try:
                    self.db[pnt1][pnt2] = m[pnt1].sell / m[pnt2].buy
                except AttributeError as e:
                    print(f"ERROR:{e} on RelativeModel.fill with keys {pnt1} && {pnt2}")

    def __str__(self) -> str:
        res = ""
        for key in self.relations.keys():
            res += f"______{key}_____:\n"
            for itm in self.db[key]:
                res += f"{itm} \t-> {self.db[key][itm]}\n"
        return res
