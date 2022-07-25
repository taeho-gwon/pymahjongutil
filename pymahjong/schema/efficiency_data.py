from __future__ import annotations

from pydantic import BaseModel

from pymahjong.schema.tile import Tile


class EfficiencyData(BaseModel):
    discard_tile: Tile
    ukeire: list[Tile]
    ukeire_count: int

    def __lt__(self, other: EfficiencyData) -> bool:
        if self.ukeire_count != other.ukeire_count:
            return self.ukeire_count > other.ukeire_count
        return self.discard_tile < other.discard_tile
