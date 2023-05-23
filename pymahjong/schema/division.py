from pydantic import BaseModel

from pymahjong.enum.common import CallTypeEnum, DivisionPartTypeEnum
from pymahjong.schema.call import Call
from pymahjong.schema.count import TileCount
from pymahjong.schema.tile import Tile, Tiles


class DivisionPart(BaseModel):
    type: DivisionPartTypeEnum
    counts: TileCount
    is_concealed: bool

    @staticmethod
    def create_head(tile: Tile, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.HEAD,
            counts=TileCount.create_from_tiles([tile] * 2),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_triple(tile: Tile, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.TRIPLE,
            counts=TileCount.create_from_tiles([tile] * 3),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_straight(tile: Tile, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.STRAIGHT,
            counts=TileCount.create_from_tiles([tile, Tile(tile + 1), Tile(tile + 2)]),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_thirteen_orphans(head_tile: Tile, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.THIRTEEN_ORPHANS,
            counts=TileCount.create_from_tiles(
                Tiles.TERMINALS_AND_HONORS + [head_tile]
            ),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_from_call(call: Call):
        match call.type:
            case CallTypeEnum.CHII:
                part_type = DivisionPartTypeEnum.STRAIGHT
            case CallTypeEnum.PON:
                part_type = DivisionPartTypeEnum.TRIPLE
            case _:
                part_type = DivisionPartTypeEnum.QUAD

        return DivisionPart(
            type=part_type,
            counts=TileCount.create_from_tiles(call.tiles),
            is_concealed=call.type is CallTypeEnum.CONCEALED_KAN,
        )


class Division(BaseModel):
    parts: list[DivisionPart]
    agari_tile: Tile
    is_opened: bool
