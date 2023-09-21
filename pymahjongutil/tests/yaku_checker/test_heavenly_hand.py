import pytest

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.heavenly_hand import HeavenlyHand
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_tsumo_agari, player_wind, is_first_turn, expected",
    [
        (True, WindEnum.EAST, True, True),
        (True, WindEnum.SOUTH, True, False),
        (True, WindEnum.EAST, False, False),
        (False, WindEnum.EAST, True, False),
    ],
)
def test_heavenly_hand(is_tsumo_agari, player_wind, is_first_turn, expected):
    agari_info = AgariInfo(
        is_tsumo_agari=is_tsumo_agari,
        player_wind=player_wind,
        is_first_turn=is_first_turn,
    )
    assert_yaku_check("123456789m11199p", expected, HeavenlyHand(), agari_info)
