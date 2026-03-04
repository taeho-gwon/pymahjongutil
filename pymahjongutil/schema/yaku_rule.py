from dataclasses import dataclass, field

from pymahjongutil.enum.common import YakuEnum


@dataclass
class YakuRule:
    yaku: YakuEnum
    han_normal: int
    han_opened: int
    is_yakuman: bool = False
    high_yakus: list[YakuEnum] = field(default_factory=list)

    def get_han(self, is_opened: bool) -> int:
        return self.han_opened if is_opened else self.han_normal
