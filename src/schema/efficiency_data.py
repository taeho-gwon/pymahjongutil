from __future__ import annotations

from pydantic import BaseModel

from src.schema.tile import Tile


class EfficiencyData(BaseModel):
    discard_tile: Tile
    ukeire: list[Tile]
