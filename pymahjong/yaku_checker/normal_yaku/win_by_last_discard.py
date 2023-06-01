from pymahjong.enum.common import NormalYakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.normal_yaku.base_normal_yaku import BaseNormalYaku


class WinByLastDiscard(BaseNormalYaku):
    def __init__(self):
        super().__init__(NormalYakuEnum.WIN_BY_LAST_DISCARD)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        raise NotImplementedError
