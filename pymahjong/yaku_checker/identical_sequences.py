from itertools import combinations

from pymahjong.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class IdenticalSequences(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.IDENTICAL_SEQUENCES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return any(
            part1.type is part2.type is DivisionPartTypeEnum.SEQUENCE
            and part1.counts == part2.counts
            for part1, part2 in combinations(division.parts, 2)
        )
