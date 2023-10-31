from itertools import combinations

from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class TwoSetsOfIdenticalSequences(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.TWO_SETS_OF_IDENTICAL_SEQUENCES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        num_identical_sequences = sum(
            1
            for part1, part2 in combinations(division.parts, 2)
            if part1.type is part2.type is DivisionPartTypeEnum.SEQUENCE
            and part1.counts == part2.counts
        )
        return num_identical_sequences == 2 or num_identical_sequences == 6
