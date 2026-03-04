from dataclasses import dataclass, field

from pymahjongutil.schema.round_record import RoundRecord


@dataclass
class GameRecord:
    initial_scores: list[int]
    rounds: list[RoundRecord] = field(default_factory=list)
