from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine

from typing import Annotated, Optional
from model.point import POINT
from model.market import Market

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/db")
async def form(base: Annotated[str, Form]):
    print(base)
    return {"base": base}
    # return RedirectResponse("/index", status_code=303)


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
