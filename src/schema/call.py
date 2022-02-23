from pydantic import BaseModel

from src.enum.common import CallType
from src.schema.tile import Tile


class Call(BaseModel):
    type: CallType
    tiles: list[Tile]
    call_idx: int
