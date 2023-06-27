import pytest

from pymahjong.enum.common import (
    AgariTypeFuReasonEnum,
    BodyFuReasonEnum,
    HandShapeFuReasonEnum,
    HeadFuReasonEnum,
    WaitFuReasonEnum,
    YakuEnum,
)
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.point_calculator.point_calculator import PointCalculator
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.point_info import PointInfo
from pymahjong.schema.tile import Tiles


@pytest.mark.parametrize(
    "fu, han, expected",
    [
        (30, 4, 1920),
        (70, 1, 560),
        (110, 2, 1760),
        (25, 4, 1600),
        (25, 6, 3000),
        (40, 5, 2000),
        (70, 9, 4000),
        (80, 11, 6000),
    ],
)
def test_calculate_base_point(fu, han, expected):
    assert PointCalculator().calculate_base_point(fu, han) == expected


@pytest.mark.parametrize(
    "fu, han, expected",
    [
        (30, 13, 8000),
        (30, 26, 16000),
        (30, 39, 24000),
        (30, 52, 32000),
        (30, 65, 40000),
        (30, 78, 48000),
    ],
)
def test_calculate_base_point_yakuman(fu, han, expected):
    assert PointCalculator().calculate_base_point(fu, han, is_yakuman=True) == expected


@pytest.mark.parametrize(
    "test_input, agari_info, point_diff, han, fu, yakus, fu_reasons",
    [
        (
            "233445p88s345m,pon555s",
            AgariInfo(is_tsumo_agari=True),
            [1500, -500, -500, -500],
            1,
            30,
            [YakuEnum.ALL_SIMPLES],
            [
                HandShapeFuReasonEnum.BASE,
                BodyFuReasonEnum.OPENED_NORMAL_TRIPLE,
                AgariTypeFuReasonEnum.TSUMO,
            ],
        ),
        (
            "222444m56667p11s6p",
            AgariInfo(loser_wind=Tiles.WINDS[1]),
            [4800, -4800, 0, 0],
            2,
            50,
            [YakuEnum.THREE_CONCEALED_TRIPLETS],
            [
                HandShapeFuReasonEnum.BASE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                WaitFuReasonEnum.CLOSED_WAIT,
                AgariTypeFuReasonEnum.CONCEALED_RON,
            ],
        ),
        (
            "11122233m111s11p3m",
            AgariInfo(player_wind=Tiles.WINDS[1], is_tsumo_agari=True),
            [-16000, 32000, -8000, -8000],
            13,
            50,
            [YakuEnum.FOUR_CONCEALED_TRIPLETS],
            [
                HandShapeFuReasonEnum.BASE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                BodyFuReasonEnum.CONCEALED_OUTSIDE_TRIPLE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                BodyFuReasonEnum.CONCEALED_OUTSIDE_TRIPLE,
                AgariTypeFuReasonEnum.TSUMO,
            ],
        ),
        (
            "11122233m123s11p3m",
            AgariInfo(player_wind=Tiles.WINDS[1]),
            [-8000, 8000, 0, 0],
            4,
            40,
            [YakuEnum.IDENTICAL_SEQUENCES, YakuEnum.PURE_OUTSIDE_HAND],
            [
                HandShapeFuReasonEnum.BASE,
                WaitFuReasonEnum.EDGE_WAIT,
                AgariTypeFuReasonEnum.CONCEALED_RON,
            ],
        ),
        (
            "1133557799m1133z",
            AgariInfo(
                player_wind=Tiles.WINDS[2],
                loser_wind=Tiles.WINDS[3],
                is_ready_hand=True,
                is_one_shot=True,
            ),
            [0, 0, 12000, -12000],
            7,
            25,
            [
                YakuEnum.READY,
                YakuEnum.ONE_SHOT,
                YakuEnum.SEVEN_PAIRS,
                YakuEnum.HALF_FLUSH,
            ],
            [
                HandShapeFuReasonEnum.SEVEN_PAIRS,
            ],
        ),
        (
            "2233488m234s4m,chi234s",
            AgariInfo(loser_wind=Tiles.WINDS[3]),
            [1500, 0, 0, -1500],
            1,
            30,
            [
                YakuEnum.ALL_SIMPLES,
            ],
            [
                HandShapeFuReasonEnum.BASE,
                AgariTypeFuReasonEnum.OPENED_PINFU,
            ],
        ),
        (
            "19m199s19p1234567z",
            AgariInfo(is_tsumo_agari=True, player_wind=Tiles.WINDS[3]),
            [-16000, -8000, -8000, 32000],
            13,
            25,
            [
                YakuEnum.THIRTEEN_ORPHANS,
            ],
            [
                HandShapeFuReasonEnum.THIRTEEN_ORPHANS,
            ],
        ),
        (
            "223344m223344s11z",
            AgariInfo(loser_wind=Tiles.WINDS[2]),
            [7700, 0, -7700, 0],
            3,
            40,
            [
                YakuEnum.TWO_SETS_OF_IDENTICAL_SEQUENCES,
            ],
            [
                HandShapeFuReasonEnum.BASE,
                HeadFuReasonEnum.DOUBLE_WIND_HEAD,
                WaitFuReasonEnum.HEAD_WAIT,
                AgariTypeFuReasonEnum.CONCEALED_RON,
            ],
        ),
        (
            "222m222p77z897s,bmk2222s",
            AgariInfo(loser_wind=Tiles.WINDS[2]),
            [3900, 0, -3900, 0],
            2,
            40,
            [
                YakuEnum.THREE_COLOR_TRIPLETS,
            ],
            [
                HandShapeFuReasonEnum.BASE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
                HeadFuReasonEnum.VALUE_HEAD,
                BodyFuReasonEnum.OPENED_NORMAL_QUAD,
                WaitFuReasonEnum.EDGE_WAIT,
            ],
        ),
    ],
)
def test_calculate_point_info(
    test_input, agari_info, point_diff, han, fu, yakus, fu_reasons
):
    hand = get_hand_from_code(test_input)
    assert PointCalculator().calculate_point_info(hand, agari_info) == PointInfo(
        point_diff=point_diff,
        han=han,
        fu=fu,
        yakus=yakus,
        fu_reasons=fu_reasons,
    )
