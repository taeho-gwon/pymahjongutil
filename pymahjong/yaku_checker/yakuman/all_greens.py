from pymahjong.enum.common import YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class AllGreens(BaseYakuman):
    def __init__(self):
        super().__init__(YakumanEnum.ALL_GREENS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return division.tile_count.is_containing_only(Tiles.GREENS)
