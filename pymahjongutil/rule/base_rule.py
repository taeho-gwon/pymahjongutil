from pydantic import BaseModel, Field

from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.yaku_rule import YakuRule


class BaseRule(BaseModel):
    yaku_rule_dict: dict[YakuEnum, YakuRule]
    use_open_tanyao: bool = Field(default=True)
