import asyncio
from src.service.market import run_cli

######## My globbal constants #######
url = "wss://ws.okx.com:8443/ws/v5/public"
instrm_url = "https://www.okx.com/api/v5/public/instruments"
params = (
    "DASH-USDT",
    "LTC-USDT",
    "ADA-USDT",
    "ATOM-USDT",
    "DOGE-USDT",
    "ALGO-USDT",
    "BCH-USDT",
    "XRP-USDT",
    "DOT-USDT",
)
## TODO
## ADD%
## LTC/XPR ATOM/DOT ATOM/XRP LTC/BCH ATOM/BCH

relations = {
    ## dict[str:set]
    "LTC": {"ADA", "DASH", "ATOM", "DOGE", "ALGO", "XRP", "BCH"},
    "ATOM": {"ADA", "DOGE", "ALGO", "DOT", "XRP", "BCH"},
    "DASH": {"ADA", "DOGE", "ATOM", "ALGO"},
    "ADA": {"DOGE", "ALGO"},
}
######### Global def end ###########


asyncio.run(run_cli())
