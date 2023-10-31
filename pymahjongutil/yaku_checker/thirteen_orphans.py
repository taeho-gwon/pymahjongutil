from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class ThirteenOrphans(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.THIRTEEN_ORPHANS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return len(division.parts) == 1
