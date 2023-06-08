import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.green_dragon import GreenDragon
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22789m456s123p666z", True),
        ("22789m456s123p,pon666z", True),
        ("22789m456s123p555z", False),
        ("22789m555666777z", True),
    ],
)
def test_green_dragon(test_input, expected):
    assert_yaku_check(test_input, expected, GreenDragon(), AgariInfo())
