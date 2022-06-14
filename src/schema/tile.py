from pydantic import BaseModel

from src.enum.common import TileType


class Tile(BaseModel):
    type: TileType
    value: int

    def __hash__(self):
        return hash(self.type) + hash(self.value)

    def __index__(self):
        start_idx = {
            TileType.MAN: -1,
            TileType.PIN: 8,
            TileType.SOU: 17,
            TileType.WIND: 26,
            TileType.DRAGON: 30,
        }
        return start_idx[self.type] + self.value


class Tiles:
    MANS = [Tile(type=TileType.MAN, value=value + 1) for value in range(9)]
    PINS = [Tile(type=TileType.PIN, value=value + 1) for value in range(9)]
    SOUS = [Tile(type=TileType.SOU, value=value + 1) for value in range(9)]
    WINDS = [Tile(type=TileType.WIND, value=value + 1) for value in range(4)]
    DRAGONS = [Tile(type=TileType.DRAGON, value=value + 1) for value in range(3)]
    HONORS = WINDS + DRAGONS
    ALL = MANS + PINS + SOUS + HONORS

    TERMINALS = [MANS[0], MANS[8], PINS[0], PINS[8], SOUS[0], SOUS[8]]
    TERMINALS_AND_HONORS = TERMINALS + HONORS

    STRAIGHT_STARTS = MANS[0:7] + PINS[0:7] + SOUS[0:7]
    PARTIAL_STRAIGHT_STARTS = MANS[0:8] + PINS[0:8] + SOUS[0:8]
