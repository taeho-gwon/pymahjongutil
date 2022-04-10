import collections

from pydantic import BaseModel

from src.enum.common import TileType


class Tile(BaseModel):
    type: TileType
    value: int

    def __hash__(self):
        return hash(self.type) + hash(self.value)


class TileCount(collections.UserDict):
    def __setitem__(self, key: Tile, value: int):
        if value not in range(0, 5):
            raise ValueError
        self.data[key] = value
