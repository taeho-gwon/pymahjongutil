from pymahjong.enum.common import YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class AllTerminals(BaseYakuman):
    def __init__(self):
        super().__init__(YakumanEnum.ALL_TERMINALS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return all(
            sum(part.counts[t] for t in Tiles.SIMPLES + Tiles.HONORS) == 0
            for part in division.parts
        )