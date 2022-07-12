import pytest

from src.enum.common import TileType
from src.schema.tile import Tile


@pytest.mark.parametrize(
    "test_prev, test_next",
    [
        (Tile(type=TileType.PIN, value=2), Tile(type=TileType.PIN, value=3)),
        (Tile(type=TileType.MAN, value=8), Tile(type=TileType.MAN, value=9)),
        (Tile(type=TileType.SOU, value=4), Tile(type=TileType.SOU, value=5)),
    ],
)
def test_tile_next_prev(test_prev, test_next):
    assert test_prev.next == test_next
    assert test_next.prev == test_prev
