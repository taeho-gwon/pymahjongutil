from dataclasses import dataclass, field

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.player_state import PlayerState
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.wall import Wall


@dataclass
class RoundState:
    round_wind: WindEnum
    round_number: int
    honba: int
    riichi_sticks: int
    dealer: int
    current_player: int
    wall: Wall
    draw_index: int
    players: list[PlayerState]
    dora_count: int = 1
    action_history: list[RoundAction] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.players) != 4:
            msg = f"players must have exactly 4 elements, got {len(self.players)}"
            raise ValueError(msg)
        if not (0 <= self.draw_index <= 122):
            msg = f"draw_index must be between 0 and 122, got {self.draw_index}"
            raise ValueError(msg)
