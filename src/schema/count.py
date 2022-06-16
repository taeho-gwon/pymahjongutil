from __future__ import annotations

from itertools import islice
from typing import Iterable, Union

from pydantic import BaseModel

from src.schema.call import Call
from src.schema.hand import Hand
from src.schema.tile import Tile


class TileCount:
    def __init__(self, tiles: list[Tile]):
        self._values = [0] * 34
        for tile in tiles:
            self._values[tile] += 1

    def __getitem__(self, key: Union[Tile, int]):
        return self._values[key]

    def __setitem__(self, key: Union[Tile, int], value: int):
        if value not in range(5):
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


class TmpTileCount(BaseModel):
    counts: list[int]

    @property
    def total_count(self):
        return sum(self.counts)

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]):
        counts = [0] * 34
        for tile in tiles:
            counts[tile] += 1
        return TmpTileCount(counts=counts)

    @staticmethod
    def create_from_calls(calls: Iterable[Call]):
        return sum(
            (TmpTileCount.create_from_tiles(call.tiles) for call in calls),
            start=TmpTileCount(counts=[0] * 34),
        )

    def __add__(self, other: TmpTileCount):
        counts = [x + y for x, y in zip(self.counts, other.counts)]
        return TmpTileCount(counts=counts)

    def __getitem__(self, key: Union[Tile, int]):
        return self.counts[key]

    def __setitem__(self, key: Union[Tile, int], value: int):
        if value not in range(5):
            raise ValueError
        self.counts[key] = value

    def get_first_nonzero_idx(self, idx: int):
        candidate = (
            x
            for x, val in enumerate(islice(self.counts, idx, None), start=idx)
            if val != 0
        )
        return next(candidate, len(self.counts))


class HandCount(BaseModel):
    concealed_count: TmpTileCount
    call_count: TmpTileCount

    @staticmethod
    def create_from_hand(hand: Hand):
        concealed_count = TmpTileCount.create_from_tiles(hand.iter_concealed_tiles)
        call_count = TmpTileCount.create_from_calls(hand.calls)
        return HandCount(concealed_count=concealed_count, call_count=call_count)

    @property
    def total_count(self):
        return self.concealed_count.total_count + self.call_count.total_count
