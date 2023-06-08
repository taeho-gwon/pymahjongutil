from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class SelfDraw(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.SELF_DRAW)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        return agari_info.is_tsumo_agari and not division.is_opened
