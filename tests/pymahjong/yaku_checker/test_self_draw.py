import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.self_draw import SelfDraw
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, is_tsumo_agari, expected",
    [
        ("123456789m11199p", True, True),
        ("123456789m11199p", False, False),
        ("123456m11199p,chi789m", True, False),
        ("123456m11199p,chi789m", False, False),
        ("123456789m99p,cok1111p", True, True),
        ("123456789m99p,cok1111p", False, False),
    ],
)
def test_self_draw(test_input, is_tsumo_agari, expected):
    agari_info = AgariInfo(is_tsumo_agari=is_tsumo_agari)
    assert_yaku_check(test_input, expected, SelfDraw(), agari_info)
