from pymahjong.enum.common import (
    BodyFuReasonEnum,
    DivisionPartTypeEnum,
    FuReasonEnum,
    OtherFuReasonEnum,
)
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division, DivisionPart
from pymahjong.schema.tile import Tile, Tiles


class FuCalculator:
    def __init__(self):
        self.fu_dict: dict[FuReasonEnum, int] = {
            OtherFuReasonEnum.SEVEN_PAIRS: 25,
            OtherFuReasonEnum.THIRTEEN_ORPHANS: 25,
            OtherFuReasonEnum.BASE: 20,
            OtherFuReasonEnum.HEAD_WAIT: 2,
            OtherFuReasonEnum.CLOSED_WAIT: 2,
            OtherFuReasonEnum.EDGE_WAIT: 2,
            OtherFuReasonEnum.CONCEALED_RON: 10,
            OtherFuReasonEnum.TSUMO: 2,
            OtherFuReasonEnum.OPENED_PINFU: 10,
            OtherFuReasonEnum.DOUBLE_WIND_PAIR: 4,
            OtherFuReasonEnum.VALUE_PAIR: 2,
            BodyFuReasonEnum.OPENED_NORMAL_TRIPLE: 2,
            BodyFuReasonEnum.OPENED_OUTSIDE_TRIPLE: 4,
            BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE: 4,
            BodyFuReasonEnum.CONCEALED_OUTSIDE_TRIPLE: 8,
            BodyFuReasonEnum.OPENED_NORMAL_QUAD: 8,
            BodyFuReasonEnum.OPENED_OUTSIDE_QUAD: 16,
            BodyFuReasonEnum.CONCEALED_NORMAL_QUAD: 16,
            BodyFuReasonEnum.CONCEALED_OUTSIDE_QUAD: 32,
        }

    def calculate_fu(
        self, division: Division, agari_info: AgariInfo
    ) -> tuple[int, list[FuReasonEnum]]:
        fu_reasons = self._calculate_fu_reasons(division, agari_info)
        fu = sum(self.fu_dict[fu_reason] for fu_reason in fu_reasons)
        return fu, fu_reasons

    def _calculate_fu_reasons(
        self, division: Division, agari_info: AgariInfo
    ) -> list[FuReasonEnum]:
        if len(division.parts) == 7:
            return [OtherFuReasonEnum.SEVEN_PAIRS]

        if len(division.parts) == 1:
            return [OtherFuReasonEnum.THIRTEEN_ORPHANS]

        fu_reasons: list[FuReasonEnum] = [OtherFuReasonEnum.BASE]

        for part in division.parts:
            new_fu_reason = self._calculate_part_fu(part, agari_info)
            if new_fu_reason:
                fu_reasons.append(new_fu_reason)

        new_fu_reason = self._calculate_waiting_fu(
            division.parts[0], division.agari_tile
        )
        if new_fu_reason:
            fu_reasons.append(new_fu_reason)

        new_fu_reason = self._calculate_agari_type_fu(
            agari_info.is_tsumo_agari, division.is_opened, len(fu_reasons) == 1
        )
        if new_fu_reason:
            fu_reasons.append(new_fu_reason)

        return fu_reasons

    def _calculate_part_fu(
        self, part: DivisionPart, agari_info: AgariInfo
    ) -> FuReasonEnum | None:
        first_tile = Tile(part.counts.find_earliest_nonzero_index())
        if part.type is DivisionPartTypeEnum.HEAD:
            if (
                first_tile == agari_info.player_wind
                and first_tile == agari_info.round_wind
            ):
                return OtherFuReasonEnum.DOUBLE_WIND_PAIR
            if (
                first_tile
                in [agari_info.player_wind, agari_info.round_wind] + Tiles.DRAGONS
            ):
                return OtherFuReasonEnum.VALUE_PAIR
            return None

        if part.type is DivisionPartTypeEnum.STRAIGHT:
            return None

        fu_reason_idx = (
            (part.type is DivisionPartTypeEnum.QUAD) * 4
            + part.is_concealed * 2
            + (first_tile in Tiles.TERMINALS_AND_HONORS)
        )

        return list(BodyFuReasonEnum)[fu_reason_idx]

    def _calculate_waiting_fu(
        self, part: DivisionPart, agari_tile: Tile
    ) -> FuReasonEnum | None:
        if part.type is DivisionPartTypeEnum.HEAD:
            return OtherFuReasonEnum.HEAD_WAIT

        if part.type is not DivisionPartTypeEnum.STRAIGHT:
            return None

        if (
            agari_tile in Tiles.SIMPLES
            and part.counts[agari_tile - 1] == 1
            and part.counts[agari_tile + 1] == 1
        ):
            return OtherFuReasonEnum.CLOSED_WAIT

        if (
            agari_tile.number == 3
            and part.counts[agari_tile - 1] == 1
            and part.counts[agari_tile - 2] == 1
        ):
            return OtherFuReasonEnum.EDGE_WAIT

        if (
            agari_tile.number == 7
            and part.counts[agari_tile + 1] == 1
            and part.counts[agari_tile + 2] == 1
        ):
            return OtherFuReasonEnum.EDGE_WAIT

        return None

    def _calculate_agari_type_fu(
        self, is_tsumo_agari: bool, is_opened: bool, is_pinfu_shape: bool
    ) -> FuReasonEnum | None:
        if is_tsumo_agari:
            return OtherFuReasonEnum.TSUMO if is_opened or not is_pinfu_shape else None

        if not is_opened:
            return OtherFuReasonEnum.CONCEALED_RON

        if is_pinfu_shape:
            return OtherFuReasonEnum.OPENED_PINFU

        return None
