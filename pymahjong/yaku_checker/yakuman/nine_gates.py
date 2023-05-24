import numpy as np

from pymahjong.enum.common import YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.count import TileCount
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class NineGates(BaseYakuman):
    def __init__(self):
        super().__init__(YakumanEnum.NINE_GATES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        if division.is_opened:
            return False

        tile_count: TileCount = sum(
            (part.counts for part in division.parts), start=TileCount()
        )
        base_shape = np.array([3, 1, 1, 1, 1, 1, 1, 1, 3])
        return (
            sum(abs(tile_count[0:9] - base_shape)) == 1
            or sum(abs(tile_count[9:18] - base_shape)) == 1
            or sum(abs(tile_count[18:27] - base_shape)) == 1
        )
