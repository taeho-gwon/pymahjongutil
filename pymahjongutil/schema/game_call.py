from dataclasses import dataclass

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.game_tile import GameTile


@dataclass
class GameCall:
    type: CallTypeEnum
    tiles: list[GameTile]
    call_idx: int
