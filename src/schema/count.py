from __future__ import annotations

from typing import Iterable

from pydantic import BaseModel

from src.schema.call import Call
from src.schema.hand import Hand
from src.schema.tile import Tile, Tiles


class TileCount(BaseModel):
    counts: dict[Tile, int]
    block: list[Tile]

    @property
    def total_count(self):
        return sum(self.counts.values())

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile], block: list[Tile] | None = None):
        if block is None:
            block = Tiles.ALL
        counts = dict(zip(block, [0] * len(block)))
        for tile in tiles:
            counts[tile] += 1
        return TileCount(counts=counts, block=block)

    @staticmethod
    def create_from_calls(calls: Iterable[Call], block: list[Tile] | None = None):
        if block is None:
            block = Tiles.ALL
        return sum(
            (TileCount.create_from_tiles(call.tiles) for call in calls),
            start=TileCount(counts={tile: 0 for tile in block}, block=block),
        )

    def __add__(self, other: TileCount):
        if self.block == other.block:
            counts = {
                tile: self.counts[tile] + other.counts[tile] for tile in self.block
            }
            return TileCount(counts=counts, block=self.block)
        raise ValueError("add tile_count of different block")

    def __getitem__(self, key: Tile):
        return self.counts[key]

    def __setitem__(self, key: Tile, value: int):
        if value not in range(5):
            raise ValueError
        self.counts[key] = value


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
