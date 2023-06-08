from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.base_yaku import BaseYaku


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
