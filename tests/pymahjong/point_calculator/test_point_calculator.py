import pytest

from pymahjong.point_calculator.point_calculator import PointCalculator


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
    assert PointCalculator.calculate_base_point(fu, han) == expected


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
    assert PointCalculator.calculate_base_point(fu, han, is_yakuman=True) == expected
