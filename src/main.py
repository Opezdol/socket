from asyncio import get_event_loop
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio


from datetime import datetime
from random import randint
from sqlmodel import SQLModel, Field, create_engine, Session, select

from typing import Optional
from model.point import Point
from model.market import Market, RelativeModel
from service.market import listen_market, print_market


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


# FastApi app creation
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
####################


## INIT functions.
## Create db_tables && add background task
async def create_db_tables():
    SQLModel.metadata.create_all(engine)


m = Market()
r = RelativeModel()


@app.on_event("startup")
async def on_startup():
    await create_db_tables()
    ## add background task
    loop = asyncio.get_event_loop()
    loop.create_task(listen_market(m))
    loop.create_task(print_market(m, r))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(2)
        data = r.json()
        await websocket.send_json(data)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with Session(engine) as session:
        statement = select(Deal)
        res = session.exec(statement).all()
        return templates.TemplateResponse(
            name="index.html",
            request=request,
            context={"choices": Point, "deals": res},
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
        # id=randint(0, 1000),
    )
    with Session(engine) as session:
        session.add(obj)
        session.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/db_auto")
async def auto_fill(data: list[Deal]):
    lst = []
    for item in data:
        # item.id = randint(0, 1000)
        lst.append(item)
    with Session(engine) as session:
        for item in lst:
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
