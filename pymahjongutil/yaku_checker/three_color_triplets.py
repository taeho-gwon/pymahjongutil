from itertools import combinations

from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku
from pymahjongutil.yaku_checker.utils import is_three_color_index


class ThreeColorTriplets(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.THREE_COLOR_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        for part1, part2, part3 in combinations(division.parts, 3):
            if not (
                part1.type is DivisionPartTypeEnum.TRIPLE
                or part1.type is DivisionPartTypeEnum.QUAD
            ):
                continue
            if not (
                part2.type is DivisionPartTypeEnum.TRIPLE
                or part2.type is DivisionPartTypeEnum.QUAD
            ):
                continue
            if not (
                part3.type is DivisionPartTypeEnum.TRIPLE
                or part3.type is DivisionPartTypeEnum.QUAD
            ):
                continue

            if is_three_color_index(
                part1.counts.find_earliest_nonzero_index(),
                part2.counts.find_earliest_nonzero_index(),
                part3.counts.find_earliest_nonzero_index(),
            ):
                return True
        return False
