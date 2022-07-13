from __future__ import annotations

from pydantic import BaseModel

from src.enum.common import TileTypeEnum


class Tile(BaseModel):
    type: TileTypeEnum
    value: int

    class Config:
        frozen = True

    def __index__(self):
        start_idx = {
            TileTypeEnum.MAN: -1,
            TileTypeEnum.PIN: 8,
            TileTypeEnum.SOU: 17,
            TileTypeEnum.WIND: 26,
            TileTypeEnum.DRAGON: 30,
        }
        return start_idx[self.type] + self.value

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
