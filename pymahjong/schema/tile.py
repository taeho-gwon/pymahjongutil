from __future__ import annotations

from pydantic import BaseModel

from pymahjong.enum.common import TileTypeEnum


class Tile(BaseModel):
    type: TileTypeEnum
    value: int

    class Config:
        frozen = True

    def __lt__(self, other: Tile) -> bool:
        priority_dict = {
            TileTypeEnum.MAN: 0,
            TileTypeEnum.PIN: 1,
            TileTypeEnum.SOU: 2,
            TileTypeEnum.WIND: 3,
            TileTypeEnum.DRAGON: 4,
        }
        if self.type != other.type:
            return priority_dict[self.type] < priority_dict[other.type]
        return self.value < other.value

    @property
    def next(self) -> Tile:
        return Tile(type=self.type, value=self.value + 1)

    @property
    def prev(self) -> Tile:
        return Tile(type=self.type, value=self.value - 1)


class Tiles:
    MANS = [Tile(type=TileTypeEnum.MAN, value=value + 1) for value in range(9)]
    PINS = [Tile(type=TileTypeEnum.PIN, value=value + 1) for value in range(9)]
    SOUS = [Tile(type=TileTypeEnum.SOU, value=value + 1) for value in range(9)]
    WINDS = [Tile(type=TileTypeEnum.WIND, value=value + 1) for value in range(4)]
    DRAGONS = [Tile(type=TileTypeEnum.DRAGON, value=value + 1) for value in range(3)]
    HONORS = WINDS + DRAGONS
    ALL = MANS + PINS + SOUS + HONORS

    TERMINALS = [MANS[0], MANS[8], PINS[0], PINS[8], SOUS[0], SOUS[8]]
    TERMINALS_AND_HONORS = TERMINALS + HONORS

    STRAIGHT_STARTS = MANS[0:7] + PINS[0:7] + SOUS[0:7]
    PARTIAL_STRAIGHT_STARTS = MANS[0:8] + PINS[0:8] + SOUS[0:8]
