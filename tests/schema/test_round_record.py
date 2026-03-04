from pymahjongutil.enum.common import (
    ActionTypeEnum,
    RoundResultTypeEnum,
    WindEnum,
    YakuEnum,
)
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.round_record import RoundRecord
from pymahjongutil.schema.round_result import RoundResult
from pymahjongutil.schema.tile_index import TileIndex
from pymahjongutil.schema.wall import Wall


def _make_wall() -> Wall:
    return Wall(tiles=[GameTile(tile_index=TileIndex(i % 34)) for i in range(136)])


def _make_initial_hands() -> list[list[GameTile]]:
    return [
        [GameTile(tile_index=TileIndex(j % 34)) for j in range(13)]
        for _ in range(4)
    ]


class TestRoundRecord:
    def test_create_minimal(self) -> None:
        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=_make_wall(),
            initial_hands=_make_initial_hands(),
        )
        assert record.round_wind is WindEnum.EAST
        assert record.round_number == 1
        assert record.honba == 0
        assert record.riichi_sticks == 0
        assert record.dealer == 0
        assert record.actions == []
        assert record.result is None

    def test_create_with_actions_and_result(self) -> None:
        tile = GameTile(tile_index=TileIndex(0))
        actions = [
            RoundAction(type=ActionTypeEnum.DRAW, actor=0, tiles=[tile]),
            RoundAction(type=ActionTypeEnum.DISCARD, actor=0, tiles=[tile]),
        ]
        result = RoundResult(
            type=RoundResultTypeEnum.TSUMO,
            winners=[0],
            han=[1],
            fu=[30],
            yakus=[[YakuEnum.SELF_DRAW]],
            point_diffs=[1500, -500, -500, -500],
        )
        record = RoundRecord(
            round_wind=WindEnum.SOUTH,
            round_number=2,
            honba=1,
            riichi_sticks=1,
            scores=[30000, 20000, 25000, 25000],
            dealer=1,
            wall=_make_wall(),
            initial_hands=_make_initial_hands(),
            actions=actions,
            result=result,
        )
        assert record.round_wind is WindEnum.SOUTH
        assert record.round_number == 2
        assert record.honba == 1
        assert record.riichi_sticks == 1
        assert len(record.actions) == 2
        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.TSUMO
