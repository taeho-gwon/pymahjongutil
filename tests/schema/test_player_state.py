from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.game_call import GameCall
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.player_state import PlayerState
from pymahjongutil.schema.tile_index import TileIndex


def _make_hand(count: int = 13) -> list[GameTile]:
    return [GameTile(tile_index=TileIndex(i % 34)) for i in range(count)]


class TestPlayerState:
    def test_create_default(self) -> None:
        state = PlayerState(hand=_make_hand(), discards=[], calls=[])
        assert len(state.hand) == 13
        assert state.discards == []
        assert state.calls == []
        assert state.is_riichi is False
        assert state.score == 25000

    def test_create_with_discards(self) -> None:
        discards = [
            GameTile(tile_index=TileIndex(0)),
            GameTile(tile_index=TileIndex(1)),
        ]
        state = PlayerState(hand=_make_hand(), discards=discards, calls=[])
        assert len(state.discards) == 2

    def test_create_with_calls(self) -> None:
        call = GameCall(
            type=CallTypeEnum.PON,
            tiles=[GameTile(tile_index=TileIndex(0)) for _ in range(3)],
            call_idx=1,
        )
        state = PlayerState(hand=_make_hand(10), discards=[], calls=[call])
        assert len(state.calls) == 1

    def test_riichi_state(self) -> None:
        state = PlayerState(hand=_make_hand(), discards=[], calls=[], is_riichi=True)
        assert state.is_riichi is True

    def test_custom_score(self) -> None:
        state = PlayerState(hand=_make_hand(), discards=[], calls=[], score=30000)
        assert state.score == 30000
