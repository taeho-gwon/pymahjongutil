from __future__ import annotations

from collections import Counter
from typing import Iterable

from pydantic import BaseModel

from pymahjong.schema.call import Call
from pymahjong.schema.hand import Hand
from pymahjong.schema.tile import Tile, Tiles


class TileCount(BaseModel):
    counts: dict[Tile, int]

    @property
    def total_count(self):
        return sum(self.counts.values())

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]):
        counts = {tile: 0 for tile in Tiles.ALL}
        counts.update(Counter(tiles))
        return TileCount(counts=counts)

    @staticmethod
    def create_from_calls(calls: Iterable[Call]):
        return sum(
            (TileCount.create_from_tiles(call.tiles) for call in calls),
            start=TileCount(counts={tile: 0 for tile in Tiles.ALL}),
        )

    def __add__(self, other: TileCount):
        counts = {tile: self.counts[tile] + other.counts[tile] for tile in Tiles.ALL}
        return TileCount(counts=counts)

    def __getitem__(self, key: Tile):
        return self.counts.get(key, 0)

    def __setitem__(self, key: Tile, value: int):
        if value not in range(5):
            raise ValueError
        self.counts[key] = value

    def convert_to_list34(self):
        return [self.counts[tile] for tile in Tiles.ALL]


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
