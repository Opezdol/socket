from typing import Literal, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# import models
from market_models import Deal, Moneda, POINT

# generate models for typescrypt
from pydantic2ts import generate_typescript_defs

# generate_typescript_defs("./market_models.py", "./front/models/models.ts")

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
my_deals: list[Deal] = [
    Deal(bought=135, sold=1.3, dir=("LTC", "USDT"), ts=datetime.now()),
    Deal(bought=991, sold=0.003, dir=("BTC", "USDT"), ts=datetime.now()),
]
market: dict[POINT, Moneda]
html2 = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  </head>
  <body>
    <h1>Hello, world!</h1>
    <canvas id="grid" width="600px" height="600px"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <script src="/static/code.js"></script>
  </body>
</html>
"""
html = """

<!DOCTYPE html>
<html>
    <head>
        <title>OKX by pohhmann</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>OKX data</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>

        <ul id='messages'>
        </ul>
        <canvas id="grid" width="600px" height="600px"></canvas>

        <script src="graphplot.js" type="module"></script>
        <script type="module">
            import {drawGrid} from './graphplot.js';

            const canvas = document.getElementById("grid");
            const config = {
                xMin: -3,
                xMax: 5,
                yMin: -1,
                yMax: 2,
                ctx: canvas.getContext("2d")
            };

            drawGrid(config);
        </script>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get_root():
    return HTMLResponse(html2)


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
