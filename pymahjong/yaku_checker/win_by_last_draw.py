from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class WinByLastDraw(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.WIN_BY_LAST_DRAW)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        raise NotImplementedError
