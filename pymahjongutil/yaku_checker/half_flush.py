from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class HalfFlush(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.HALF_FLUSH)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        tile_count = division.tile_count
        return (
            tile_count.is_containing_only(Tiles.MANS + Tiles.HONORS)
            or tile_count.is_containing_only(Tiles.PINS + Tiles.HONORS)
            or tile_count.is_containing_only(Tiles.SOUS + Tiles.HONORS)
        ) and not tile_count.is_containing_only(Tiles.NUMBERS)
