from pymahjong.enum.common import YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class ThirteenOrphans(BaseYakuman):
    def __init__(self):
        super().__init__(YakumanEnum.THIRTEEN_ORPHANS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return len(division.parts) == 1