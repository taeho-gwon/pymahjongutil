from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class Chinrotou(BaseYakuman):
    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return all(
            sum(part.counts[t] for t in Tiles.SIMPLES + Tiles.HONORS) == 0
            for part in division.parts
        )
