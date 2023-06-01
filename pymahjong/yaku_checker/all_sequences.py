from pymahjong.enum.common import AgariTypeFuReasonEnum, HandShapeFuReasonEnum, YakuEnum
from pymahjong.point_calculator.fu_calculator import FuCalculator
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class AllSequences(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ALL_SEQUENCES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        if division.is_opened:
            return False

        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        if (
            len(fu_reasons) == 1
            and fu_reasons[0] is HandShapeFuReasonEnum.BASE
            and agari_info.is_tsumo_agari
        ):
            return True

        if (
            len(fu_reasons) == 2
            and fu_reasons[0] is HandShapeFuReasonEnum.BASE
            and fu_reasons[1] is AgariTypeFuReasonEnum.CONCEALED_RON
            and not agari_info.is_tsumo_agari
        ):
            return True

        return False
