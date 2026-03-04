import pytest

from pymahjongutil.enum.common import (
    ActionTypeEnum,
    RoundResultTypeEnum,
    WindEnum,
)
from pymahjongutil.game_manager import GameManager
from pymahjongutil.schema.game_record import GameRecord
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.round_record import RoundRecord
from pymahjongutil.schema.round_result import RoundResult
from pymahjongutil.schema.tile_index import TileIndex
from pymahjongutil.schema.wall import Wall


def _gt(index: int) -> GameTile:
    return GameTile(tile_index=TileIndex(index), is_red=False)


def _make_wall() -> Wall:
    tiles: list[GameTile] = []
    for _copy in range(4):
        for idx in range(34):
            tiles.append(_gt(idx))
    return Wall(tiles=tiles)


def _make_round_record(
    round_wind: WindEnum = WindEnum.EAST,
    round_number: int = 1,
    honba: int = 0,
    riichi_sticks: int = 0,
    scores: list[int] | None = None,
    dealer: int = 0,
    result: RoundResult | None = None,
    actions: list[RoundAction] | None = None,
) -> RoundRecord:
    if scores is None:
        scores = [25000, 25000, 25000, 25000]
    initial_hands = [
        [_gt(i) for i in range(13)],
        [_gt(i) for i in range(13, 26)],
        [_gt(i) for i in range(21, 34)],
        [_gt(i) for i in range(8, 21)],
    ]
    return RoundRecord(
        round_wind=round_wind,
        round_number=round_number,
        honba=honba,
        riichi_sticks=riichi_sticks,
        scores=scores,
        dealer=dealer,
        wall=_make_wall(),
        initial_hands=initial_hands,
        actions=actions if actions is not None else [],
        result=result,
    )


def _tsumo_result(winners: list[int], point_diffs: list[int]) -> RoundResult:
    return RoundResult(
        type=RoundResultTypeEnum.TSUMO,
        winners=winners,
        point_diffs=point_diffs,
    )


def _ron_result(winners: list[int], loser: int, point_diffs: list[int]) -> RoundResult:
    return RoundResult(
        type=RoundResultTypeEnum.RON,
        winners=winners,
        loser=loser,
        point_diffs=point_diffs,
    )


def _exhaustive_draw_result(
    is_tenpai: list[bool], point_diffs: list[int]
) -> RoundResult:
    return RoundResult(
        type=RoundResultTypeEnum.EXHAUSTIVE_DRAW,
        is_tenpai=is_tenpai,
        point_diffs=point_diffs,
    )


class TestCreateNew:
    def test_default_scores(self) -> None:
        gm = GameManager.create_new()
        s = gm.state
        assert s.round_wind is WindEnum.EAST
        assert s.round_number == 1
        assert s.honba == 0
        assert s.riichi_sticks == 0
        assert s.scores == [25000, 25000, 25000, 25000]
        assert s.round_records == []

    def test_custom_scores(self) -> None:
        gm = GameManager.create_new([30000, 25000, 20000, 25000])
        assert gm.state.scores == [30000, 25000, 20000, 25000]

    def test_dealer_property(self) -> None:
        gm = GameManager.create_new()
        assert gm.state.dealer == 0


class TestDealerWinContinuation:
    def test_dealer_tsumo_continues(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=_tsumo_result([0], [4000, -1000, -1000, -2000]),
        )
        gm.complete_round(record)

        s = gm.state
        assert s.round_wind is WindEnum.EAST
        assert s.round_number == 1
        assert s.honba == 1
        assert s.scores == [29000, 24000, 24000, 23000]

    def test_dealer_ron_continues(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=_ron_result([0], 1, [8000, -8000, 0, 0]),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1


class TestNonDealerWin:
    def test_non_dealer_tsumo_advances(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=_tsumo_result([1], [-2000, 6000, -2000, -2000]),
        )
        gm.complete_round(record)

        s = gm.state
        assert s.round_wind is WindEnum.EAST
        assert s.round_number == 2
        assert s.honba == 0

    def test_non_dealer_ron_advances(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=_ron_result([2], 0, [-8000, 0, 8000, 0]),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 2
        assert gm.state.honba == 0


class TestExhaustiveDraw:
    def test_dealer_tenpai_continues(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=_exhaustive_draw_result(
                [True, False, False, False], [3000, -1000, -1000, -1000]
            ),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1

    def test_dealer_noten_advances(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=_exhaustive_draw_result(
                [False, True, False, False], [-1000, 3000, -1000, -1000]
            ),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 2
        assert gm.state.honba == 1


class TestSpecialDraws:
    def test_four_winds_draw(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=RoundResult(
                type=RoundResultTypeEnum.FOUR_WINDS_DRAW,
                point_diffs=[0, 0, 0, 0],
            ),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1

    def test_four_kans_draw(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=RoundResult(
                type=RoundResultTypeEnum.FOUR_KANS_DRAW,
                point_diffs=[0, 0, 0, 0],
            ),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1

    def test_four_riichi_draw(self) -> None:
        gm = GameManager.create_new()
        actions = [
            RoundAction(type=ActionTypeEnum.RIICHI, actor=i, tiles=[_gt(0)])
            for i in range(4)
        ]
        record = _make_round_record(
            result=RoundResult(
                type=RoundResultTypeEnum.FOUR_RIICHI_DRAW,
                point_diffs=[0, 0, 0, 0],
            ),
            actions=actions,
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1
        assert gm.state.riichi_sticks == 4

    def test_nine_tiles_draw(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=RoundResult(
                type=RoundResultTypeEnum.NINE_TILES_DRAW,
                point_diffs=[0, 0, 0, 0],
            ),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1

    def test_three_ron_draw(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record(
            result=RoundResult(
                type=RoundResultTypeEnum.THREE_RON_DRAW,
                point_diffs=[0, 0, 0, 0],
            ),
        )
        gm.complete_round(record)

        assert gm.state.round_number == 1
        assert gm.state.honba == 1


class TestRiichiSticks:
    def test_win_clears_riichi_sticks(self) -> None:
        gm = GameManager.create_new()
        # First round: exhaustive draw with 2 riichi
        actions = [
            RoundAction(type=ActionTypeEnum.RIICHI, actor=0, tiles=[_gt(0)]),
            RoundAction(type=ActionTypeEnum.RIICHI, actor=1, tiles=[_gt(0)]),
        ]
        record1 = _make_round_record(
            result=_exhaustive_draw_result(
                [True, True, False, False], [1500, 1500, -1500, -1500]
            ),
            actions=actions,
        )
        gm.complete_round(record1)
        assert gm.state.riichi_sticks == 2

        # Second round: someone wins → sticks cleared
        record2 = _make_round_record(
            result=_tsumo_result([0], [4000, -1000, -1000, -2000]),
        )
        gm.complete_round(record2)
        assert gm.state.riichi_sticks == 0

    def test_draw_accumulates_riichi_sticks(self) -> None:
        gm = GameManager.create_new()
        actions = [
            RoundAction(type=ActionTypeEnum.RIICHI, actor=0, tiles=[_gt(0)]),
        ]
        record = _make_round_record(
            result=_exhaustive_draw_result(
                [True, False, False, False], [3000, -1000, -1000, -1000]
            ),
            actions=actions,
        )
        gm.complete_round(record)
        assert gm.state.riichi_sticks == 1


class TestWindTransition:
    def test_east_4_to_south_1(self) -> None:
        gm = GameManager.create_new()
        # Advance through east 1-4 with non-dealer wins
        for round_num in range(1, 5):
            dealer = round_num - 1
            winner = (dealer + 1) % 4
            diffs = [0, 0, 0, 0]
            diffs[winner] = 8000
            diffs[dealer] = -8000
            record = _make_round_record(
                result=_ron_result([winner], dealer, diffs),
            )
            gm.complete_round(record)

        assert gm.state.round_wind is WindEnum.SOUTH
        assert gm.state.round_number == 1

    def test_full_hanchan_to_game_over(self) -> None:
        gm = GameManager.create_new()
        # East 1-4
        for _ in range(4):
            winner = (gm.state.dealer + 1) % 4
            diffs = [0, 0, 0, 0]
            diffs[winner] = 8000
            diffs[gm.state.dealer] = -8000
            record = _make_round_record(
                result=_ron_result([winner], gm.state.dealer, diffs),
            )
            gm.complete_round(record)

        assert gm.state.round_wind is WindEnum.SOUTH
        assert not gm.is_game_over

        # South 1-4
        for _ in range(4):
            winner = (gm.state.dealer + 1) % 4
            diffs = [0, 0, 0, 0]
            diffs[winner] = 8000
            diffs[gm.state.dealer] = -8000
            record = _make_round_record(
                result=_ron_result([winner], gm.state.dealer, diffs),
            )
            gm.complete_round(record)

        assert gm.state.round_wind is WindEnum.WEST
        assert gm.is_game_over


class TestIsGameOver:
    def test_not_over_at_start(self) -> None:
        gm = GameManager.create_new()
        assert not gm.is_game_over

    def test_not_over_during_south(self) -> None:
        gm = GameManager.create_new()
        # Advance to south
        for _ in range(4):
            winner = (gm.state.dealer + 1) % 4
            diffs = [0, 0, 0, 0]
            diffs[winner] = 8000
            diffs[gm.state.dealer] = -8000
            record = _make_round_record(
                result=_ron_result([winner], gm.state.dealer, diffs),
            )
            gm.complete_round(record)

        assert gm.state.round_wind is WindEnum.SOUTH
        assert not gm.is_game_over


class TestCreateFromRecord:
    def test_restore_from_record(self) -> None:
        gm = GameManager.create_new()
        records: list[RoundRecord] = []

        # Play 2 rounds
        r1 = _make_round_record(
            result=_tsumo_result([0], [4000, -1000, -1000, -2000]),
        )
        gm.complete_round(r1)
        records.append(r1)

        r2 = _make_round_record(
            result=_tsumo_result([1], [-2000, 6000, -2000, -2000]),
        )
        gm.complete_round(r2)
        records.append(r2)

        game_record = GameRecord(
            initial_scores=[25000, 25000, 25000, 25000],
            rounds=records,
        )

        restored = GameManager.create_from_record(game_record)
        assert restored.state.scores == gm.state.scores
        assert restored.state.round_wind is gm.state.round_wind
        assert restored.state.round_number == gm.state.round_number
        assert restored.state.honba == gm.state.honba
        assert restored.state.riichi_sticks == gm.state.riichi_sticks


class TestToRecord:
    def test_to_record(self) -> None:
        gm = GameManager.create_new()
        r1 = _make_round_record(
            result=_tsumo_result([0], [4000, -1000, -1000, -2000]),
        )
        gm.complete_round(r1)

        game_record = gm.to_record()
        assert game_record.initial_scores == [25000, 25000, 25000, 25000]
        assert len(game_record.rounds) == 1


class TestCompleteRoundRequiresResult:
    def test_no_result_raises(self) -> None:
        gm = GameManager.create_new()
        record = _make_round_record()
        with pytest.raises(ValueError):
            gm.complete_round(record)


class TestIntegrationScenario:
    def test_mixed_rounds(self) -> None:
        """Mixed rounds: dealer win, non-dealer win, draws."""
        gm = GameManager.create_new()

        # East 1: dealer tsumo → stays, honba 1
        gm.complete_round(
            _make_round_record(
                result=_tsumo_result([0], [4000, -1000, -1000, -2000]),
            )
        )
        assert gm.state.round_number == 1
        assert gm.state.honba == 1

        # East 1 (honba 1): dealer tsumo again → stays, honba 2
        gm.complete_round(
            _make_round_record(
                result=_tsumo_result([0], [4000, -1000, -1000, -2000]),
            )
        )
        assert gm.state.round_number == 1
        assert gm.state.honba == 2

        # East 1 (honba 2): non-dealer ron → advance, honba 0
        gm.complete_round(
            _make_round_record(
                result=_ron_result([2], 1, [0, -8000, 8000, 0]),
            )
        )
        assert gm.state.round_number == 2
        assert gm.state.honba == 0

        # East 2: exhaustive draw, dealer(player 1) noten → advance, honba 1
        gm.complete_round(
            _make_round_record(
                result=_exhaustive_draw_result(
                    [False, False, True, False], [-1000, -1000, 3000, -1000]
                ),
            )
        )
        assert gm.state.round_number == 3
        assert gm.state.honba == 1

        # East 3: four winds draw → dealer stays, honba 2
        gm.complete_round(
            _make_round_record(
                result=RoundResult(
                    type=RoundResultTypeEnum.FOUR_WINDS_DRAW,
                    point_diffs=[0, 0, 0, 0],
                ),
            )
        )
        assert gm.state.round_number == 3
        assert gm.state.honba == 2

        # East 3 (honba 2): non-dealer win → advance, honba 0
        gm.complete_round(
            _make_round_record(
                result=_ron_result([3], 0, [-8000, 0, 0, 8000]),
            )
        )
        assert gm.state.round_number == 4
        assert gm.state.honba == 0

        # East 4: non-dealer win → advance to south
        gm.complete_round(
            _make_round_record(
                result=_ron_result([0], 3, [8000, 0, 0, -8000]),
            )
        )
        assert gm.state.round_wind is WindEnum.SOUTH
        assert gm.state.round_number == 1

        # Verify total scores
        total = sum(gm.state.scores)
        assert total == 100000  # zero-sum

        assert len(gm.state.round_records) == 7
