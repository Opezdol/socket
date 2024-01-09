from datetime import datetime

from model.deal import Deal
from model.point import POINT
import asyncio

# https://www.youtube.com/shorts/5hyAUyvLJP0?feature=share
# fake deals will be replced with database

_deals = [
    Deal(ts=datetime.now(), dir=("LTC", "DASH"), bought=112.64, sold=33.45),
    Deal(ts=datetime.now(), dir=("LTC", "DOT"), bought=1322.44, sold=11.2),
    Deal(ts=datetime.now(), dir=("LTC", "FIL"), bought=122.657, sold=1.223),
    Deal(ts=datetime.now(), dir=("LTC", "BTC"), bought=0.657, sold=122.223),
]


async def get_all() -> list[Deal]:
    await asyncio.sleep(1.24)
    return _deals


async def get_one(id: int) -> Deal | None:
    try:
        return _deals[id]
    except Exception:
        return None


async def create(d: Deal) -> Deal:
    """Create new Deal"""
    return d


async def modify(d: Deal) -> Deal:
    """Partially modify"""
    return d


async def replace(d: Deal) -> Deal:
    """Completely replace"""
    return d


async def delete(id: POINT) -> bool:
    """Remove if it existed, return True when doen"""
    await asyncio.sleep(4)
    return True
