from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class AllTriplets(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.ALL_TRIPLETS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        num_triplets = sum(
            1
            for part in division.parts
            if part.is_triplet_or_quad
        )
        return num_triplets == 4
