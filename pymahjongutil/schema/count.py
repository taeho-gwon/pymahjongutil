from dataclasses import dataclass
from typing import Iterable, Sequence, overload

from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.tile import Tile, Tiles


class TileCount:
    def __init__(self, counts: list[int] | None = None):
        self.counts: list[int] = (
            [0] * len(Tiles.DEFAULTS) if counts is None else counts
        )

    @property
    def num_tiles(self) -> int:
        return sum(self.counts)

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]) -> "TileCount":
        counts = [0] * 34
        for tile in tiles:
            counts[tile.value] += 1
        return TileCount(counts=counts)

    @staticmethod
    def create_from_indices(tiles: Iterable[int]) -> "TileCount":
        counts = [0] * 34
        for idx in tiles:
            counts[idx] += 1
        return TileCount(counts=counts)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TileCount):
            return NotImplemented
        return self.counts == other.counts

    def __add__(self, other: "TileCount") -> "TileCount":
        return TileCount(
            counts=[a + b for a, b in zip(self.counts, other.counts, strict=True)]
        )

    @overload
    def __getitem__(self, idx: int) -> int: ...

    @overload
    def __getitem__(self, idx: slice) -> list[int]: ...

    def __getitem__(self, idx: int | slice) -> int | list[int]:
        return self.counts[idx]

    @overload
    def __setitem__(self, idx: int, value: int) -> None: ...

    @overload
    def __setitem__(self, idx: slice, value: list[int]) -> None: ...

    def __setitem__(self, idx: int | slice, value: int | list[int]) -> None:
        self.counts[idx] = value  # type: ignore[index,assignment]

    def find_earliest_nonzero_index(self, index: int = 0) -> int:
        while index < len(self.counts) and self.counts[index] == 0:
            index += 1
        return index

    def is_containing_only(self, indices: Sequence[int]) -> bool:
        return sum(self.counts[i] for i in indices) == sum(self.counts)


@dataclass
class HandCount:
    concealed_count: TileCount
    call_counts: list[TileCount]

    @staticmethod
    def create_from_hand(hand: Hand) -> "HandCount":
        concealed_count = TileCount.create_from_tiles(hand.iter_concealed_tiles)
        call_counts = [TileCount.create_from_tiles(call.tiles) for call in hand.calls]
        return HandCount(concealed_count=concealed_count, call_counts=call_counts)

    @property
    def total_count(self) -> TileCount:
        return sum(self.call_counts, start=self.concealed_count)

    def __getitem__(self, item: int) -> int:
        return self.concealed_count[item] + sum(
            call_count[item] for call_count in self.call_counts
        )
