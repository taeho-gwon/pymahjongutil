"""실제 마작 1국 흐름을 재현하는 통합 테스트."""

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


def _gt(index: int, is_red: bool = False) -> GameTile:
    return GameTile(tile_index=TileIndex(index), is_red=is_red)


def _make_standard_wall() -> Wall:
    """표준 136장 배산 생성. 각 패 4장씩, 5m/5p/5s 각 1장은 적패."""
    tiles: list[GameTile] = []
    for copy in range(4):
        for idx in range(34):
            is_red = copy == 0 and idx in (4, 13, 22)
            tiles.append(_gt(idx, is_red=is_red))
    return Wall(tiles=tiles)


def _act(
    type: ActionTypeEnum,
    actor: int,
    tiles: list[GameTile],
    target: int | None = None,
) -> RoundAction:
    return RoundAction(type=type, actor=actor, tiles=tiles, target=target)


class TestRoundTsumo:
    """동1국: 딜러(player 0)가 리치 후 쯔모.

    시나리오:
    - 4순 진행 후 player 0이 리치 선언
    - 리치 후 쯔모 아가리 (리치 + 멘젠쯔모 + 핑후)
    """

    def test_riichi_tsumo_round(self) -> None:
        wall = _make_standard_wall()
        initial_hands = [
            [
                _gt(0),
                _gt(1),
                _gt(2),
                _gt(3),
                _gt(4, True),
                _gt(5),
                _gt(9),
                _gt(10),
                _gt(11),
                _gt(18),
                _gt(19),
                _gt(20),
                _gt(27),
            ],
            [
                _gt(6),
                _gt(7),
                _gt(8),
                _gt(12),
                _gt(13, True),
                _gt(14),
                _gt(15),
                _gt(16),
                _gt(17),
                _gt(21),
                _gt(22, True),
                _gt(23),
                _gt(24),
            ],
            [
                _gt(25),
                _gt(26),
                _gt(28),
                _gt(29),
                _gt(30),
                _gt(31),
                _gt(32),
                _gt(33),
                _gt(0),
                _gt(1),
                _gt(2),
                _gt(3),
                _gt(4),
            ],
            [
                _gt(5),
                _gt(6),
                _gt(7),
                _gt(8),
                _gt(9),
                _gt(10),
                _gt(11),
                _gt(12),
                _gt(13),
                _gt(14),
                _gt(15),
                _gt(16),
                _gt(17),
            ],
        ]

        actions = [
            # 1순: 각 플레이어 드로우 & 타패
            _act(ActionTypeEnum.DRAW, 0, [_gt(27)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(27)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(28)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(28)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(29)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(29)]),
            _act(ActionTypeEnum.DRAW, 3, [_gt(30)]),
            _act(ActionTypeEnum.DISCARD, 3, [_gt(30)]),
            # 2순
            _act(ActionTypeEnum.DRAW, 0, [_gt(31)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(31)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(32)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(32)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(33)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(33)]),
            _act(ActionTypeEnum.DRAW, 3, [_gt(0)]),
            _act(ActionTypeEnum.DISCARD, 3, [_gt(0)]),
            # 3순: player 0 리치 선언
            _act(ActionTypeEnum.DRAW, 0, [_gt(27)]),
            _act(ActionTypeEnum.RIICHI, 0, [_gt(27)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(1)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(1)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(2)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(2)]),
            _act(ActionTypeEnum.DRAW, 3, [_gt(3)]),
            _act(ActionTypeEnum.DISCARD, 3, [_gt(3)]),
            # 4순: player 0 쯔모
            _act(ActionTypeEnum.DRAW, 0, [_gt(27)]),
            _act(ActionTypeEnum.TSUMO, 0, [_gt(27)]),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.TSUMO,
            winners=[0],
            han=[3],
            fu=[30],
            yakus=[[YakuEnum.READY, YakuEnum.SELF_DRAW, YakuEnum.ALL_SEQUENCES]],
            point_diffs=[4000, -1300, -1300, -1400],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.round_wind is WindEnum.EAST
        assert record.dealer == 0
        assert len(record.initial_hands) == 4
        assert all(len(h) == 13 for h in record.initial_hands)
        assert len(record.actions) == 26
        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.TSUMO
        assert record.result.winners == [0]
        assert YakuEnum.READY in record.result.yakus[0]
        assert sum(record.result.point_diffs) == 0

        # 리치 액션 확인
        riichi_actions = [a for a in record.actions if a.type is ActionTypeEnum.RIICHI]
        assert len(riichi_actions) == 1
        assert riichi_actions[0].actor == 0

        # 쯔모 액션 확인
        tsumo_actions = [a for a in record.actions if a.type is ActionTypeEnum.TSUMO]
        assert len(tsumo_actions) == 1
        assert tsumo_actions[0].actor == 0


class TestRoundRon:
    """동2국: player 1이 player 0의 타패에 론.

    시나리오:
    - 간단한 드로우/타패 후 론 아가리
    """

    def test_ron_round(self) -> None:
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(33)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(33)]),
            _act(ActionTypeEnum.RON, 1, [_gt(33)], target=0),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.RON,
            winners=[1],
            loser=0,
            han=[2],
            fu=[40],
            yakus=[[YakuEnum.READY, YakuEnum.ONE_SHOT]],
            point_diffs=[-2600, 2600, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=2,
            honba=0,
            riichi_sticks=0,
            scores=[29000, 23700, 23700, 23600],
            dealer=1,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.RON
        assert record.result.loser == 0
        assert record.result.winners == [1]
        assert sum(record.result.point_diffs) == 0

        # 론 액션이 target을 가지는지 확인
        ron_action = next(a for a in record.actions if a.type is ActionTypeEnum.RON)
        assert ron_action.target == 0
        assert ron_action.actor == 1


class TestRoundWithCalls:
    """치/퐁/깡이 포함된 1국.

    시나리오:
    - player 1이 player 0의 타패에 치
    - player 2가 player 1의 타패에 퐁
    - player 3이 안깡 선언
    - player 0이 가깡(소명깡) 선언
    - 이후 유국
    """

    def test_round_with_various_calls(self) -> None:
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            # player 0 드로우 & 타패 → player 1 치
            _act(ActionTypeEnum.DRAW, 0, [_gt(18)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(18)]),
            _act(ActionTypeEnum.CHII, 1, [_gt(19), _gt(20), _gt(18)], target=0),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(25)]),
            # player 2 퐁
            _act(ActionTypeEnum.PON, 2, [_gt(25), _gt(25), _gt(25)], target=1),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(33)]),
            # player 3 드로우 후 안깡
            _act(ActionTypeEnum.DRAW, 3, [_gt(10)]),
            _act(ActionTypeEnum.CONCEALED_KAN, 3, [_gt(10), _gt(10), _gt(10), _gt(10)]),
            # 영상패 드로우 후 타패
            _act(ActionTypeEnum.DRAW, 3, [_gt(5)]),
            _act(ActionTypeEnum.DISCARD, 3, [_gt(5)]),
            # player 0 드로우, 이미 가진 퐁에 가깡(소명깡)
            _act(ActionTypeEnum.DRAW, 0, [_gt(0)]),
            _act(ActionTypeEnum.SMALL_MELDED_KAN, 0, [_gt(0), _gt(0), _gt(0), _gt(0)]),
            # 영상패 드로우 후 타패
            _act(ActionTypeEnum.DRAW, 0, [_gt(31)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(31)]),
            # 이후 간략히 순회하여 유국
            _act(ActionTypeEnum.DRAW, 1, [_gt(7)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(7)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(8)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(8)]),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.EXHAUSTIVE_DRAW,
            is_tenpai=[True, False, True, False],
            point_diffs=[1500, -1500, 1500, -1500],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.EXHAUSTIVE_DRAW
        assert record.result.is_tenpai == [True, False, True, False]
        assert sum(record.result.point_diffs) == 0

        # 각 부름 타입 존재 확인
        action_types = [a.type for a in record.actions]
        assert ActionTypeEnum.CHII in action_types
        assert ActionTypeEnum.PON in action_types
        assert ActionTypeEnum.CONCEALED_KAN in action_types
        assert ActionTypeEnum.SMALL_MELDED_KAN in action_types

        # 부름 액션에 target 확인
        chii = next(a for a in record.actions if a.type is ActionTypeEnum.CHII)
        assert chii.target == 0
        assert chii.actor == 1
        assert len(chii.tiles) == 3

        pon = next(a for a in record.actions if a.type is ActionTypeEnum.PON)
        assert pon.target == 1
        assert len(pon.tiles) == 3

        kan = next(a for a in record.actions if a.type is ActionTypeEnum.CONCEALED_KAN)
        assert kan.target is None
        assert len(kan.tiles) == 4


class TestRoundDoubleRon:
    """더블론: player 0의 타패에 player 1, 3이 동시 론."""

    def test_double_ron_round(self) -> None:
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(33)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(33)]),
            _act(ActionTypeEnum.RON, 1, [_gt(33)], target=0),
            _act(ActionTypeEnum.RON, 3, [_gt(33)], target=0),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.RON,
            winners=[1, 3],
            loser=0,
            han=[1, 2],
            fu=[30, 40],
            yakus=[[YakuEnum.READY], [YakuEnum.READY, YakuEnum.ONE_SHOT]],
            point_diffs=[-3600, 1000, 0, 2600],
        )

        record = RoundRecord(
            round_wind=WindEnum.SOUTH,
            round_number=3,
            honba=0,
            riichi_sticks=0,
            scores=[30000, 20000, 25000, 25000],
            dealer=2,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert len(record.result.winners) == 2
        assert record.result.loser == 0
        assert len(record.result.han) == 2
        assert len(record.result.fu) == 2
        assert len(record.result.yakus) == 2
        assert sum(record.result.point_diffs) == 0

        ron_actions = [a for a in record.actions if a.type is ActionTypeEnum.RON]
        assert len(ron_actions) == 2
        assert all(a.target == 0 for a in ron_actions)


class TestRoundSpecialDraws:
    """특수 유국 케이스들."""

    def test_four_winds_draw(self) -> None:
        """사풍연타 유국: 첫 순 4명 모두 같은 풍패 타패."""
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(27)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(27)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(27)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(27)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(27)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(27)]),
            _act(ActionTypeEnum.DRAW, 3, [_gt(27)]),
            _act(ActionTypeEnum.DISCARD, 3, [_gt(27)]),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.FOUR_WINDS_DRAW,
            point_diffs=[0, 0, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.FOUR_WINDS_DRAW
        assert record.result.winners == []
        assert sum(record.result.point_diffs) == 0

    def test_nine_tiles_draw(self) -> None:
        """구종구패 유국: 딜러 배패에 구종구패, 첫 드로우 후 선언."""
        wall = _make_standard_wall()
        # 딜러 배패: 1m 9m 1p 9p 1s 9s 東 南 西 北 白 發 中 (13장 요로하이)
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

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(5)]),
            _act(ActionTypeEnum.NINE_TILES_DRAW, 0, []),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.NINE_TILES_DRAW,
            point_diffs=[0, 0, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.NINE_TILES_DRAW
        assert len(record.actions) == 2
        assert record.actions[1].type is ActionTypeEnum.NINE_TILES_DRAW

    def test_four_kans_draw(self) -> None:
        """사깡산료: 서로 다른 플레이어가 4번 깡하여 유국."""
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(0)]),
            _act(ActionTypeEnum.CONCEALED_KAN, 0, [_gt(0), _gt(0), _gt(0), _gt(0)]),
            _act(ActionTypeEnum.DRAW, 0, [_gt(5)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(5)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(13)]),
            _act(ActionTypeEnum.CONCEALED_KAN, 1, [_gt(13), _gt(13), _gt(13), _gt(13)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(6)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(6)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(25)]),
            _act(ActionTypeEnum.CONCEALED_KAN, 2, [_gt(25), _gt(25), _gt(25), _gt(25)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(7)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(7)]),
            _act(ActionTypeEnum.DRAW, 3, [_gt(10)]),
            _act(ActionTypeEnum.CONCEALED_KAN, 3, [_gt(10), _gt(10), _gt(10), _gt(10)]),
            # 4번째 깡 후 유국
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.FOUR_KANS_DRAW,
            point_diffs=[0, 0, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.FOUR_KANS_DRAW
        kan_actions = [
            a for a in record.actions if a.type is ActionTypeEnum.CONCEALED_KAN
        ]
        assert len(kan_actions) == 4

    def test_four_riichi_draw(self) -> None:
        """사가리치 유국: 4명 모두 리치 선언."""
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(27)]),
            _act(ActionTypeEnum.RIICHI, 0, [_gt(27)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(28)]),
            _act(ActionTypeEnum.RIICHI, 1, [_gt(28)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(29)]),
            _act(ActionTypeEnum.RIICHI, 2, [_gt(29)]),
            _act(ActionTypeEnum.DRAW, 3, [_gt(30)]),
            _act(ActionTypeEnum.RIICHI, 3, [_gt(30)]),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.FOUR_RIICHI_DRAW,
            point_diffs=[0, 0, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.FOUR_RIICHI_DRAW
        riichi_actions = [a for a in record.actions if a.type is ActionTypeEnum.RIICHI]
        assert len(riichi_actions) == 4
        assert [a.actor for a in riichi_actions] == [0, 1, 2, 3]

    def test_three_ron_draw(self) -> None:
        """삼가화 유국: 3명 동시 론으로 유국 처리."""
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(33)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(33)]),
            _act(ActionTypeEnum.RON, 1, [_gt(33)], target=0),
            _act(ActionTypeEnum.RON, 2, [_gt(33)], target=0),
            _act(ActionTypeEnum.RON, 3, [_gt(33)], target=0),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.THREE_RON_DRAW,
            point_diffs=[0, 0, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.THREE_RON_DRAW
        ron_actions = [a for a in record.actions if a.type is ActionTypeEnum.RON]
        assert len(ron_actions) == 3


class TestRoundWithRedTiles:
    """적패(is_red)가 포함된 시나리오."""

    def test_red_tiles_in_hand_and_actions(self) -> None:
        wall = _make_standard_wall()

        # 적5만, 적5통을 가진 배패
        initial_hands = [
            [
                _gt(0),
                _gt(1),
                _gt(2),
                _gt(3),
                _gt(4, True),
                _gt(5),
                _gt(6),
                _gt(7),
                _gt(8),
                _gt(9),
                _gt(10),
                _gt(11),
                _gt(12),
            ],
            [
                _gt(13, True),
                _gt(14),
                _gt(15),
                _gt(16),
                _gt(17),
                _gt(18),
                _gt(19),
                _gt(20),
                _gt(21),
                _gt(22, True),
                _gt(23),
                _gt(24),
                _gt(25),
            ],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(22, True)]),  # 적5소 드로우
            _act(ActionTypeEnum.DISCARD, 0, [_gt(12)]),
            _act(ActionTypeEnum.DRAW, 1, [_gt(26)]),
            _act(ActionTypeEnum.TSUMO, 1, [_gt(26)]),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.TSUMO,
            winners=[1],
            han=[4],
            fu=[30],
            yakus=[[YakuEnum.READY, YakuEnum.SELF_DRAW, YakuEnum.ALL_SEQUENCES]],
            point_diffs=[-2600, 5200, -1300, -1300],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        # 적패 확인
        red_in_hand_0 = [t for t in record.initial_hands[0] if t.is_red]
        assert len(red_in_hand_0) == 1
        assert red_in_hand_0[0].tile_index == TileIndex(4)  # 적5만

        red_in_hand_1 = [t for t in record.initial_hands[1] if t.is_red]
        assert len(red_in_hand_1) == 2  # 적5통, 적5소

        # 드로우한 적패 확인
        draw_action = record.actions[0]
        assert draw_action.tiles[0].is_red is True
        assert draw_action.tiles[0].tile_index == TileIndex(22)  # 적5소


class TestRoundWithBigMeldedKan:
    """대명깡(BIG_MELDED_KAN)이 포함된 시나리오."""

    def test_big_melded_kan_round(self) -> None:
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(27)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(27)]),
            # player 1이 player 0의 타패를 대명깡
            _act(
                ActionTypeEnum.BIG_MELDED_KAN,
                1,
                [_gt(27), _gt(27), _gt(27), _gt(27)],
                target=0,
            ),
            # 영상패 드로우 후 타패
            _act(ActionTypeEnum.DRAW, 1, [_gt(5)]),
            _act(ActionTypeEnum.DISCARD, 1, [_gt(5)]),
            _act(ActionTypeEnum.DRAW, 2, [_gt(6)]),
            _act(ActionTypeEnum.DISCARD, 2, [_gt(6)]),
        ]

        result = RoundResult(
            type=RoundResultTypeEnum.EXHAUSTIVE_DRAW,
            is_tenpai=[False, False, False, False],
            point_diffs=[0, 0, 0, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=[25000, 25000, 25000, 25000],
            dealer=0,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        big_kan = next(
            a for a in record.actions if a.type is ActionTypeEnum.BIG_MELDED_KAN
        )
        assert big_kan.actor == 1
        assert big_kan.target == 0
        assert len(big_kan.tiles) == 4


class TestRoundHonbaAndRiichiSticks:
    """본장/리치봉이 있는 상태에서의 1국."""

    def test_honba_and_riichi_sticks(self) -> None:
        """남3국 2본장, 리치봉 2개 상태에서 론 아가리."""
        wall = _make_standard_wall()
        initial_hands = [
            [_gt(i) for i in range(13)],
            [_gt(i) for i in range(13, 26)],
            [_gt(i) for i in range(21, 34)],
            [_gt(i) for i in range(8, 21)],
        ]

        actions = [
            _act(ActionTypeEnum.DRAW, 0, [_gt(33)]),
            _act(ActionTypeEnum.DISCARD, 0, [_gt(33)]),
            _act(ActionTypeEnum.RON, 2, [_gt(33)], target=0),
        ]

        # 2본장(+600) + 리치봉 2개(+2000)가 승자에게
        result = RoundResult(
            type=RoundResultTypeEnum.RON,
            winners=[2],
            loser=0,
            han=[1],
            fu=[30],
            yakus=[[YakuEnum.WHITE_DRAGON]],
            point_diffs=[-3600, 0, 3600, 0],
        )

        record = RoundRecord(
            round_wind=WindEnum.SOUTH,
            round_number=3,
            honba=2,
            riichi_sticks=2,
            scores=[30000, 25000, 20000, 25000],
            dealer=2,
            wall=wall,
            initial_hands=initial_hands,
            actions=actions,
            result=result,
        )

        assert record.round_wind is WindEnum.SOUTH
        assert record.round_number == 3
        assert record.honba == 2
        assert record.riichi_sticks == 2
        assert record.dealer == 2
        assert record.result is not None
        assert record.result.type is RoundResultTypeEnum.RON
