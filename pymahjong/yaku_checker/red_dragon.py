from pymahjong.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.base_yaku import BaseYaku


class RedDragon(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.RED_DRAGON)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return any(
            (
                part.type is DivisionPartTypeEnum.TRIPLE
                or part.type is DivisionPartTypeEnum.QUAD
            )
            and part.counts.is_containing_only([Tiles.DRAGONS[2]])
            for part in division.parts
        )