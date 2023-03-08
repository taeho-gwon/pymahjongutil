from pydantic import BaseModel

from pymahjong.enum.common import DivisionPartTypeEnum
from pymahjong.schema.count import TileCount
from pymahjong.schema.tile import Tile


class DivisionPart(BaseModel):
    type: DivisionPartTypeEnum
    counts: TileCount
    is_concealed: bool


class Division(BaseModel):
    parts: list[DivisionPart]
    agari_tile: Tile
