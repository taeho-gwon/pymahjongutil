from pymahjongutil.enum.common import ActionTypeEnum
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.tile_index import TileIndex


class TestRoundAction:
    def test_draw_action(self) -> None:
        tile = GameTile(tile_index=TileIndex(0))
        action = RoundAction(
            type=ActionTypeEnum.DRAW,
            actor=0,
            tiles=[tile],
        )
        assert action.type is ActionTypeEnum.DRAW
        assert action.actor == 0
        assert action.tiles == [tile]
        assert action.target is None

    def test_discard_action(self) -> None:
        tile = GameTile(tile_index=TileIndex(5))
        action = RoundAction(
            type=ActionTypeEnum.DISCARD,
            actor=1,
            tiles=[tile],
        )
        assert action.type is ActionTypeEnum.DISCARD
        assert action.actor == 1

    def test_chii_action(self) -> None:
        tiles = [
            GameTile(tile_index=TileIndex(0)),
            GameTile(tile_index=TileIndex(1)),
            GameTile(tile_index=TileIndex(2)),
        ]
        action = RoundAction(
            type=ActionTypeEnum.CHII,
            actor=1,
            tiles=tiles,
            target=0,
        )
        assert action.type is ActionTypeEnum.CHII
        assert action.target == 0
        assert len(action.tiles) == 3

    def test_ron_action(self) -> None:
        tile = GameTile(tile_index=TileIndex(33))
        action = RoundAction(
            type=ActionTypeEnum.RON,
            actor=2,
            tiles=[tile],
            target=0,
        )
        assert action.type is ActionTypeEnum.RON
        assert action.target == 0
