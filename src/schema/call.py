from pydantic import BaseModel

from src.enum.common import CallTypeEnum
from src.schema.tile import Tile


class Call(BaseModel):
    type: CallTypeEnum
    tiles: list[Tile]
    call_idx: int
