from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class WinByLastDraw(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.WIN_BY_LAST_DRAW)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        return agari_info.is_last_draw
