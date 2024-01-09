from fastapi import FastAPI
from web import deal

app = FastAPI()
app.include_router(deal.router)
