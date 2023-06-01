from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class SmallFourWinds(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.SMALL_FOUR_WINDS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        raise NotImplementedError
