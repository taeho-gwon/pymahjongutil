import pytest

from pymahjongutil.enum.common import (
    AgariTypeFuReasonEnum,
    BodyFuReasonEnum,
    HandShapeFuReasonEnum,
    HeadFuReasonEnum,
    WaitFuReasonEnum,
    WindEnum,
)
from pymahjongutil.hand_checker.riichi_checker import RiichiChecker
from pymahjongutil.hand_parser import get_hand_from_code
from pymahjongutil.point_calculator.fu_calculator import FuCalculator
from pymahjongutil.schema.agari_info import AgariInfo


def get_first_division(hand_code: str, is_tsumo: bool = False):
    hand = get_hand_from_code(hand_code)
    checker = RiichiChecker(hand)
    divisions = checker.calculate_divisions(is_tsumo_agari=is_tsumo)
    assert len(divisions) > 0, f"No divisions found for {hand_code}"
    return divisions[0]


def get_all_divisions(hand_code: str, is_tsumo: bool = False):
    hand = get_hand_from_code(hand_code)
    checker = RiichiChecker(hand)
    divisions = checker.calculate_divisions(is_tsumo_agari=is_tsumo)
    assert len(divisions) > 0, f"No divisions found for {hand_code}"
    return divisions


class TestFuCalculatorSevenPairs:
    def test_seven_pairs_fu(self) -> None:
        division = get_first_division("1133557799m1133z")
        agari_info = AgariInfo(
            player_wind=WindEnum.WEST,
            loser_wind=WindEnum.NORTH,
        )
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert fu == 25
        assert fu_reasons == [HandShapeFuReasonEnum.SEVEN_PAIRS]


class TestFuCalculatorThirteenOrphans:
    def test_thirteen_orphans_fu(self) -> None:
        division = get_first_division("19m199s19p1234567z", is_tsumo=True)
        agari_info = AgariInfo(is_tsumo_agari=True)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert fu == 25
        assert fu_reasons == [HandShapeFuReasonEnum.THIRTEEN_ORPHANS]


class TestFuCalculatorNormalHand:
    def test_pinfu_tsumo(self) -> None:
        # Pinfu hand: all sequences, no value head, two-sided wait, tsumo
        # Find a division that gives exactly 20 fu (pinfu tsumo)
        agari_info = AgariInfo(is_tsumo_agari=True)
        calculator = FuCalculator()
        divisions = get_all_divisions("123456789m34555s", is_tsumo=True)
        found_pinfu = False
        for division in divisions:
            fu, fu_reasons = calculator.calculate_fu(division, agari_info)
            if fu == 20:
                assert fu_reasons == [HandShapeFuReasonEnum.BASE]
                found_pinfu = True
                break
        assert found_pinfu

    def test_concealed_ron(self) -> None:
        # Concealed hand ron: 10 fu for concealed ron
        division = get_first_division("222444m56667p11s6p")
        agari_info = AgariInfo(loser_wind=WindEnum.SOUTH)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert AgariTypeFuReasonEnum.CONCEALED_RON in fu_reasons
        assert HandShapeFuReasonEnum.BASE in fu_reasons

    def test_concealed_triple_fu(self) -> None:
        # Hand with concealed triples: 222m 444m
        division = get_first_division("222444m56667p11s6p")
        agari_info = AgariInfo(loser_wind=WindEnum.SOUTH)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert fu_reasons.count(BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE) == 3

    def test_opened_hand_with_tsumo(self) -> None:
        # Opened hand with tsumo: 2 fu for tsumo
        division = get_first_division("233445p88s345m,pon555s")
        agari_info = AgariInfo(is_tsumo_agari=True)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert AgariTypeFuReasonEnum.TSUMO in fu_reasons
        assert BodyFuReasonEnum.OPENED_NORMAL_TRIPLE in fu_reasons

    def test_value_head_fu(self) -> None:
        # Head is a value tile (dragon/wind)
        division = get_first_division("222m222p77z897s,bmk2222s")
        agari_info = AgariInfo(loser_wind=WindEnum.WEST)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert HeadFuReasonEnum.VALUE_HEAD in fu_reasons

    def test_double_wind_head_fu(self) -> None:
        # Head is both round wind and player wind (east-east)
        division = get_first_division("223344m223344s11z")
        agari_info = AgariInfo(
            round_wind=WindEnum.EAST,
            player_wind=WindEnum.EAST,
            loser_wind=WindEnum.WEST,
        )
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert HeadFuReasonEnum.DOUBLE_WIND_HEAD in fu_reasons

    def test_closed_wait_fu(self) -> None:
        # Closed wait (kanchan)
        division = get_first_division("222444m56667p11s6p")
        agari_info = AgariInfo(loser_wind=WindEnum.SOUTH)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert WaitFuReasonEnum.CLOSED_WAIT in fu_reasons

    def test_edge_wait_fu(self) -> None:
        # Edge wait: 12 waiting on 3, or 89 waiting on 7
        # Use the same hand as the existing point_calculator test
        agari_info = AgariInfo(player_wind=WindEnum.SOUTH)
        divisions = get_all_divisions("11122233m123s11p3m")
        calculator = FuCalculator()
        found_edge_wait = False
        for division in divisions:
            fu, fu_reasons = calculator.calculate_fu(division, agari_info)
            if WaitFuReasonEnum.EDGE_WAIT in fu_reasons:
                found_edge_wait = True
                break
        assert found_edge_wait

    def test_head_wait_fu(self) -> None:
        # Waiting on the head pair
        division = get_first_division("223344m223344s11z")
        agari_info = AgariInfo(loser_wind=WindEnum.WEST)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert WaitFuReasonEnum.HEAD_WAIT in fu_reasons

    def test_opened_pinfu_fu(self) -> None:
        # Opened hand, pinfu shape, ron -> opened pinfu 10 fu
        division = get_first_division("2233488m234s4m,chi234s")
        agari_info = AgariInfo(loser_wind=WindEnum.NORTH)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert AgariTypeFuReasonEnum.OPENED_PINFU in fu_reasons
        assert fu == 30

    def test_opened_outside_quad_fu(self) -> None:
        division = get_first_division("222m222p77z897s,bmk2222s")
        agari_info = AgariInfo(loser_wind=WindEnum.WEST)
        fu, fu_reasons = FuCalculator().calculate_fu(division, agari_info)
        assert BodyFuReasonEnum.OPENED_NORMAL_QUAD in fu_reasons
