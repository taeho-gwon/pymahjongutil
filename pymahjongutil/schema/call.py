from pydantic import BaseModel

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.tile import Tile


class Call(BaseModel):
    type: CallTypeEnum
    tiles: list[Tile]
    call_idx: int
