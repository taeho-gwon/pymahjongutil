from abc import abstractmethod

from pymahjong.enum.common import YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class BaseYakuman(BaseYaku):
    def __init__(self, yaku: YakumanEnum):
        super().__init__(yaku)
        self.yaku: YakumanEnum = yaku

    @abstractmethod
    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        pass
