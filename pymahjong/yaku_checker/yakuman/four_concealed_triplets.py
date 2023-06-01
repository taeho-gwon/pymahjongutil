from pymahjong.enum.common import YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class FourConcealedTriplets(BaseYakuman):
    def __init__(self):
        super().__init__(YakumanEnum.FOUR_CONCEALED_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return division.num_concealed_triplets == 4
