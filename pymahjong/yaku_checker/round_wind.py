from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class RoundWind(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ROUND_WIND)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        raise NotImplementedError