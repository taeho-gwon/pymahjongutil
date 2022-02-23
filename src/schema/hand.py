from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from src.enum.common import CallType
from src.schema.call import Call
from src.schema.tile import Tile


class Hand(BaseModel):
    tiles: list[Tile]
    calls: list[Call]
    draw_tile: Optional[Tile]

    @property
    def is_opened(self):
        return any(call.type != CallType.CONCEALED_KAN for call in self.calls)
