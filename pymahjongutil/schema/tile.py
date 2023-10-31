from __future__ import annotations

from pydantic import BaseModel

from pymahjongutil.enum.common import TileTypeEnum, WindEnum


class Tile(BaseModel):
    value: int

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
        return self.value - 30 if self.value > 30 else self.value % 9 + 1


class Tiles:
    MANS = [value for value in range(9)]
    PINS = [value for value in range(9, 18)]
    SOUS = [value for value in range(18, 27)]
    WINDS = [value for value in range(27, 31)]
    DRAGONS = [value for value in range(31, 34)]
    ETCS = [value for value in range(34, 42)]

    NUMBERS = MANS + PINS + SOUS
    HONORS = WINDS + DRAGONS
    DEFAULTS = NUMBERS + HONORS
    ALLS = DEFAULTS + ETCS

    TERMINALS = [MANS[0], MANS[8], PINS[0], PINS[8], SOUS[0], SOUS[8]]
    TERMINALS_AND_HONORS = TERMINALS + HONORS

    STRAIGHT_STARTS = MANS[0:7] + PINS[0:7] + SOUS[0:7]
    PARTIAL_STRAIGHT_STARTS = MANS[0:8] + PINS[0:8] + SOUS[0:8]

    SIMPLES = MANS[1:8] + PINS[1:8] + SOUS[1:8]
    GREENS = [SOUS[1], SOUS[2], SOUS[3], SOUS[5], SOUS[7], DRAGONS[1]]

    @classmethod
    def get_tile_from_wind_enum(cls, wind: WindEnum):
        if wind is WindEnum.EAST:
            return cls.WINDS[0]
        elif wind is WindEnum.SOUTH:
            return cls.WINDS[1]
        elif wind is WindEnum.WEST:
            return cls.WINDS[2]
        else:
            return cls.WINDS[3]
