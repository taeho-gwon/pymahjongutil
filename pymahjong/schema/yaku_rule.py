from pydantic import BaseModel

from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker import YAKU_DICT
from pymahjong.yaku_checker.base_yaku import BaseYaku


class YakuRule(BaseModel):
    is_yakuman: bool = False
    han_normal: int
    han_opened: int
    high_yakus: list[YakuEnum] = []
    checker: BaseYaku

    def get_han(self, is_opened: bool) -> int:
        return self.han_opened if is_opened else self.han_normal

    def is_applied(self, division: Division, agari_info: AgariInfo) -> bool:
        if not self.checker.is_satisfied(division, agari_info):
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
