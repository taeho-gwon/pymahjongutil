import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.red_dragon import RedDragon
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22789m456s123p777z", True),
        ("22789m456s123p,pon777z", True),
        ("22789m456s123p666z", False),
        ("22789m555666777z", True),
    ],
)
def test_red_dragon(test_input, expected):
    assert_yaku_check(test_input, expected, RedDragon(), AgariInfo())
