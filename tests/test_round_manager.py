from pymahjongutil.enum.common import (
    ActionTypeEnum,
    CallTypeEnum,
    RoundResultTypeEnum,
    WindEnum,
    YakuEnum,
)
from pymahjongutil.round_manager import RoundManager
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.round_record import RoundRecord
from pymahjongutil.schema.round_result import RoundResult
from pymahjongutil.schema.tile_index import TileIndex
from pymahjongutil.schema.wall import Wall


def _gt(index: int, is_red: bool = False) -> GameTile:
    return GameTile(tile_index=TileIndex(index), is_red=is_red)


def _act(
    type: ActionTypeEnum,
    actor: int,
    tiles: list[GameTile],
    target: int | None = None,
) -> RoundAction:
    return RoundAction(type=type, actor=actor, tiles=tiles, target=target)


def _make_standard_wall() -> Wall:
    tiles: list[GameTile] = []
    for copy in range(4):
        for idx in range(34):
            is_red = copy == 0 and idx in (4, 13, 22)
            tiles.append(_gt(idx, is_red=is_red))
    return Wall(tiles=tiles)


def _make_record(
    initial_hands: list[list[GameTile]] | None = None,
    scores: list[int] | None = None,
    dealer: int = 0,
    riichi_sticks: int = 0,
    honba: int = 0,
) -> RoundRecord:
    if initial_hands is None:
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]
    if scores is None:
        scores = [25000, 25000, 25000, 25000]
    return RoundRecord(
        round_wind=WindEnum.EAST,
        round_number=1,
        honba=honba,
        riichi_sticks=riichi_sticks,
        scores=scores,
        dealer=dealer,
        wall=_make_standard_wall(),
        initial_hands=initial_hands,
    )


class TestCreateFromRecord:
    def test_basic_creation(self) -> None:
        record = _make_record()
        manager = RoundManager.create_from_record(record)
        s = manager.state

        assert s.round_wind is WindEnum.EAST
        assert s.round_number == 1
        assert s.honba == 0
        assert s.riichi_sticks == 0
        assert s.dealer == 0
        assert s.current_player == 0
        assert s.draw_index == 0
        assert s.dora_count == 1
        assert len(s.players) == 4
        assert len(s.action_history) == 0

    def test_initial_player_state(self) -> None:
        record = _make_record(scores=[30000, 25000, 20000, 25000])
        manager = RoundManager.create_from_record(record)

        for _i, p in enumerate(manager.state.players):
            assert len(p.hand) == 13
            assert p.discards == []
            assert p.calls == []
            assert p.is_riichi is False
        assert manager.state.players[0].score == 30000
        assert manager.state.players[2].score == 20000

    def test_dealer_as_current_player(self) -> None:
        record = _make_record(dealer=2)
        manager = RoundManager.create_from_record(record)
        assert manager.state.current_player == 2


class TestDrawAndDiscard:
    def test_draw(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        tile = _gt(27)
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [tile]))

        assert len(manager.state.players[0].hand) == 14
        assert manager.state.draw_index == 1
        assert manager.state.current_player == 0

    def test_discard(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(27)]))

        assert len(manager.state.players[0].hand) == 13
        assert manager.state.players[0].discards == [_gt(27)]
        assert manager.state.current_player == 1

    def test_draw_discard_cycle(self) -> None:
        manager = RoundManager.create_from_record(_make_record())

        for player_id in range(4):
            manager.apply_action(_act(ActionTypeEnum.DRAW, player_id, [_gt(27)]))
            manager.apply_action(_act(ActionTypeEnum.DISCARD, player_id, [_gt(27)]))

        assert manager.state.draw_index == 4
        assert manager.state.current_player == 0
        for p in manager.state.players:
            assert len(p.hand) == 13
            assert len(p.discards) == 1


class TestRiichi:
    def test_riichi_changes_state(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.RIICHI, 0, [_gt(27)]))

        p0 = manager.state.players[0]
        assert p0.is_riichi is True
        assert p0.score == 24000
        assert p0.discards == [_gt(27)]
        assert len(p0.hand) == 13
        assert manager.state.riichi_sticks == 1
        assert manager.state.current_player == 1

    def test_multiple_riichi(self) -> None:
        manager = RoundManager.create_from_record(_make_record())

        for pid in range(4):
            manager.apply_action(_act(ActionTypeEnum.DRAW, pid, [_gt(27)]))
            manager.apply_action(_act(ActionTypeEnum.RIICHI, pid, [_gt(27)]))

        assert manager.state.riichi_sticks == 4
        for p in manager.state.players:
            assert p.is_riichi is True
            assert p.score == 24000


class TestChii:
    def test_chii_proper(self) -> None:
        """Player 0 discards 4p(12), Player 1 calls CHII with 5p(13)+6p(14)+4p(12)."""
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(12)]))

        # Player 1 calls CHII: 13(5p), 14(6p) from hand + 12(4p) called
        manager.apply_action(
            _act(ActionTypeEnum.CHII, 1, [_gt(13), _gt(14), _gt(12)], target=0)
        )

        p1 = manager.state.players[1]
        assert len(p1.hand) == 11  # 13 - 2 tiles used for chii
        assert len(p1.calls) == 1
        assert p1.calls[0].type is CallTypeEnum.CHII
        assert p1.calls[0].call_idx == 2  # 12(4p) is at index 2
        assert manager.state.current_player == 1


class TestPon:
    def test_pon(self) -> None:
        """Player 0 discards 6m(5), Player 3 calls PON (has 2x 6m(5))."""
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [
                _gt(5),
                _gt(5),
                _gt(9),
                _gt(10),
                _gt(11),
                _gt(12),
                _gt(14),
                _gt(15),
                _gt(16),
                _gt(17),
                _gt(19),
                _gt(20),
                _gt(8),
            ],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(5)]))

        manager.apply_action(
            _act(ActionTypeEnum.PON, 3, [_gt(5), _gt(5), _gt(5)], target=0)
        )

        p3 = manager.state.players[3]
        assert len(p3.hand) == 11  # 13 - 2
        assert len(p3.calls) == 1
        assert p3.calls[0].type is CallTypeEnum.PON
        assert manager.state.current_player == 3


class TestKan:
    def test_concealed_kan(self) -> None:
        """Player 0 has 4x 1m(0), draws then declares CONCEALED_KAN."""
        initial_hands = [
            [
                _gt(0),
                _gt(0),
                _gt(0),
                _gt(0),
                _gt(1),
                _gt(2),
                _gt(3),
                _gt(4),
                _gt(5),
                _gt(6),
                _gt(7),
                _gt(8),
                _gt(9),
            ],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        manager.apply_action(
            _act(ActionTypeEnum.CONCEALED_KAN, 0, [_gt(0), _gt(0), _gt(0), _gt(0)])
        )

        p0 = manager.state.players[0]
        assert len(p0.hand) == 9  # 13 - 4
        assert len(p0.calls) == 1
        assert p0.calls[0].type is CallTypeEnum.CONCEALED_KAN
        assert manager.state.dora_count == 2
        assert manager.state.current_player == 0

    def test_big_melded_kan(self) -> None:
        """Player 0 discards 1m(0), Player 2 has 3x 1m(0) and calls BIG_MELDED_KAN."""
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [
                _gt(0),
                _gt(0),
                _gt(0),
                _gt(21),
                _gt(22),
                _gt(23),
                _gt(24),
                _gt(25),
                _gt(26),
                _gt(27),
                _gt(28),
                _gt(29),
                _gt(30),
            ],
            [_gt(i) for i in range(8, 21)],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(31)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(0)]))

        manager.apply_action(
            _act(
                ActionTypeEnum.BIG_MELDED_KAN,
                2,
                [_gt(0), _gt(0), _gt(0), _gt(0)],
                target=0,
            )
        )

        p2 = manager.state.players[2]
        assert len(p2.hand) == 10  # 13 - 3
        assert len(p2.calls) == 1
        assert p2.calls[0].type is CallTypeEnum.BIG_MELDED_KAN
        assert manager.state.dora_count == 2
        assert manager.state.current_player == 2

    def test_small_melded_kan(self) -> None:
        """Player 3 has PON of 6m(5), draws 4th 6m(5), declares SMALL_MELDED_KAN."""
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [
                _gt(5),
                _gt(5),
                _gt(9),
                _gt(10),
                _gt(11),
                _gt(12),
                _gt(14),
                _gt(15),
                _gt(16),
                _gt(17),
                _gt(19),
                _gt(20),
                _gt(8),
            ],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        # Player 0 draws, discards 6m(5)
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(5)]))

        # Player 3 PON
        manager.apply_action(
            _act(ActionTypeEnum.PON, 3, [_gt(5), _gt(5), _gt(5)], target=0)
        )
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 3, [_gt(8)]))

        # Next cycle
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(28)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(28)]))
        manager.apply_action(_act(ActionTypeEnum.DRAW, 1, [_gt(29)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 1, [_gt(29)]))
        manager.apply_action(_act(ActionTypeEnum.DRAW, 2, [_gt(30)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 2, [_gt(30)]))

        # Player 3 draws 4th 6m(5) and declares SMALL_MELDED_KAN
        manager.apply_action(_act(ActionTypeEnum.DRAW, 3, [_gt(5)]))
        manager.apply_action(
            _act(
                ActionTypeEnum.SMALL_MELDED_KAN,
                3,
                [_gt(5), _gt(5), _gt(5), _gt(5)],
            )
        )

        p3 = manager.state.players[3]
        # Hand: 13 - 2(pon) - 1(discard) + 1(draw) - 1(kan_add) = 10
        assert len(p3.hand) == 10
        assert len(p3.calls) == 1
        assert p3.calls[0].type is CallTypeEnum.SMALL_MELDED_KAN
        assert manager.state.dora_count == 2
        assert manager.state.current_player == 3


class TestTerminalActions:
    def test_tsumo(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.TSUMO, 0, [_gt(27)]))

        assert len(manager.state.action_history) == 2
        assert manager.state.action_history[-1].type is ActionTypeEnum.TSUMO

    def test_ron(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.RON, 1, [_gt(27)], target=0))

        assert len(manager.state.action_history) == 3
        assert manager.state.action_history[-1].type is ActionTypeEnum.RON

    def test_nine_tiles_draw(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.NINE_TILES_DRAW, 0, []))

        assert len(manager.state.action_history) == 2
        assert manager.state.action_history[-1].type is ActionTypeEnum.NINE_TILES_DRAW


class TestToRecord:
    def test_to_record_preserves_initial_state(self) -> None:
        record = _make_record(riichi_sticks=2, honba=1)
        manager = RoundManager.create_from_record(record)

        # Player 0 riichi → riichi_sticks changes in state
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.RIICHI, 0, [_gt(27)]))

        assert manager.state.riichi_sticks == 3

        result = RoundResult(
            type=RoundResultTypeEnum.TSUMO,
            winners=[0],
            han=[1],
            fu=[30],
            yakus=[[YakuEnum.READY]],
            point_diffs=[3000, -1000, -1000, -1000],
        )
        out = manager.to_record(result)

        assert out.riichi_sticks == 2  # initial value
        assert out.honba == 1
        assert out.scores == [25000, 25000, 25000, 25000]
        assert len(out.actions) == 2
        assert out.result is result

    def test_to_record_without_result(self) -> None:
        manager = RoundManager.create_from_record(_make_record())
        out = manager.to_record()
        assert out.result is None

    def test_to_record_initial_hands_unchanged(self) -> None:
        record = _make_record()
        manager = RoundManager.create_from_record(record)
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(0)]))

        out = manager.to_record()
        # initial_hands should have original 13 tiles including _gt(0)
        assert len(out.initial_hands[0]) == 13
        assert any(t.tile_index == TileIndex(0) for t in out.initial_hands[0])


class TestIntegrationRiichiTsumo:
    """Full riichi → tsumo flow."""

    def test_riichi_tsumo_flow(self) -> None:
        record = _make_record()
        manager = RoundManager.create_from_record(record)

        # 1순: all players draw and discard
        for pid in range(4):
            manager.apply_action(_act(ActionTypeEnum.DRAW, pid, [_gt(27)]))
            manager.apply_action(_act(ActionTypeEnum.DISCARD, pid, [_gt(27)]))

        # 2순: player 0 riichi
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(28)]))
        manager.apply_action(_act(ActionTypeEnum.RIICHI, 0, [_gt(28)]))

        # Others continue
        manager.apply_action(_act(ActionTypeEnum.DRAW, 1, [_gt(29)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 1, [_gt(29)]))
        manager.apply_action(_act(ActionTypeEnum.DRAW, 2, [_gt(30)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 2, [_gt(30)]))
        manager.apply_action(_act(ActionTypeEnum.DRAW, 3, [_gt(31)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 3, [_gt(31)]))

        # 3순: player 0 tsumo
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.TSUMO, 0, [_gt(27)]))

        s = manager.state
        assert s.players[0].is_riichi is True
        assert s.players[0].score == 24000
        assert s.riichi_sticks == 1
        assert s.draw_index == 9
        assert len(s.action_history) == 18

        result = RoundResult(
            type=RoundResultTypeEnum.TSUMO,
            winners=[0],
            han=[3],
            fu=[30],
            yakus=[[YakuEnum.READY, YakuEnum.SELF_DRAW, YakuEnum.ALL_SEQUENCES]],
            point_diffs=[4000, -1300, -1300, -1400],
        )
        out = manager.to_record(result)
        assert out.result is not None
        assert out.result.type is RoundResultTypeEnum.TSUMO
        assert sum(out.result.point_diffs) == 0


class TestIntegrationWithCalls:
    """Flow with PON → SMALL_MELDED_KAN."""

    def test_pon_to_small_melded_kan(self) -> None:
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [
                _gt(5),
                _gt(5),
                _gt(9),
                _gt(10),
                _gt(11),
                _gt(12),
                _gt(14),
                _gt(15),
                _gt(16),
                _gt(17),
                _gt(19),
                _gt(20),
                _gt(8),
            ],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        # Player 0 draws, discards 6m(5)
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(27)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(5)]))

        # Player 3 PON
        manager.apply_action(
            _act(ActionTypeEnum.PON, 3, [_gt(5), _gt(5), _gt(5)], target=0)
        )
        assert manager.state.players[3].calls[0].type is CallTypeEnum.PON
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 3, [_gt(8)]))

        # Full cycle
        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(28)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(28)]))
        manager.apply_action(_act(ActionTypeEnum.DRAW, 1, [_gt(29)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 1, [_gt(29)]))
        manager.apply_action(_act(ActionTypeEnum.DRAW, 2, [_gt(30)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 2, [_gt(30)]))

        # Player 3 draws 4th 6m(5) and kans
        manager.apply_action(_act(ActionTypeEnum.DRAW, 3, [_gt(5)]))
        manager.apply_action(
            _act(
                ActionTypeEnum.SMALL_MELDED_KAN,
                3,
                [_gt(5), _gt(5), _gt(5), _gt(5)],
            )
        )

        p3 = manager.state.players[3]
        assert p3.calls[0].type is CallTypeEnum.SMALL_MELDED_KAN
        assert manager.state.dora_count == 2

        # Rinshan draw and discard
        manager.apply_action(_act(ActionTypeEnum.DRAW, 3, [_gt(31)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 3, [_gt(31)]))

        result = RoundResult(
            type=RoundResultTypeEnum.EXHAUSTIVE_DRAW,
            is_tenpai=[False, False, False, False],
            point_diffs=[0, 0, 0, 0],
        )
        out = manager.to_record(result)
        assert out.result is not None
        assert out.result.type is RoundResultTypeEnum.EXHAUSTIVE_DRAW


class TestIntegrationSpecialDraw:
    """Nine tiles draw flow."""

    def test_nine_tiles_draw_flow(self) -> None:
        initial_hands = [
            [
                _gt(0),
                _gt(8),
                _gt(9),
                _gt(17),
                _gt(18),
                _gt(26),
                _gt(27),
                _gt(28),
                _gt(29),
                _gt(30),
                _gt(31),
                _gt(32),
                _gt(33),
            ],
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(8, 21)],
        ]
        manager = RoundManager.create_from_record(_make_record(initial_hands))

        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(5)]))
        manager.apply_action(_act(ActionTypeEnum.NINE_TILES_DRAW, 0, []))

        assert len(manager.state.action_history) == 2

        result = RoundResult(
            type=RoundResultTypeEnum.NINE_TILES_DRAW,
            point_diffs=[0, 0, 0, 0],
        )
        out = manager.to_record(result)
        assert out.result is not None
        assert out.result.type is RoundResultTypeEnum.NINE_TILES_DRAW
        assert len(out.initial_hands[0]) == 13


class TestIntegrationDoubleRon:
    """Double ron flow."""

    def test_double_ron(self) -> None:
        manager = RoundManager.create_from_record(_make_record())

        manager.apply_action(_act(ActionTypeEnum.DRAW, 0, [_gt(33)]))
        manager.apply_action(_act(ActionTypeEnum.DISCARD, 0, [_gt(33)]))
        manager.apply_action(_act(ActionTypeEnum.RON, 1, [_gt(33)], target=0))
        manager.apply_action(_act(ActionTypeEnum.RON, 3, [_gt(33)], target=0))

        assert len(manager.state.action_history) == 4

        result = RoundResult(
            type=RoundResultTypeEnum.RON,
            winners=[1, 3],
            loser=0,
            han=[1, 2],
            fu=[30, 40],
            yakus=[[YakuEnum.READY], [YakuEnum.READY, YakuEnum.ONE_SHOT]],
            point_diffs=[-3600, 1000, 0, 2600],
        )
        out = manager.to_record(result)
        assert out.result is not None
        assert len(out.result.winners) == 2
        assert sum(out.result.point_diffs) == 0
