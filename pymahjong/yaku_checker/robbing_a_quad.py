from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class RobbingAQuad(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ROBBING_A_QUAD)

    def is_satisfied(self, division: Division, agari_info: AgariInfo) -> bool:
        raise NotImplementedError
