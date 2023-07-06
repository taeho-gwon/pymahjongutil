import pytest

from pymahjong.enum.common import WindEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.earthly_hand import EarthlyHand
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_tsumo_agari, player_wind, is_first_turn, expected",
    [
        (True, WindEnum.NORTH, True, True),
        (True, WindEnum.EAST, True, False),
        (True, WindEnum.NORTH, False, False),
        (False, WindEnum.NORTH, True, False),
    ],
)
def test_earthly_hand(is_tsumo_agari, player_wind, is_first_turn, expected):
    agari_info = AgariInfo(
        is_tsumo_agari=is_tsumo_agari,
        player_wind=player_wind,
        is_first_turn=is_first_turn,
    )
    assert_yaku_check("123456789m11199p", expected, EarthlyHand(), agari_info)
