from dataclasses import dataclass, field

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.round_record import RoundRecord


@dataclass
class GameState:
    round_wind: WindEnum
    round_number: int
    honba: int
    riichi_sticks: int
    scores: list[int]
    round_records: list[RoundRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.scores) != 4:
            msg = f"scores must have exactly 4 elements, got {len(self.scores)}"
            raise ValueError(msg)
        if not 1 <= self.round_number <= 4:
            msg = f"round_number must be 1-4, got {self.round_number}"
            raise ValueError(msg)

    @property
    def dealer(self) -> int:
        return (self.round_number - 1) % 4
