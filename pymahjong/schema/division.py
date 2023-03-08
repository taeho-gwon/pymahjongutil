from pydantic import BaseModel

from pymahjong.enum.common import DivisionPartTypeEnum
from pymahjong.schema.count import TileCount
from pymahjong.schema.tile import Tile


class DivisionPart(BaseModel):
    type: DivisionPartTypeEnum
    counts: TileCount
    is_concealed: bool

    @staticmethod
    def create_head(head_tile: Tile, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.HEAD,
            counts=TileCount.create_from_tiles([head_tile] * 2),
            is_concealed=is_concealed,
        )


class Division(BaseModel):
    parts: list[DivisionPart]
    agari_tile: Tile
