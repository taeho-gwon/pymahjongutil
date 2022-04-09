import collections
from itertools import product
from typing import Any

from pydantic import BaseModel, root_validator

from src.enum.common import TileType

TILE_TYPE_CNT = {
    TileType.MAN: 9,
    TileType.PIN: 9,
    TileType.SOU: 9,
    TileType.WIND: 4,
    TileType.DRAGON: 3,
}


class Tile(BaseModel):
    type: TileType
    value: int

    def __hash__(self):
        return hash(self.type) + hash(self.value)

    @root_validator
    def validate_tile(cls, values: dict[str, Any]):
        t, v = values["type"], values["value"]
        if v < 1 or v > TILE_TYPE_CNT[t]:
            raise ValueError("Not Exist Tile")
        return values

    @staticmethod
    def all():
        for tile_type, cnt in TILE_TYPE_CNT.items():
            yield from (
                Tile(type=tile_type, value=value) for value in range(1, cnt + 1)
            )

    @staticmethod
    def terminals():
        yield from (
            Tile(type=tile_type, value=value)
            for tile_type, value in product(
                (TileType.MAN, TileType.PIN, TileType.SOU), (1, 9)
            )
        )

    @staticmethod
    def honors():
        yield from (Tile(type=TileType.WIND, value=value) for value in range(1, 5))
        yield from (Tile(type=TileType.DRAGON, value=value) for value in range(1, 4))

    @staticmethod
    def terminals_and_honors():
        yield from Tile.terminals()
        yield from Tile.honors()


class TileCount(collections.UserDict):
    def __setitem__(self, key: Tile, value: int):
        if value not in range(0, 5):
            raise ValueError
        self.data[key] = value
