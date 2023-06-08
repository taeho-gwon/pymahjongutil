import pytest

from pymahjong.yaku_checker.straight import Straight
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123456789m45688s", True),
        ("123789p22299m,chi456p", True),
        ("11112345678999m", True),
        ("11123455678999m", False),
        ("123345567789m11z", False),
    ],
)
def test_straight(test_input, expected):
    assert_yaku_check(test_input, expected, Straight())
