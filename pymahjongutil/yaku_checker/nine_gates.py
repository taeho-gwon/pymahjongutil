import numpy as np

from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku

_NINE_GATES_BASE = np.array([3, 1, 1, 1, 1, 1, 1, 1, 3])


class NineGates(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.NINE_GATES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        if division.is_opened:
            return False

        tile_count = division.tile_count
        return any(
            sum(abs(tile_count[i : i + 9] - _NINE_GATES_BASE)) == 1
            for i in (0, 9, 18)
        )
