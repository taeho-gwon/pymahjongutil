import pytest

from pymahjong.enum.common import TileTypeEnum
from pymahjong.schema.tile import Tile


@pytest.mark.parametrize(
    "test_prev, test_next",
    [
        (Tile(type=TileTypeEnum.PIN, value=2), Tile(type=TileTypeEnum.PIN, value=3)),
        (Tile(type=TileTypeEnum.MAN, value=8), Tile(type=TileTypeEnum.MAN, value=9)),
        (Tile(type=TileTypeEnum.SOU, value=4), Tile(type=TileTypeEnum.SOU, value=5)),
    ],
)
def test_tile_next_prev(test_prev, test_next):
    assert test_prev.next == test_next
    assert test_next.prev == test_prev
