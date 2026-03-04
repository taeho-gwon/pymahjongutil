from pymahjongutil.enum.common import RoundResultTypeEnum, YakuEnum
from pymahjongutil.schema.round_result import RoundResult


class TestRoundResult:
    def test_tsumo_result(self) -> None:
        result = RoundResult(
            type=RoundResultTypeEnum.TSUMO,
            winners=[0],
            han=[3],
            fu=[30],
            yakus=[[YakuEnum.READY, YakuEnum.SELF_DRAW, YakuEnum.ALL_SIMPLES]],
            point_diffs=[4000, -1300, -1300, -1400],
        )
        assert result.type is RoundResultTypeEnum.TSUMO
        assert result.winners == [0]
        assert result.loser is None
        assert result.han == [3]

    def test_ron_result(self) -> None:
        result = RoundResult(
            type=RoundResultTypeEnum.RON,
            winners=[1],
            loser=0,
            han=[2],
            fu=[40],
            yakus=[[YakuEnum.READY, YakuEnum.ONE_SHOT]],
            point_diffs=[-2600, 2600, 0, 0],
        )
        assert result.type is RoundResultTypeEnum.RON
        assert result.loser == 0

    def test_exhaustive_draw(self) -> None:
        result = RoundResult(
            type=RoundResultTypeEnum.EXHAUSTIVE_DRAW,
            is_tenpai=[True, False, False, True],
            point_diffs=[1500, -1000, -1000, 1500],
        )
        assert result.type is RoundResultTypeEnum.EXHAUSTIVE_DRAW
        assert result.is_tenpai == [True, False, False, True]

    def test_special_draw(self) -> None:
        result = RoundResult(type=RoundResultTypeEnum.FOUR_WINDS_DRAW)
        assert result.type is RoundResultTypeEnum.FOUR_WINDS_DRAW
        assert result.winners == []

    def test_double_ron(self) -> None:
        result = RoundResult(
            type=RoundResultTypeEnum.RON,
            winners=[1, 3],
            loser=0,
            han=[1, 2],
            fu=[30, 40],
            yakus=[[YakuEnum.READY], [YakuEnum.READY, YakuEnum.ONE_SHOT]],
            point_diffs=[-3600, 1000, 0, 2600],
        )
        assert len(result.winners) == 2
