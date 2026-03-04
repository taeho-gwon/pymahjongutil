import pytest

from pymahjongutil.enum.common import (
    AgariTypeFuReasonEnum,
    BodyFuReasonEnum,
    HandShapeFuReasonEnum,
    WaitFuReasonEnum,
    YakuEnum,
)
from pymahjongutil.schema.point_info import PointInfo


class TestPointInfo:
    def test_basic_creation(self) -> None:
        info = PointInfo(
            point_diff=[0, -8000, 0, 0],
            han=3,
            fu=40,
            yakus=[YakuEnum.READY, YakuEnum.SELF_DRAW],
            fu_reasons=[HandShapeFuReasonEnum.BASE, AgariTypeFuReasonEnum.TSUMO],
        )
        assert info.han == 3
        assert info.fu == 40
        assert info.point_diff == [0, -8000, 0, 0]
        assert YakuEnum.READY in info.yakus
        assert YakuEnum.SELF_DRAW in info.yakus
        assert len(info.fu_reasons) == 2

    def test_creation_with_empty_lists(self) -> None:
        info = PointInfo(
            point_diff=[0, 0, 0, 0],
            han=0,
            fu=0,
            yakus=[],
            fu_reasons=[],
        )
        assert info.han == 0
        assert info.fu == 0
        assert info.yakus == []
        assert info.fu_reasons == []

    def test_creation_with_multiple_yakus(self) -> None:
        info = PointInfo(
            point_diff=[-4000, 12000, -4000, -4000],
            han=6,
            fu=30,
            yakus=[
                YakuEnum.READY,
                YakuEnum.ONE_SHOT,
                YakuEnum.SELF_DRAW,
                YakuEnum.ALL_SIMPLES,
                YakuEnum.IDENTICAL_SEQUENCES,
            ],
            fu_reasons=[HandShapeFuReasonEnum.BASE],
        )
        assert info.han == 6
        assert len(info.yakus) == 5

    def test_creation_with_body_fu_reasons(self) -> None:
        info = PointInfo(
            point_diff=[0, -2000, 0, 0],
            han=1,
            fu=40,
            yakus=[YakuEnum.READY],
            fu_reasons=[
                HandShapeFuReasonEnum.BASE,
                AgariTypeFuReasonEnum.CONCEALED_RON,
                BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE,
            ],
        )
        assert len(info.fu_reasons) == 3
        assert BodyFuReasonEnum.CONCEALED_NORMAL_TRIPLE in info.fu_reasons

    def test_creation_with_wait_fu_reason(self) -> None:
        info = PointInfo(
            point_diff=[0, -1300, 0, 0],
            han=1,
            fu=40,
            yakus=[YakuEnum.READY],
            fu_reasons=[
                HandShapeFuReasonEnum.BASE,
                WaitFuReasonEnum.EDGE_WAIT,
            ],
        )
        assert WaitFuReasonEnum.EDGE_WAIT in info.fu_reasons
