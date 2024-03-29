from dataclasses import dataclass, field

from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker import YAKU_DICT


@dataclass
class YakuRule:
    yaku: YakuEnum
    han_normal: int
    han_opened: int
    is_yakuman: bool = False
    high_yakus: list[YakuEnum] = field(default_factory=list)

    def get_han(self, is_opened: bool) -> int:
        return self.han_opened if is_opened else self.han_normal

    def is_applied(self, division: Division, agari_info: AgariInfo) -> bool:
        if not YAKU_DICT[self.yaku]().is_satisfied(division, agari_info):
            return False

        if self.get_han(division.is_opened) == 0:
            return False

        if any(
            YAKU_DICT[high_yaku]().is_satisfied(division, agari_info)
            for high_yaku in self.high_yakus
        ):
            return False

        return True

    class Config:
        arbitrary_types_allowed = True
