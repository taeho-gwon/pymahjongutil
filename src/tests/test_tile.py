from contextlib import nullcontext

import pytest

from src.enum.common import TileType
from src.schema.tile import Tile


@pytest.mark.parametrize(
    "tile_type, value",
    [(TileType.MAN, 5), (TileType.DRAGON, 3), (TileType.WIND, 3), (TileType.SOU, 9)],
)
def test_tile_validate_success(tile_type, value):
    with nullcontext():
        Tile(type=tile_type, value=value)


@pytest.mark.parametrize(
    "tile_type, value",
    [(TileType.MAN, 10), (TileType.DRAGON, 4), (TileType.WIND, 5), (TileType.SOU, 0)],
)
def test_tile_validate_fail(tile_type, value):
    with pytest.raises(ValueError):
        Tile(type=tile_type, value=value)
