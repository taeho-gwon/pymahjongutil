import pytest

from pymahjong.enum.common import WindEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.player_wind import PlayerWind
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, player_wind, expected",
    [
        ("22789m456s123p111z", WindEnum.EAST, True),
        ("22789m456s123p222z", WindEnum.EAST, False),
        ("22789m456s123p333z", WindEnum.EAST, False),
        ("22789m456s123p444z", WindEnum.EAST, False),
        ("22789m456s123p444z", WindEnum.NORTH, True),
    ],
)
def test_player_wind(test_input, player_wind, expected):
    assert_yaku_check(
        test_input, expected, PlayerWind(), AgariInfo(player_wind=player_wind)
    )
