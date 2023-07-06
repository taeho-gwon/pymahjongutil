import pytest

from pymahjong.enum.common import TileTypeEnum
from pymahjong.schema.tile import Tile


@pytest.mark.parametrize(
    "tile_num, expected",
    [
        (0, TileTypeEnum.MAN),
        (8, TileTypeEnum.MAN),
        (9, TileTypeEnum.PIN),
        (17, TileTypeEnum.PIN),
        (18, TileTypeEnum.SOU),
        (26, TileTypeEnum.SOU),
        (27, TileTypeEnum.WIND),
        (30, TileTypeEnum.WIND),
        (31, TileTypeEnum.DRAGON),
        (33, TileTypeEnum.DRAGON),
    ],
)
def test_tile_type(tile_num, expected):
    assert Tile(value=tile_num).type is expected
