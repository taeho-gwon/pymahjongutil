from dataclasses import dataclass

from pymahjongutil.schema.game_call import GameCall
from pymahjongutil.schema.game_tile import GameTile


@dataclass
class PlayerState:
    hand: list[GameTile]
    discards: list[GameTile]
    calls: list[GameCall]
    is_riichi: bool = False
    score: int = 25000
