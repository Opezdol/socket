from os import name
from enum import Enum
from typing import Literal, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI

from market_models import Deal, Moneda, POINT

app = FastAPI()
my_deals: list[Deal] = []
market: dict[POINT, Moneda]


@app.get("/")
async def get_root():
    return "Hello: World"


@app.get("/items/{key}")
async def get_coin(key: POINT) -> Moneda:
    res = Moneda(base=key, rel={"LTC": 155, "BTC": 123})
    return res


@app.get("/deals")
async def get_deals() -> list[Deal]:
    return my_deals


@app.post("/deals")
async def add_deal(deal: Deal) -> Deal:
    deal.id = len(my_deals) + 1
    deal.ts = datetime.now()
    my_deals.append(deal)
    return deal
