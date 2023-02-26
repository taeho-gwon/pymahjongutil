from __future__ import annotations

from pydantic import BaseModel

from pymahjong.enum.common import TileTypeEnum


class Tile(BaseModel):
    value: int

    def __lt__(self, other: Tile) -> bool:
        return self.value < other.value

    @property
    def next(self) -> Tile:
        return Tile(value=self.value + 1)

    @property
    def prev(self) -> Tile:
        return Tile(value=self.value - 1)

    @property
    def type(self) -> TileTypeEnum:
        if 0 <= self.value < 9:
            return TileTypeEnum.MAN
        elif 9 <= self.value < 18:
            return TileTypeEnum.PIN
        elif 18 <= self.value < 27:
            return TileTypeEnum.SOU
        elif 27 <= self.value < 31:
            return TileTypeEnum.WIND
        elif 31 <= self.value < 34:
            return TileTypeEnum.DRAGON
        else:
            return TileTypeEnum.ETC

    @property
    def number(self) -> int:
        if 0 <= self.value < 31:
            return self.value % 9 + 1
        elif 31 <= self.value < 34:
            return self.value - 30
        else:
            return self.value - 34


class Tiles:
    MANS = [Tile(value=value) for value in range(9)]
    PINS = [Tile(value=value) for value in range(9, 18)]
    SOUS = [Tile(value=value) for value in range(18, 27)]
    WINDS = [Tile(value=value) for value in range(27, 31)]
    DRAGONS = [Tile(value=value) for value in range(31, 34)]
    HONORS = WINDS + DRAGONS
    DEFAULTS = MANS + PINS + SOUS + HONORS

    TERMINALS = [MANS[0], MANS[8], PINS[0], PINS[8], SOUS[0], SOUS[8]]
    TERMINALS_AND_HONORS = TERMINALS + HONORS

    STRAIGHT_STARTS = MANS[0:7] + PINS[0:7] + SOUS[0:7]
    PARTIAL_STRAIGHT_STARTS = MANS[0:8] + PINS[0:8] + SOUS[0:8]
