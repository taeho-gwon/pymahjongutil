from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class TwoSetsOfIdenticalSequences(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.TWO_SETS_OF_IDENTICAL_SEQUENCES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        raise NotImplementedError
