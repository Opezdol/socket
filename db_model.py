from datetime import datetime
from pydantic import BaseModel, Field
import json


class Point(BaseModel):
    """
    One intrument reads as point in BaseMarket
    """

    name: str = Field(repr=False)
    price: float = 1


class Market(BaseModel):
    base: str = Field(default="USDT", repr=False)
    ts: datetime = Field(default=datetime.now(), repr=True)
    pnt: dict[str, Point] = Field(default=dict(), repr=True)
    pairs: set[str]
    points: set[str] = Field(
        default=set(), repr=False
    )  ##### Maybe dont need it!!!!!!!!!!!!!!

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # that was sexy I thought...
        # Ok, we take pairs, split them to coins, and filter out base coin
        points = {
            coin
            for pair in self.pairs
            for coin in pair.split(sep="-")
            if not coin == self.base
        }
        self.points = points  ####### Maybe also dont need !!!!!!!!!!!!!!
        # print (self.points)
        for key in points:
            self.pnt.update({key: Point(name=key)})

    # def model_post_init(self, __context: Any):
    #     # Ok, we take pairs, split them to coins, and filter out base coin
    #     points = {
    #         coin
    #         for pair in self.pairs
    #         for coin in pair.split(sep="-")
    #         if not coin == self.base
    #     }
    #     self.points = points  ####### Maybe also dont need !!!!!!!!!!!!!!
    #     # print (self.points)
    #     for key in points:
    #         self.pnt.update({key: Point(name=key)})
    #
    #     # return super().model_post_init(__context)

    def __getitem__(self, key: str) -> float:
        """Get last price of instrumen on market"""
        return self.pnt[key].price

    def __setitem__(self, name: str, value: float) -> None:
        """Update last price of instrument over market"""
        self.ts = datetime.now()
        self.pnt[name].price = value


class RelativeModel(BaseModel):
    relations: dict[str, set] = Field(repr=False)
    db: dict[str, dict[str, float]] = Field(default={}, repr=True)
    _index: dict[int, str] = {}
    user_relation: dict[str, float] = {}

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.init_db()

    def init_db(self):
        ind = 1
        for pnt1 in self.relations.keys():
            self.db[pnt1] = {}
            for pnt2 in self.relations[pnt1]:
                key = pnt1 + "@" + pnt2
                self.db[pnt1][pnt2] = 1.0
                self._index[int(ind)] = key
                self.user_relation[key] = 1.0
                ind += 1.0
        self.load_user()

    def fill(self, m: Market):
        for pnt1 in self.relations.keys():
            for pnt2 in self.relations[pnt1]:
                self.db[pnt1][pnt2] = m[pnt1] / m[pnt2]

    def save_user(self):
        with open("./usr_data.json", mode="w") as f:
            f.write(self.model_dump_json(include={"user_relation"}))

    def load_user(self):
        try:
            with open("./usr_data.json", mode="r") as f:
                data = json.load(f)
                for key, value in data["user_relation"].items():
                    self.user_relation[key] = value
        except Exception as e:
            print(f"ERROR: {e}, during load_user function")

    def clear_user(self):
        for key, _ in self.user_relation.items():
            self.user_relation[key] = 0.0

    def fill_user(self, ind: int, value: float):
        key = self._index[ind]
        self.user_relation[key] = value
        self.save_user()

    def __str__(self) -> str:
        res = ""
        res += "*****************************************\n"
        res += f"************* {datetime.now().isoformat()[11:19]} ******************\n"
        res += "Ind |   Ins#1/Ins#2  | Relation   | Usr_rel | Usr_rel/Relation \n"
        res += "_______________________________________________________________\n"
        for ind, val in self._index.items():
            pnt1, pnt2 = val.split(sep="@")
            relation = self.db[pnt1][pnt2]
            user_relation = self.user_relation[val]
            res += f"{ind:>3} |\t{pnt1:>4} / {pnt2:<5} |{relation:10.3f}  |{user_relation:8} |\t{user_relation/relation:6.5f}\n"

        return res
