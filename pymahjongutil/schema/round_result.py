from dataclasses import dataclass, field

from pymahjongutil.enum.common import RoundResultTypeEnum, YakuEnum


@dataclass
class RoundResult:
    type: RoundResultTypeEnum
    winners: list[int] = field(default_factory=list)
    loser: int | None = None
    han: list[int] = field(default_factory=list)
    fu: list[int] = field(default_factory=list)
    yakus: list[list[YakuEnum]] = field(default_factory=list)
    point_diffs: list[int] = field(default_factory=list)
    is_tenpai: list[bool] = field(default_factory=list)
