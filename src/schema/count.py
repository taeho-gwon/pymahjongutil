from __future__ import annotations

from itertools import islice
from typing import Iterable, Union

from pydantic import BaseModel

from src.schema.call import Call
from src.schema.hand import Hand
from src.schema.tile import Tile


class TileCount(BaseModel):
    counts: list[int]

    @property
    def total_count(self):
        return sum(self.counts)

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]):
        counts = [0] * 34
        for tile in tiles:
            counts[tile] += 1
        return TileCount(counts=counts)

    @staticmethod
    def create_from_calls(calls: Iterable[Call]):
        return sum(
            (TileCount.create_from_tiles(call.tiles) for call in calls),
            start=TileCount(counts=[0] * 34),
        )

    def __add__(self, other: TileCount):
        counts = [x + y for x, y in zip(self.counts, other.counts)]
        return TileCount(counts=counts)

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
    concealed_count: TileCount
    call_counts: list[TileCount]

    @staticmethod
    def create_from_hand(hand: Hand):
        concealed_count = TileCount.create_from_tiles(hand.iter_concealed_tiles)
        call_counts = [TileCount.create_from_tiles(call.tiles) for call in hand.calls]
        return HandCount(concealed_count=concealed_count, call_counts=call_counts)

    @property
    def total_count(self):
        return self.concealed_count.total_count + sum(
            call_count.total_count for call_count in self.call_counts
        )

    def __getitem__(self, item):
        return self.concealed_count[item] + sum(
            call_count[item] for call_count in self.call_counts
        )
