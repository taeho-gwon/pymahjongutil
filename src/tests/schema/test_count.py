import pytest

from src.enum.common import TileTypeEnum
from src.hand_parser import get_hand_from_code
from src.schema.count import HandCount
from src.schema.tile import Tile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123s456p99m,chi123s,chi12-3s",
            {
                Tile(type=TileTypeEnum.SOU, value=1): 3,
                Tile(type=TileTypeEnum.SOU, value=2): 3,
                Tile(type=TileTypeEnum.SOU, value=3): 3,
                Tile(type=TileTypeEnum.PIN, value=4): 1,
                Tile(type=TileTypeEnum.PIN, value=5): 1,
                Tile(type=TileTypeEnum.PIN, value=6): 1,
                Tile(type=TileTypeEnum.MAN, value=9): 2,
            },
        ),
        (
            "123s123456789p99m",
            {
                Tile(type=TileTypeEnum.SOU, value=1): 1,
                Tile(type=TileTypeEnum.SOU, value=2): 1,
                Tile(type=TileTypeEnum.SOU, value=3): 1,
                Tile(type=TileTypeEnum.PIN, value=1): 1,
                Tile(type=TileTypeEnum.PIN, value=2): 1,
                Tile(type=TileTypeEnum.PIN, value=3): 1,
                Tile(type=TileTypeEnum.PIN, value=4): 1,
                Tile(type=TileTypeEnum.PIN, value=5): 1,
                Tile(type=TileTypeEnum.PIN, value=6): 1,
                Tile(type=TileTypeEnum.PIN, value=7): 1,
                Tile(type=TileTypeEnum.PIN, value=8): 1,
                Tile(type=TileTypeEnum.PIN, value=9): 1,
                Tile(type=TileTypeEnum.MAN, value=9): 2,
            },
        ),
        (
            "123s456p99m,cok111-1z,cok3-333z",
            {
                Tile(type=TileTypeEnum.SOU, value=1): 1,
                Tile(type=TileTypeEnum.SOU, value=2): 1,
                Tile(type=TileTypeEnum.SOU, value=3): 1,
                Tile(type=TileTypeEnum.PIN, value=4): 1,
                Tile(type=TileTypeEnum.PIN, value=5): 1,
                Tile(type=TileTypeEnum.PIN, value=6): 1,
                Tile(type=TileTypeEnum.MAN, value=9): 2,
                Tile(type=TileTypeEnum.WIND, value=1): 4,
                Tile(type=TileTypeEnum.WIND, value=3): 4,
            },
        ),
    ],
)
def test_hand_counts(test_input, expected):
    hand_count = HandCount.create_from_hand(get_hand_from_code(test_input))
    for key, val in expected.items():
        assert hand_count[key] == val
