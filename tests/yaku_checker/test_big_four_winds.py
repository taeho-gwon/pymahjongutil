import pytest

from pymahjongutil.yaku_checker.big_four_winds import BigFourWinds
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m11222333444z", False),
        ("222m11z,pon222z,cok3333z,bmk4444z", False),
        ("22m111z,pon222z,cok3333z,bmk4444z", True),
        ("112233m11223344z", False),
    ],
)
def test_big_four_winds(test_input, expected):
    assert_yaku_check(test_input, expected, BigFourWinds())
