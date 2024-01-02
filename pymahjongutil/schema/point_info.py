from dataclasses import dataclass

from pymahjongutil.enum.common import FuReasonEnum, YakuEnum


@dataclass
class PointInfo:
    point_diff: tuple[int, int, int, int]
    han: int
    fu: int
    yakus: list[YakuEnum]
    fu_reasons: list[FuReasonEnum]
