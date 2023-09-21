from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class RobbingAQuad(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ROBBING_A_QUAD)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        return agari_info.is_robbing_a_quad
