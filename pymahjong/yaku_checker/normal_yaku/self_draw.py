from pymahjong.enum.common import NormalYakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.normal_yaku.base_normal_yaku import BaseNormalYaku


class SelfDraw(BaseNormalYaku):
    def __init__(self):
        super().__init__(NormalYakuEnum.SELF_DRAW)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        raise NotImplementedError
