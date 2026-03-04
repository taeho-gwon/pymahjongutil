from itertools import combinations

from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku
from pymahjongutil.yaku_checker.utils import is_three_color_index


class ThreeColorTriplets(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.THREE_COLOR_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        for part1, part2, part3 in combinations(division.parts, 3):
            if not all(
                p.is_triplet_or_quad for p in (part1, part2, part3)
            ):
                continue

            if is_three_color_index(
                part1.counts.find_earliest_nonzero_index(),
                part2.counts.find_earliest_nonzero_index(),
                part3.counts.find_earliest_nonzero_index(),
            ):
                return True
        return False
