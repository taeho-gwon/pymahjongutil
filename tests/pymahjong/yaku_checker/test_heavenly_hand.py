import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.heavenly_hand import HeavenlyHand
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_tsumo_agari, player_wind, is_first_turn, expected",
    [
        (True, Tiles.WINDS[0], True, True),
        (True, Tiles.WINDS[1], True, False),
        (True, Tiles.WINDS[0], False, False),
        (False, Tiles.WINDS[0], True, False),
    ],
)
def test_heavenly_hand(is_tsumo_agari, player_wind, is_first_turn, expected):
    agari_info = AgariInfo(
        is_tsumo_agari=is_tsumo_agari,
        player_wind=player_wind,
        is_first_turn=is_first_turn,
    )
    assert_yaku_check("123456789m11199p", expected, HeavenlyHand(), agari_info)
