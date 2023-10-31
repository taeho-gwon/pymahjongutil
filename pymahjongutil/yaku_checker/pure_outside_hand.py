from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class PureOutsideHand(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.PURE_OUTSIDE_HAND)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return all(
            not part.counts.is_containing_only(Tiles.SIMPLES + Tiles.HONORS)
            for part in division.parts
        )
