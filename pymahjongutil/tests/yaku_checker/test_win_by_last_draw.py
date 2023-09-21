import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.win_by_last_draw import WinByLastDraw
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_last_draw, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_win_by_last_draw(is_last_draw, expected):
    agari_info = AgariInfo(is_last_draw=is_last_draw)
    assert_yaku_check("123456789m11199p", expected, WinByLastDraw(), agari_info)
