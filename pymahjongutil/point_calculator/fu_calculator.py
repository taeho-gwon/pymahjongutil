from pymahjongutil.enum.common import (
    AgariTypeFuReasonEnum,
    BodyFuReasonEnum,
    DivisionPartTypeEnum,
    FuReasonEnum,
    HandShapeFuReasonEnum,
    HeadFuReasonEnum,
    WaitFuReasonEnum,
)
from pymahjongutil.rule.riichi_default_rule import RiichiDefaultRule
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division, DivisionPart
from pymahjongutil.schema.tile import Tile, Tiles


class FuCalculator:
    def __init__(self, rule: RiichiDefaultRule | None = None):
        self.fu_dict: dict[FuReasonEnum, int] = {
            HandShapeFuReasonEnum.SEVEN_PAIRS: 25,
            HandShapeFuReasonEnum.THIRTEEN_ORPHANS: 25,
            HandShapeFuReasonEnum.BASE: 20,
            WaitFuReasonEnum.HEAD_WAIT: 2,
            WaitFuReasonEnum.CLOSED_WAIT: 2,
            WaitFuReasonEnum.EDGE_WAIT: 2,
            AgariTypeFuReasonEnum.CONCEALED_RON: 10,
            AgariTypeFuReasonEnum.TSUMO: 2,
            AgariTypeFuReasonEnum.OPENED_PINFU: 10,
            HeadFuReasonEnum.DOUBLE_WIND_HEAD: 4,
            HeadFuReasonEnum.VALUE_HEAD: 2,
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
        fu_reasons: list[FuReasonEnum] = [
            self._calculate_hand_shape_fu(len(division.parts))
        ]
        if fu_reasons[0] is not HandShapeFuReasonEnum.BASE:
            return fu_reasons

        for part in division.parts:
            part_fu_reason = self._calculate_part_fu(part, agari_info)
            if part_fu_reason:
                fu_reasons.append(part_fu_reason)

        wait_fu_reason = self._calculate_wait_fu(division.parts[0], division.agari_tile)
        if wait_fu_reason:
            fu_reasons.append(wait_fu_reason)

        agari_type_fu_reason = self._calculate_agari_type_fu(
            agari_info.is_tsumo_agari, division.is_opened, len(fu_reasons) == 1
        )
        if agari_type_fu_reason:
            fu_reasons.append(agari_type_fu_reason)

        return fu_reasons

    def _calculate_hand_shape_fu(self, num_parts: int) -> HandShapeFuReasonEnum:
        if num_parts == 7:
            return HandShapeFuReasonEnum.SEVEN_PAIRS
        if num_parts == 1:
            return HandShapeFuReasonEnum.THIRTEEN_ORPHANS
        return HandShapeFuReasonEnum.BASE

    def _calculate_part_fu(
        self, part: DivisionPart, agari_info: AgariInfo
    ) -> HeadFuReasonEnum | BodyFuReasonEnum | None:
        first_tile_idx = part.counts.find_earliest_nonzero_index()
        if part.type is DivisionPartTypeEnum.HEAD:
            return self._calculate_head_fu(first_tile_idx, agari_info)

        if part.type is DivisionPartTypeEnum.SEQUENCE:
            return None

        fu_reason_idx = (
            (part.type is DivisionPartTypeEnum.QUAD) * 4
            + part.is_concealed * 2
            + (first_tile_idx in Tiles.TERMINALS_AND_HONORS)
        )

        return list(BodyFuReasonEnum)[fu_reason_idx]

    def _calculate_head_fu(
        self, tile_idx: int, agari_info: AgariInfo
    ) -> HeadFuReasonEnum | None:
        if (
            tile_idx == agari_info.player_wind_idx
            and tile_idx == agari_info.round_wind_idx
        ):
            return HeadFuReasonEnum.DOUBLE_WIND_HEAD
        if (
            tile_idx
            in [agari_info.player_wind_idx, agari_info.round_wind_idx] + Tiles.DRAGONS
        ):
            return HeadFuReasonEnum.VALUE_HEAD
        return None

    def _calculate_wait_fu(
        self, part: DivisionPart, agari_tile: Tile
    ) -> WaitFuReasonEnum | None:
        if part.type is DivisionPartTypeEnum.HEAD:
            return WaitFuReasonEnum.HEAD_WAIT

        if part.type is not DivisionPartTypeEnum.SEQUENCE:
            return None

        if (
            agari_tile.value in Tiles.SIMPLES
            and part.counts[agari_tile.value - 1] == 1
            and part.counts[agari_tile.value + 1] == 1
        ):
            return WaitFuReasonEnum.CLOSED_WAIT

        if (
            agari_tile.number == 3
            and part.counts[agari_tile.value - 1] == 1
            and part.counts[agari_tile.value - 2] == 1
        ):
            return WaitFuReasonEnum.EDGE_WAIT

        if (
            agari_tile.number == 7
            and part.counts[agari_tile.value + 1] == 1
            and part.counts[agari_tile.value + 2] == 1
        ):
            return WaitFuReasonEnum.EDGE_WAIT

        return None

    def _calculate_agari_type_fu(
        self, is_tsumo_agari: bool, is_opened: bool, is_pinfu_shape: bool
    ) -> AgariTypeFuReasonEnum | None:
        if is_tsumo_agari:
            return (
                AgariTypeFuReasonEnum.TSUMO if is_opened or not is_pinfu_shape else None
            )

        if not is_opened:
            return AgariTypeFuReasonEnum.CONCEALED_RON

        if is_pinfu_shape:
            return AgariTypeFuReasonEnum.OPENED_PINFU

        return None
