from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class ThirteenOrphans(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.THIRTEEN_ORPHANS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return len(division.parts) == 1
