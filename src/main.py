from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from datetime import datetime
import json
from random import randint
import time
from sqlmodel import SQLModel, Field, create_engine, Session, select
from pydantic import TypeAdapter

from typing import Annotated, Optional
from model.point import Point
from model.market import Market

#### Class Definition Zone #######
##################################


#  Table=true adds Deal definition to SQLModel.metadata
class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # date: datetime
    base: str
    dest: str
    base_amount: float
    dest_amount: float
    # market: Optional[str]
    # time: datetime

    @property
    def straight(self) -> float:
        return round(self.base_amount / self.dest_amount, 3)

    @property
    def reversed(self) -> float:
        return round(self.dest_amount / self.base_amount, 3)

    # TODO market: str  # Json repr  of Market at the moment of transaction


##################################

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CREATE database
####################
file_name = "deals.db"
db_url = f"sqlite:///{file_name}"
# create engine. We have only one engine for whole app. This thing differs from Session
engine = create_engine(db_url, echo=True)
SQLModel.metadata.create_all(engine)
with Session(engine) as session:
    session.add(Deal(base="LTC", base_amount=112.2, dest="USDT", dest_amount=1000.22))
    session.commit()
####################


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with Session(engine) as session:
        statement = select(Deal)
        res = session.exec(statement)
        return templates.TemplateResponse(
            name="deals.html",
            request=request,
            context={"choices": Point, "deals": res.all()},
        )


@app.post("/db")
async def add_deal(
    # I used Enum for Point, and choice of <select> is coded with Enum.value
    base: int = Form(...),
    base_amount: float = Form(...),
    dest: int = Form(...),
    dest_amount: float = Form(...),
):
    """
    Posts user input to database from <form> converting them to Deal model
    """
    obj = Deal(
        base=Point(base).name,
        dest=Point(dest).name,
        base_amount=base_amount,
        dest_amount=dest_amount,
        id=randint(0, 1000),
    )
    with Session(engine) as session:
        session.add(obj)
        session.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/db_auto")
async def auto_fill(data: list[Deal]):
    l = []
    for item in data:
        item.id = randint(0, 1000)
        l.append(item)
    with Session(engine) as session:
        for item in l:
            session.add(item)
        session.commit()


@app.delete("/db/{id}", response_class=RedirectResponse)
async def remove_item(request: Request, id: str):
    with Session(engine) as session:
        statement = select(Deal).where(Deal.id == id)
        res = session.exec(statement)
        deal = res.one()
        session.delete(deal)
        session.commit()
    return RedirectResponse("/", status_code=303)
