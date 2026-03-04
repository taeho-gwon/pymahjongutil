from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class ThreeQuads(BaseYaku):
    def __init__(self) -> None:
        super().__init__(YakuEnum.THREE_QUADS)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        return division.num_quads == 3
