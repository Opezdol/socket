from pydantic import BaseModel, computed_field
from datetime import datetime
from .point import Point


class Deal(BaseModel):
    # id: int | None
    ts: datetime
    dir: tuple[str, str]
    sold: float
    bought: float

    @computed_field(repr=True)  # type: ignore[misc]
    @property
    def actual_price(self) -> float:
        return self.bought / self.sold

    class Config:
        extra = "allow"
        json_encoders = {float: lambda v: round(v, 2)}
