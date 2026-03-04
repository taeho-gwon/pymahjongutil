from dataclasses import dataclass

from pymahjongutil.enum.common import ActionTypeEnum
from pymahjongutil.schema.game_tile import GameTile


@dataclass
class RoundAction:
    type: ActionTypeEnum
    actor: int
    tiles: list[GameTile]
    target: int | None = None
