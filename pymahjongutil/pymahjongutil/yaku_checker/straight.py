from itertools import combinations

from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class Straight(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.STRAIGHT)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        for part1, part2, part3 in combinations(division.parts, 3):
            if not (
                part1.type is part2.type is part3.type is DivisionPartTypeEnum.SEQUENCE
            ):
                continue
            idx1 = part1.counts.find_earliest_nonzero_index()
            idx2 = part2.counts.find_earliest_nonzero_index()
            idx3 = part3.counts.find_earliest_nonzero_index()
            index = sorted([idx1, idx2, idx3])
            if index == [0, 3, 6] or index == [9, 12, 15] or index == [18, 21, 24]:
                return True
        return False
