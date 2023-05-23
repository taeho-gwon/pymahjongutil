import pytest

from pymahjong.hand_checker.riichi_checker import RiichiChecker
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.tile import Tile
from pymahjong.yaku_checker.yakuman.chinrotou import Chinrotou


@pytest.mark.parametrize(
    "test_input, agari_tile, expected",
    [
        ("111999p111999s11m", Tile(0), True),
        ("11m,pon999p,cok1111s,bmk9999s,pon111p", Tile(0), True),
        ("1199m1199p1199s11z", Tile(0), False),
    ],
)
def test_chinrotou(test_input, agari_tile, expected):
    hand = get_hand_from_code(test_input)
    result = any(
        Chinrotou().is_satisfied(division, AgariInfo())
        for division in RiichiChecker(hand).calculate_divisions(True)
    )
    assert result == expected
