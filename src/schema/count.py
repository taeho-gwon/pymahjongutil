from typing import Union

from src.schema.tile import Tile


class TileCount:
    def __init__(self, tiles: list[Tile]):
        self._values = [0] * 34
        for tile in tiles:
            self._values[tile] += 1

    def __getitem__(self, key: Union[Tile, int]):
        return self._values[key]

    def __setitem__(self, key: Union[Tile, int], value: int):
        if value not in range(0, 5):
            raise ValueError
        self._values[key] = value

    def __iter__(self):
        yield from self._values

    def get_last_nonzero_idx(self, idx: int = 0):
        while idx < len(self._values):
            if self._values[idx] != 0:
                break
            idx += 1
        return idx
