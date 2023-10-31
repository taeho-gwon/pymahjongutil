from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class Flush(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.FLUSH)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        tile_count = division.tile_count
        return (
            tile_count.is_containing_only(Tiles.MANS)
            or tile_count.is_containing_only(Tiles.PINS)
            or tile_count.is_containing_only(Tiles.SOUS)
        )
