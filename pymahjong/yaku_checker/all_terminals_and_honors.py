from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.base_yaku import BaseYaku


class AllTerminalsAndHonors(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ALL_TERMINALS_AND_HONORS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return division.tile_count.is_containing_only(Tiles.TERMINALS_AND_HONORS)