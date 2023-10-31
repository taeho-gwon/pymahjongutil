from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class AllTriplets(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ALL_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        num_triplets = sum(
            1
            for part in division.parts
            if part.type is DivisionPartTypeEnum.TRIPLE
            or part.type is DivisionPartTypeEnum.QUAD
        )
        return num_triplets == 4
