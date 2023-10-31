from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class WhiteDragon(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.WHITE_DRAGON)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return any(
            (
                part.type is DivisionPartTypeEnum.TRIPLE
                or part.type is DivisionPartTypeEnum.QUAD
            )
            and part.counts.is_containing_only([Tiles.DRAGONS[0]])
            for part in division.parts
        )
