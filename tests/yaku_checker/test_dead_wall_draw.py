import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.dead_wall_draw import DeadWallDraw
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_dead_wall_draw, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_dead_wall_draw(is_dead_wall_draw, expected):
    agari_info = AgariInfo(is_dead_wall_draw=is_dead_wall_draw)
    assert_yaku_check("123456789m99p,cok1111p", expected, DeadWallDraw(), agari_info)
