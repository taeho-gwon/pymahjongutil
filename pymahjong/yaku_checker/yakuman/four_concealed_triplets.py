from pymahjong.enum.common import DivisionPartTypeEnum, YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class FourConcealedTriplets(BaseYakuman):
    def __init__(self):
        super().__init__(YakumanEnum.FOUR_CONCEALED_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        if len(division.parts) != 5:
            return False

        for part in division.parts:
            if part.type is DivisionPartTypeEnum.HEAD:
                continue
            if not part.is_concealed or part.type is DivisionPartTypeEnum.STRAIGHT:
                return False
        return True
