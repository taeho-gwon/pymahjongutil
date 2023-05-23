from __future__ import annotations

from typing import Iterable

import numpy as np
from pydantic import BaseModel

from pymahjong.schema.call import Call
from pymahjong.schema.hand import Hand
from pymahjong.schema.tile import Tile, Tiles


class TileCount(BaseModel):
    counts: np.ndarray = np.zeros(len(Tiles.DEFAULTS))

    @property
    def num_tiles(self) -> int:
        return sum(self.counts)

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]):
        return TileCount(
            counts=np.bincount([tile for tile in tiles], minlength=len(Tiles.DEFAULTS))
        )

    @staticmethod
    def create_from_calls(calls: Iterable[Call]):
        return sum(TileCount.create_from_tiles(call.tiles) for call in calls)

    def __add__(self, other: TileCount):
        return TileCount(counts=self.counts + other.counts)

    def __getitem__(self, idx):
        return self.counts[idx]

    def __setitem__(self, idx, value):
        self.counts[idx] = value

    def find_earliest_nonzero_index(self, index: int = 0):
        while index < len(self.counts) and self.counts[index] == 0:
            index += 1
        return index

    class Config:
        arbitrary_types_allowed = True


class HandCount(BaseModel):
    concealed_count: TileCount
    call_counts: list[TileCount]

    @staticmethod
    def create_from_hand(hand: Hand):
        concealed_count = TileCount.create_from_tiles(hand.iter_concealed_tiles)
        call_counts = [TileCount.create_from_tiles(call.tiles) for call in hand.calls]
        return HandCount(concealed_count=concealed_count, call_counts=call_counts)

    @property
    def num_tiles(self):
        return self.concealed_count.num_tiles + sum(
            call_count.num_tiles for call_count in self.call_counts
        )

    @property
    def total_count(self) -> TileCount:
        return sum(self.call_counts, start=self.concealed_count)

    def __getitem__(self, item):
        return self.concealed_count[item] + sum(
            call_count[item] for call_count in self.call_counts
        )
