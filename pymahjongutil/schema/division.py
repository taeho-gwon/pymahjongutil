from pydantic import BaseModel

from pymahjongutil.enum.common import CallTypeEnum, DivisionPartTypeEnum
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.count import TileCount
from pymahjongutil.schema.tile import Tile, Tiles


class DivisionPart(BaseModel):
    type: DivisionPartTypeEnum
    counts: TileCount
    is_concealed: bool

    @staticmethod
    def create_head(tile: int, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.HEAD,
            counts=TileCount.create_from_indices([tile] * 2),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_triple(tile: int, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.TRIPLE,
            counts=TileCount.create_from_indices([tile] * 3),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_straight(tile: int, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.SEQUENCE,
            counts=TileCount.create_from_indices([tile, tile + 1, tile + 2]),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_thirteen_orphans(head_tile: int, is_concealed: bool):
        return DivisionPart(
            type=DivisionPartTypeEnum.THIRTEEN_ORPHANS,
            counts=TileCount.create_from_indices(
                Tiles.TERMINALS_AND_HONORS + [head_tile]
            ),
            is_concealed=is_concealed,
        )

    @staticmethod
    def create_from_call(call: Call):
        match call.type:
            case CallTypeEnum.CHII:
                part_type = DivisionPartTypeEnum.SEQUENCE
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

    @property
    def tile_count(self) -> TileCount:
        return sum((part.counts for part in self.parts), start=TileCount())

    @property
    def num_concealed_triplets(self) -> int:
        return sum(
            1
            for part in self.parts
            if part.is_concealed
            and (
                part.type is DivisionPartTypeEnum.TRIPLE
                or part.type is DivisionPartTypeEnum.QUAD
            )
        )

    @property
    def num_quads(self) -> int:
        return sum(1 for part in self.parts if part.type is DivisionPartTypeEnum.QUAD)
