import pytest

from pymahjongutil.hand_parser import get_hand_from_code
from pymahjongutil.schema.count import HandCount
from pymahjongutil.schema.tile import Tiles


# fmt: off
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123s456p99m,chi123s,chi12-3s",
            [
                0, 0, 0, 0, 0, 0, 0, 0, 2,
                0, 0, 0, 1, 1, 1, 0, 0, 0,
                3, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0,
            ],
        ),
        (
            "123s123456789p99m",
            [
                0, 0, 0, 0, 0, 0, 0, 0, 2,
                1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0,
            ],
        ),
        (
            "123s456p99m,cok111-1z,cok3-333z",
            [
                0, 0, 0, 0, 0, 0, 0, 0, 2,
                0, 0, 0, 1, 1, 1, 0, 0, 0,
                1, 1, 1, 0, 0, 0, 0, 0, 0,
                4, 0, 4, 0, 0, 0, 0,
            ],
        ),
    ],
)
# fmt: on
def test_hand_counts(test_input, expected):
    hand_count = HandCount.create_from_hand(get_hand_from_code(test_input))
    for tile, tile_count in zip(Tiles.DEFAULTS, expected):
        assert hand_count[tile] == tile_count
