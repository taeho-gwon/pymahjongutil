from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class FourConcealedTriplets(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.FOUR_CONCEALED_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return division.num_concealed_triplets == 4
