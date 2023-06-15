from pydantic import BaseModel

from pymahjong.enum.common import YakuEnum
from pymahjong.yaku_checker.base_yaku import BaseYaku


class YakuRule(BaseModel):
    is_yakuman: bool = False
    han_normal: int
    han_opened: int
    sub_yakus: list[YakuEnum] = []
    checker: BaseYaku

    class Config:
        arbitrary_types_allowed = True
