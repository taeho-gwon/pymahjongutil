import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.player_wind import PlayerWind
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, player_wind, expected",
    [
        ("22789m456s123p111z", Tiles.WINDS[0], True),
        ("22789m456s123p222z", Tiles.WINDS[0], False),
        ("22789m456s123p333z", Tiles.WINDS[0], False),
        ("22789m456s123p444z", Tiles.WINDS[0], False),
        ("22789m456s123p444z", Tiles.WINDS[3], True),
    ],
)
def test_player_wind(test_input, player_wind, expected):
    assert_yaku_check(
        test_input, expected, PlayerWind(), AgariInfo(player_wind=player_wind)
    )
