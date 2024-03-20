from SQLModel import SQLModel, Field
from typing import Optional
from datetime import datetime
from .point import Point


class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # date: datetime
    base: Point
    dest: str
    base_amount: float
    dest_amount: float
    ts: Optional[datetime] = Field(default=69000)

    class Config:
        extra = "allow"
        json_encoders = {float: lambda v: round(v, 4)}
