from dataclasses import dataclass

from pymahjongutil.enum.common import TileTypeEnum
from pymahjongutil.schema.tile_index import TileIndex


@dataclass
class Tile:
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
    MANS = [TileIndex(i) for i in range(9)]
    PINS = [TileIndex(i) for i in range(9, 18)]
    SOUS = [TileIndex(i) for i in range(18, 27)]
    WINDS = [TileIndex(i) for i in range(27, 31)]
    DRAGONS = [TileIndex(i) for i in range(31, 34)]

    NUMBERS = MANS + PINS + SOUS
    HONORS = WINDS + DRAGONS
    DEFAULTS = NUMBERS + HONORS

    TERMINALS = [MANS[0], MANS[8], PINS[0], PINS[8], SOUS[0], SOUS[8]]
    TERMINALS_AND_HONORS = TERMINALS + HONORS

    STRAIGHT_STARTS = [t for t in DEFAULTS if t.is_sequence_start]
    PARTIAL_STRAIGHT_STARTS = [t for t in DEFAULTS if t.is_side_wait_start]

    SIMPLES = [t for t in NUMBERS if not t.is_terminal]
    GREENS = [SOUS[1], SOUS[2], SOUS[3], SOUS[5], SOUS[7], DRAGONS[1]]
