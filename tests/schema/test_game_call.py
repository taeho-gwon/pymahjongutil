from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.game_call import GameCall
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.tile_index import TileIndex


class TestGameCall:
    def test_create_chii(self) -> None:
        tiles = [
            GameTile(tile_index=TileIndex(0)),
            GameTile(tile_index=TileIndex(1)),
            GameTile(tile_index=TileIndex(2)),
        ]
        call = GameCall(type=CallTypeEnum.CHII, tiles=tiles, call_idx=0)
        assert call.type is CallTypeEnum.CHII
        assert len(call.tiles) == 3
        assert call.call_idx == 0

    def test_create_pon(self) -> None:
        tiles = [
            GameTile(tile_index=TileIndex(0)),
            GameTile(tile_index=TileIndex(0)),
            GameTile(tile_index=TileIndex(0)),
        ]
        call = GameCall(type=CallTypeEnum.PON, tiles=tiles, call_idx=1)
        assert call.type is CallTypeEnum.PON
        assert call.call_idx == 1

    def test_create_with_red(self) -> None:
        tiles = [
            GameTile(tile_index=TileIndex(4), is_red=True),
            GameTile(tile_index=TileIndex(4)),
            GameTile(tile_index=TileIndex(4)),
        ]
        call = GameCall(type=CallTypeEnum.PON, tiles=tiles, call_idx=2)
        assert call.tiles[0].is_red is True
        assert call.tiles[1].is_red is False

    def test_create_kan(self) -> None:
        tiles = [GameTile(tile_index=TileIndex(0)) for _ in range(4)]
        call = GameCall(type=CallTypeEnum.BIG_MELDED_KAN, tiles=tiles, call_idx=0)
        assert call.type is CallTypeEnum.BIG_MELDED_KAN
        assert len(call.tiles) == 4
