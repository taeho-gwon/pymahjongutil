from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.tile import Tile


@dataclass
class Hand:
    concealed_tiles: list[Tile]
    calls: list[Call]
    last_tile: Tile | None = None

    @property
    def is_opened(self) -> bool:
        return any(call.type != CallTypeEnum.CONCEALED_KAN for call in self.calls)

    @property
    def iter_concealed_tiles(self) -> Iterable[Tile]:
        yield from self.concealed_tiles
        if self.last_tile is not None:
            yield self.last_tile

    @property
    def iter_tiles(self) -> Iterable[Tile]:
        yield from self.concealed_tiles
        for call in self.calls:
            yield from call.tiles
        if self.last_tile is not None:
            yield self.last_tile
