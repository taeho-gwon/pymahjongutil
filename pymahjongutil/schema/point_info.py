from pydantic import BaseModel

from pymahjongutil.enum.common import FuReasonEnum, YakuEnum


class PointInfo(BaseModel):
    point_diff: tuple[int, int, int, int]
    han: int
    fu: int
    yakus: list[YakuEnum]
    fu_reasons: list[FuReasonEnum]
