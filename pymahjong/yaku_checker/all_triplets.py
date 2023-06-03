from pymahjong.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class AllTriplets(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ALL_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return (
            sum(
                1
                for part in division.parts
                if part.type is DivisionPartTypeEnum.TRIPLE
                or part.type is DivisionPartTypeEnum.QUAD
            )
            == 4
        )
