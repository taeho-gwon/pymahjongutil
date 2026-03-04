import pytest

from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.tile_index import TileIndex
from pymahjongutil.schema.wall import Wall


def _make_wall() -> Wall:
    tiles = [GameTile(tile_index=TileIndex(i % 34)) for i in range(136)]
    return Wall(tiles=tiles)


class TestWall:
    def test_valid_wall(self) -> None:
        wall = _make_wall()
        assert len(wall.tiles) == 136

    def test_invalid_wall_size(self) -> None:
        tiles = [GameTile(tile_index=TileIndex(0)) for _ in range(100)]
        with pytest.raises(ValueError, match="136"):
            Wall(tiles=tiles)

    def test_live_wall(self) -> None:
        wall = _make_wall()
        assert len(wall.live_wall) == 122

    def test_dead_wall(self) -> None:
        wall = _make_wall()
        assert len(wall.dead_wall) == 14

    def test_dora_indicators(self) -> None:
        wall = _make_wall()
        indicators = wall.dora_indicators
        assert len(indicators) == 4
        assert indicators[0] is wall.tiles[132]
        assert indicators[1] is wall.tiles[130]
        assert indicators[2] is wall.tiles[128]
        assert indicators[3] is wall.tiles[126]

    def test_ura_dora_indicators(self) -> None:
        wall = _make_wall()
        indicators = wall.ura_dora_indicators
        assert len(indicators) == 4
        assert indicators[0] is wall.tiles[133]
        assert indicators[1] is wall.tiles[131]
        assert indicators[2] is wall.tiles[129]
        assert indicators[3] is wall.tiles[127]

    def test_rinshan_tiles(self) -> None:
        wall = _make_wall()
        rinshan = wall.rinshan_tiles
        assert len(rinshan) == 4
        assert rinshan[0] is wall.tiles[134]
        assert rinshan[1] is wall.tiles[135]
        assert rinshan[2] is wall.tiles[122]
        assert rinshan[3] is wall.tiles[123]
