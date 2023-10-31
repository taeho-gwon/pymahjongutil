import pytest

from pymahjongutil.yaku_checker.white_dragon import WhiteDragon
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22789m456s123p555z", True),
        ("22789m456s123p,pon555z", True),
        ("22789m456s123p777z", False),
        ("22789m555666777z", True),
    ],
)
def test_white_dragon(test_input, expected):
    assert_yaku_check(test_input, expected, WhiteDragon())
