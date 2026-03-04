from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class BigThreeDragons(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.BIG_THREE_DRAGONS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        num_dragon_triplets = sum(
            1
            for part in division.parts
            if part.counts.is_containing_only(Tiles.DRAGONS)
            and part.is_triplet_or_quad
        )
        return num_dragon_triplets == 3
