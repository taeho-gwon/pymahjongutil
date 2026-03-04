from dataclasses import dataclass, field

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.round_result import RoundResult
from pymahjongutil.schema.wall import Wall


@dataclass
class RoundRecord:
    round_wind: WindEnum
    round_number: int
    honba: int
    riichi_sticks: int
    scores: list[int]
    dealer: int
    wall: Wall
    initial_hands: list[list[GameTile]]
    actions: list[RoundAction] = field(default_factory=list)
    result: RoundResult | None = None
