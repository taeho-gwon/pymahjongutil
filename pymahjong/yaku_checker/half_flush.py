from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.base_yaku import BaseYaku


class HalfFlush(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.HALF_FLUSH)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        tile_count = division.tile_count
        return (
            tile_count.is_containing_only(Tiles.MANS + Tiles.HONORS)
            or tile_count.is_containing_only(Tiles.PINS + Tiles.HONORS)
            or tile_count.is_containing_only(Tiles.SOUS + Tiles.HONORS)
        )
