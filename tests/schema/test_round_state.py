import pytest

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.player_state import PlayerState
from pymahjongutil.schema.round_state import RoundState
from pymahjongutil.schema.tile_index import TileIndex
from pymahjongutil.schema.wall import Wall


def _make_wall() -> Wall:
    return Wall(tiles=[GameTile(tile_index=TileIndex(i % 34)) for i in range(136)])


def _make_player(hand_size: int = 13, score: int = 25000) -> PlayerState:
    return PlayerState(
        hand=[GameTile(tile_index=TileIndex(i % 34)) for i in range(hand_size)],
        discards=[],
        calls=[],
        score=score,
    )


def _make_round_state(**kwargs: object) -> RoundState:
    defaults: dict[str, object] = {
        "round_wind": WindEnum.EAST,
        "round_number": 1,
        "honba": 0,
        "riichi_sticks": 0,
        "dealer": 0,
        "current_player": 0,
        "wall": _make_wall(),
        "draw_index": 52,
        "players": [_make_player() for _ in range(4)],
    }
    defaults.update(kwargs)
    return RoundState(**defaults)  # type: ignore[arg-type]


class TestRoundState:
    def test_create_default(self) -> None:
        state = _make_round_state()
        assert state.round_wind is WindEnum.EAST
        assert state.round_number == 1
        assert state.honba == 0
        assert state.riichi_sticks == 0
        assert state.dealer == 0
        assert state.current_player == 0
        assert state.draw_index == 52
        assert state.dora_count == 1
        assert state.action_history == []

    def test_players_count_validation(self) -> None:
        with pytest.raises(ValueError, match="4"):
            _make_round_state(players=[_make_player() for _ in range(3)])

    def test_players_count_five_raises(self) -> None:
        with pytest.raises(ValueError, match="4"):
            _make_round_state(players=[_make_player() for _ in range(5)])

    def test_draw_index_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="draw_index"):
            _make_round_state(draw_index=-1)

    def test_draw_index_over_max_raises(self) -> None:
        with pytest.raises(ValueError, match="draw_index"):
            _make_round_state(draw_index=123)

    def test_draw_index_boundary(self) -> None:
        state = _make_round_state(draw_index=0)
        assert state.draw_index == 0

        state = _make_round_state(draw_index=122)
        assert state.draw_index == 122

    def test_initial_deal_scenario(self) -> None:
        """배패 직후 상태: 각 플레이어 13장, 친 14장째 쯔모 전."""
        players = [_make_player() for _ in range(4)]
        state = _make_round_state(
            round_wind=WindEnum.EAST,
            round_number=1,
            dealer=0,
            current_player=0,
            draw_index=52,
            players=players,
        )
        assert all(len(p.hand) == 13 for p in state.players)
        assert state.draw_index == 52
        assert state.dealer == 0
        assert state.current_player == 0

    def test_custom_dora_count(self) -> None:
        state = _make_round_state(dora_count=3)
        assert state.dora_count == 3
