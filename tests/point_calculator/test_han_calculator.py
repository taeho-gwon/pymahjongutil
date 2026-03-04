import pytest

from pymahjongutil.enum.common import WindEnum, YakuEnum
from pymahjongutil.hand_checker.riichi_checker import RiichiChecker
from pymahjongutil.hand_parser import get_hand_from_code
from pymahjongutil.point_calculator.han_calculator import HanCalculator
from pymahjongutil.schema.agari_info import AgariInfo


def get_best_han(hand_code: str, agari_info: AgariInfo):
    hand = get_hand_from_code(hand_code)
    checker = RiichiChecker(hand)
    divisions = checker.calculate_divisions(
        is_tsumo_agari=agari_info.is_tsumo_agari
    )
    assert len(divisions) > 0, f"No divisions found for {hand_code}"

    calculator = HanCalculator()
    best_han = 0
    best_yakus: list[YakuEnum] = []
    for division in divisions:
        han, yakus = calculator.calculate_han(division, agari_info)
        if han > best_han:
            best_han = han
            best_yakus = yakus
    return best_han, best_yakus


class TestHanCalculatorSimpleYaku:
    def test_all_simples(self) -> None:
        # Tanyao (all simples): no terminals or honors
        agari_info = AgariInfo(is_tsumo_agari=True)
        han, yakus = get_best_han("233445p88s345m,pon555s", agari_info)
        assert YakuEnum.ALL_SIMPLES in yakus

    def test_self_draw(self) -> None:
        # Tsumo with concealed hand
        agari_info = AgariInfo(is_tsumo_agari=True)
        han, yakus = get_best_han("222345p34588s456m", agari_info)
        assert YakuEnum.SELF_DRAW in yakus

    def test_ready(self) -> None:
        agari_info = AgariInfo(
            is_ready_hand=True,
            loser_wind=WindEnum.SOUTH,
        )
        han, yakus = get_best_han("123456789m23411p", agari_info)
        assert YakuEnum.READY in yakus

    def test_one_shot(self) -> None:
        agari_info = AgariInfo(
            is_ready_hand=True,
            is_one_shot=True,
            loser_wind=WindEnum.SOUTH,
        )
        han, yakus = get_best_han("123456789m23411p", agari_info)
        assert YakuEnum.ONE_SHOT in yakus
        assert YakuEnum.READY in yakus

    def test_seven_pairs(self) -> None:
        agari_info = AgariInfo(
            player_wind=WindEnum.WEST,
            loser_wind=WindEnum.NORTH,
            is_ready_hand=True,
            is_one_shot=True,
        )
        han, yakus = get_best_han("1133557799m1133z", agari_info)
        assert YakuEnum.SEVEN_PAIRS in yakus

    def test_all_triplets(self) -> None:
        agari_info = AgariInfo(loser_wind=WindEnum.SOUTH)
        han, yakus = get_best_han("222444m66677p11s7p", agari_info)
        assert YakuEnum.ALL_TRIPLETS in yakus

    def test_three_concealed_triplets(self) -> None:
        agari_info = AgariInfo(loser_wind=WindEnum.SOUTH)
        han, yakus = get_best_han("222444m56667p11s6p", agari_info)
        assert YakuEnum.THREE_CONCEALED_TRIPLETS in yakus

    def test_four_concealed_triplets_yakuman(self) -> None:
        agari_info = AgariInfo(
            player_wind=WindEnum.SOUTH, is_tsumo_agari=True
        )
        han, yakus = get_best_han("11122233m111s11p3m", agari_info)
        assert YakuEnum.FOUR_CONCEALED_TRIPLETS in yakus
        assert han == 13

    def test_thirteen_orphans_yakuman(self) -> None:
        agari_info = AgariInfo(
            is_tsumo_agari=True, player_wind=WindEnum.NORTH
        )
        han, yakus = get_best_han("19m199s19p1234567z", agari_info)
        assert YakuEnum.THIRTEEN_ORPHANS in yakus
        assert han == 13

    def test_half_flush(self) -> None:
        agari_info = AgariInfo(
            player_wind=WindEnum.WEST,
            loser_wind=WindEnum.NORTH,
            is_ready_hand=True,
        )
        han, yakus = get_best_han("1133557799m1133z", agari_info)
        assert YakuEnum.HALF_FLUSH in yakus

    def test_flush(self) -> None:
        agari_info = AgariInfo(loser_wind=WindEnum.SOUTH)
        han, yakus = get_best_han("11223344556699m", agari_info)
        assert YakuEnum.FLUSH in yakus

    def test_yakuman_overrides_normal(self) -> None:
        # When yakuman is present, normal yakus are not returned
        agari_info = AgariInfo(
            is_tsumo_agari=True, player_wind=WindEnum.NORTH
        )
        han, yakus = get_best_han("19m199s19p1234567z", agari_info)
        # Thirteen orphans is yakuman, so no normal yakus
        assert all(
            yaku not in yakus
            for yaku in [YakuEnum.READY, YakuEnum.SELF_DRAW, YakuEnum.ALL_SIMPLES]
        )
