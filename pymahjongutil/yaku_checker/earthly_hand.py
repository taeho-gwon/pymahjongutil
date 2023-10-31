from pymahjongutil.enum.common import WindEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class EarthlyHand(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.EARTHLY_HAND)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return (
            agari_info.is_first_turn
            and agari_info.player_wind != WindEnum.EAST
            and agari_info.is_tsumo_agari
        )
