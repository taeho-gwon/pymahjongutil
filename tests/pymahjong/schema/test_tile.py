import pytest

from pymahjong.schema.tile import Tile


@pytest.mark.parametrize(
    "test_prev, test_next",
    [
        (Tile(value=7), Tile(value=8)),
        (Tile(value=10), Tile(value=11)),
        (Tile(value=21), Tile(value=22)),
    ],
)
def test_tile_next_prev(test_prev, test_next):
    assert test_prev.next == test_next
    assert test_next.prev == test_prev
