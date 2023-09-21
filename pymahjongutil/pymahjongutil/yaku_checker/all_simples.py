from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class AllSimples(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ALL_SIMPLES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return division.tile_count.is_containing_only(Tiles.SIMPLES)
