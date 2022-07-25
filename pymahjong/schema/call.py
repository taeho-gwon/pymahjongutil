from pydantic import BaseModel

from pymahjong.enum.common import CallTypeEnum
from pymahjong.schema.tile import Tile


class Call(BaseModel):
    type: CallTypeEnum
    tiles: list[Tile]
    call_idx: int
