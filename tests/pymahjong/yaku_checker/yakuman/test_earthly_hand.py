import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.yakuman.earthly_hand import EarthlyHand
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "expected, is_tsumo_agari, player_wind, is_first_turn",
    [
        (True, True, Tiles.WINDS[1], True),
        (False, True, Tiles.WINDS[0], True),
        (False, True, Tiles.WINDS[1], False),
        (False, False, Tiles.WINDS[1], True),
    ],
)
def test_earthly_hand(expected, is_tsumo_agari, player_wind, is_first_turn):
    agari_info = AgariInfo(
        is_tsumo_agari=is_tsumo_agari,
        player_wind=player_wind,
        is_first_turn=is_first_turn,
    )
    assert_yaku_check("123456789m11199p", expected, EarthlyHand(), agari_info)
