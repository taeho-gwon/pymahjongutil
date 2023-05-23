from pymahjong.enum.common import DivisionPartTypeEnum, FuReasonEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division, DivisionPart
from pymahjong.schema.tile import Tile, Tiles


class FuCalculator:
    def __init__(self):
        self.fu_dict: dict[FuReasonEnum, int] = {
            FuReasonEnum.SEVEN_PAIRS: 25,
            FuReasonEnum.THIRTEEN_ORPHANS: 25,
            FuReasonEnum.BASE: 20,
            FuReasonEnum.HEAD_WAIT: 2,
            FuReasonEnum.CLOSED_WAIT: 2,
            FuReasonEnum.EDGE_WAIT: 2,
            FuReasonEnum.CONCEALED_RON: 10,
            FuReasonEnum.TSUMO: 2,
            FuReasonEnum.OPENED_PINFU: 10,
            FuReasonEnum.DOUBLE_WIND_PAIR: 4,
            FuReasonEnum.VALUE_PAIR: 2,
            FuReasonEnum.OPENED_NORMAL_TRIPLE: 2,
            FuReasonEnum.OPENED_OUTSIDE_TRIPLE: 4,
            FuReasonEnum.CONCEALED_NORMAL_TRIPLE: 4,
            FuReasonEnum.CONCEALED_OUTSIDE_TRIPLE: 8,
            FuReasonEnum.OPENED_NORMAL_QUAD: 8,
            FuReasonEnum.OPENED_OUTSIDE_QUAD: 16,
            FuReasonEnum.CONCEALED_NORMAL_QUAD: 16,
            FuReasonEnum.CONCEALED_OUTSIDE_QUAD: 32,
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
            return [FuReasonEnum.SEVEN_PAIRS]

        if len(division.parts) == 1:
            return [FuReasonEnum.THIRTEEN_ORPHANS]

        fu_reasons = [FuReasonEnum.BASE]

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
                return FuReasonEnum.DOUBLE_WIND_PAIR
            if (
                first_tile
                in [agari_info.player_wind, agari_info.round_wind] + Tiles.DRAGONS
            ):
                return FuReasonEnum.VALUE_PAIR
            return None

        if part.type is DivisionPartTypeEnum.STRAIGHT:
            return None

        fu_reasons = [
            FuReasonEnum.OPENED_NORMAL_TRIPLE,
            FuReasonEnum.OPENED_OUTSIDE_TRIPLE,
            FuReasonEnum.CONCEALED_NORMAL_TRIPLE,
            FuReasonEnum.CONCEALED_OUTSIDE_TRIPLE,
            FuReasonEnum.OPENED_NORMAL_QUAD,
            FuReasonEnum.OPENED_OUTSIDE_QUAD,
            FuReasonEnum.CONCEALED_NORMAL_QUAD,
            FuReasonEnum.CONCEALED_OUTSIDE_QUAD,
        ]

        fu_reason_idx = (
            (part.type is DivisionPartTypeEnum.QUAD) * 4
            + part.is_concealed * 2
            + (first_tile in Tiles.TERMINALS_AND_HONORS)
        )

        return fu_reasons[fu_reason_idx]

    def _calculate_waiting_fu(
        self, part: DivisionPart, agari_tile: Tile
    ) -> FuReasonEnum | None:
        if part.type is DivisionPartTypeEnum.HEAD:
            return FuReasonEnum.HEAD_WAIT

        if part.type is not DivisionPartTypeEnum.STRAIGHT:
            return None

        if (
            agari_tile in Tiles.SIMPLES
            and part.counts[agari_tile - 1] == 1
            and part.counts[agari_tile + 1] == 1
        ):
            return FuReasonEnum.CLOSED_WAIT

        if (
            agari_tile.number == 3
            and part.counts[agari_tile - 1] == 1
            and part.counts[agari_tile - 2] == 1
        ):
            return FuReasonEnum.EDGE_WAIT

        if (
            agari_tile.number == 7
            and part.counts[agari_tile + 1] == 1
            and part.counts[agari_tile + 2] == 1
        ):
            return FuReasonEnum.EDGE_WAIT

        return None

    def _calculate_agari_type_fu(
        self, is_tsumo_agari: bool, is_opened: bool, is_pinfu_shape: bool
    ) -> FuReasonEnum | None:
        if is_tsumo_agari:
            return FuReasonEnum.TSUMO if is_opened or not is_pinfu_shape else None

        if not is_opened:
            return FuReasonEnum.CONCEALED_RON

        if is_pinfu_shape:
            return FuReasonEnum.OPENED_PINFU

        return None
