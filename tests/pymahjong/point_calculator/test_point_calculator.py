import pytest

from pymahjong.enum.common import (
    AgariTypeFuReasonEnum,
    BodyFuReasonEnum,
    HandShapeFuReasonEnum,
    YakuEnum,
)
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.point_calculator.point_calculator import PointCalculator
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.point_info import PointInfo


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
    "test_input, point_diff, han, fu, yakus, fu_reasons",
    [
        (
            "233445p88s345m,pon555s",
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
    ],
)
def test_calculate_point_info(test_input, point_diff, han, fu, yakus, fu_reasons):
    hand = get_hand_from_code(test_input)
    assert PointCalculator().calculate_point_info(
        hand, AgariInfo(is_tsumo_agari=True)
    ) == PointInfo(
        point_diff=point_diff,
        han=han,
        fu=fu,
        yakus=yakus,
        fu_reasons=fu_reasons,
    )
