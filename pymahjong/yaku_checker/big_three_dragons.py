from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku
from pymahjong.yaku_checker.green_dragon import GreenDragon
from pymahjong.yaku_checker.red_dragon import RedDragon
from pymahjong.yaku_checker.white_dragon import WhiteDragon


class BigThreeDragons(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.BIG_THREE_DRAGONS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return (
            WhiteDragon().is_satisfied(division, agari_info)
            and GreenDragon().is_satisfied(division, agari_info)
            and RedDragon().is_satisfied(division, agari_info)
        )
