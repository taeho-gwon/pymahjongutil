from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.tile_index import TileIndex


class TestGameTile:
    def test_create_default(self) -> None:
        tile = GameTile(tile_index=TileIndex(0))
        assert tile.tile_index == TileIndex(0)
        assert tile.is_red is False

    def test_create_red(self) -> None:
        tile = GameTile(tile_index=TileIndex(4), is_red=True)
        assert tile.tile_index == TileIndex(4)
        assert tile.is_red is True

    def test_equality(self) -> None:
        tile1 = GameTile(tile_index=TileIndex(0), is_red=False)
        tile2 = GameTile(tile_index=TileIndex(0), is_red=False)
        assert tile1 == tile2

    def test_inequality_by_red(self) -> None:
        tile1 = GameTile(tile_index=TileIndex(4), is_red=False)
        tile2 = GameTile(tile_index=TileIndex(4), is_red=True)
        assert tile1 != tile2
