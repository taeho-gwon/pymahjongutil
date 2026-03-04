from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku
from pymahjongutil.yaku_checker.utils import has_triplet_or_quad_of


class PlayerWind(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.PLAYER_WIND)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        return has_triplet_or_quad_of(division, agari_info.player_wind_idx)
