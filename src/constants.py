from src.enum.common import TileType
from src.schema.tile import Tile

TILE_TYPE_CNT = {
    TileType.MAN: 9,
    TileType.PIN: 9,
    TileType.SOU: 9,
    TileType.WIND: 4,
    TileType.DRAGON: 3,
}


class Tiles:
    MANS = [
        Tile(type=TileType.MAN, value=value + 1)
        for value in range(TILE_TYPE_CNT[TileType.MAN])
    ]
    PINS = [
        Tile(type=TileType.PIN, value=value + 1)
        for value in range(TILE_TYPE_CNT[TileType.PIN])
    ]
    SOUS = [
        Tile(type=TileType.SOU, value=value + 1)
        for value in range(TILE_TYPE_CNT[TileType.SOU])
    ]
    WINDS = [
        Tile(type=TileType.WIND, value=value + 1)
        for value in range(TILE_TYPE_CNT[TileType.WIND])
    ]
    DRAGONS = [
        Tile(type=TileType.DRAGON, value=value + 1)
        for value in range(TILE_TYPE_CNT[TileType.DRAGON])
    ]
    ALL = MANS + PINS + SOUS + WINDS + DRAGONS
