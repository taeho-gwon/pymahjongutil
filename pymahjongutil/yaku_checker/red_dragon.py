from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku
from pymahjongutil.yaku_checker.utils import has_triplet_or_quad_of


class RedDragon(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.RED_DRAGON)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        return has_triplet_or_quad_of(division, Tiles.DRAGONS[2])
