import pytest

from pymahjong.yaku_checker.small_four_winds import SmallFourWinds
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m11222333444z", True),
        ("222m11z,pon222z,cok3333z,bmk4444z", True),
        ("22m111z,pon222z,cok3333z,bmk4444z", False),
        ("112233m11223344z", False),
    ],
)
def test_small_four_winds(test_input, expected):
    assert_yaku_check(test_input, expected, SmallFourWinds())
