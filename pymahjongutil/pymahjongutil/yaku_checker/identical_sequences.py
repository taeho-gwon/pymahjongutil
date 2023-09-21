from itertools import combinations

from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class IdenticalSequences(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.IDENTICAL_SEQUENCES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return any(
            part1.type is part2.type is DivisionPartTypeEnum.SEQUENCE
            and part1.counts == part2.counts
            for part1, part2 in combinations(division.parts, 2)
        )
