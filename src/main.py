from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine

from typing import Annotated, Optional
from model.point import Point
from model.market import Market

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = []
for item in Point:
    print(f" Name { item.name}, \t\tvalue {item.value}")


#  Table=true adds Deal definition to SQLModel.metadata
class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # date: datetime
    base: str
    dest: str
    base_amount: float
    dest_amount: float
    # market: str  # Json repr  of Market at the moment of transaction


# file_name = "deals.db"
# db_url = f"sqlite:///{file_name}"
# create engine. We have only one engine for whole app. This thing differs from Session
# engine = create_engine(db_url, echo=True)
# SQLModel.metadata.create_all(engine)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        name="form.html", request=request, context={"choices": Point}
    )


@app.post("/db")
async def form(
    base: str = Form(...),
    base_amount: float = Form(...),
    dest: str = Form(...),
    dest_amount: float = Form(...),
):
    obj = Deal(
        base=base,
        dest=dest,
        base_amount=base_amount,
        dest_amount=dest_amount,
    )
    db.append(obj)
    print()
    return RedirectResponse("/", status_code=303)


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


### Fake streamers
async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/data")
async def main():
    return StreamingResponse(fake_video_streamer())
