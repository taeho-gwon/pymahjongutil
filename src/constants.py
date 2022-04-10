from src.enum.common import TileType
from src.schema.tile import Tile


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
