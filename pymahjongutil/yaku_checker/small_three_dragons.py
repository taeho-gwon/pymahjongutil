from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class SmallThreeDragons(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.SMALL_THREE_DRAGONS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        is_dragon_head = any(
            part.type is DivisionPartTypeEnum.HEAD
            and part.counts.is_containing_only(Tiles.DRAGONS)
            for part in division.parts
        )
        num_dragon_triplets = sum(
            1
            for part in division.parts
            if part.counts.is_containing_only(Tiles.DRAGONS)
            and (
                part.type is DivisionPartTypeEnum.TRIPLE
                or part.type is DivisionPartTypeEnum.QUAD
            )
        )
        return is_dragon_head and num_dragon_triplets == 2
