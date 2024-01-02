from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EfficiencyData:
    discard_tile: int
    ukeire: list[int]
    num_ukeire: int

    def __lt__(self, other: EfficiencyData) -> bool:
        if self.num_ukeire != other.num_ukeire:
            return self.num_ukeire > other.num_ukeire
        return self.discard_tile < other.discard_tile
