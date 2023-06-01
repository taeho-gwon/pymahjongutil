from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class RedDragon(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.RED_DRAGON)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        raise NotImplementedError
