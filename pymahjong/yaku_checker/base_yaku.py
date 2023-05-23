from abc import ABC, abstractmethod

from pymahjong.enum.common import YakuEnum, YakumanEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division


class BaseYaku(ABC):
    def __init__(self, yaku: YakuEnum):
        self.yaku = yaku

    @abstractmethod
    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        pass

    @property
    def is_yakuman(self):
        return self.yaku in YakumanEnum
