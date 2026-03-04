import pytest

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.tile import Tile


class TestCall:
    def test_chii_call(self) -> None:
        call = Call(
            type=CallTypeEnum.CHII,
            tiles=[Tile(0), Tile(1), Tile(2)],
            call_idx=0,
        )
        assert call.type is CallTypeEnum.CHII
        assert len(call.tiles) == 3
        assert call.call_idx == 0

    def test_pon_call(self) -> None:
        call = Call(
            type=CallTypeEnum.PON,
            tiles=[Tile(0), Tile(0), Tile(0)],
            call_idx=1,
        )
        assert call.type is CallTypeEnum.PON
        assert len(call.tiles) == 3
        assert call.call_idx == 1

    def test_concealed_kan_call(self) -> None:
        call = Call(
            type=CallTypeEnum.CONCEALED_KAN,
            tiles=[Tile(0), Tile(0), Tile(0), Tile(0)],
            call_idx=2,
        )
        assert call.type is CallTypeEnum.CONCEALED_KAN
        assert len(call.tiles) == 4
        assert call.call_idx == 2

    def test_big_melded_kan_call(self) -> None:
        call = Call(
            type=CallTypeEnum.BIG_MELDED_KAN,
            tiles=[Tile(9), Tile(9), Tile(9), Tile(9)],
            call_idx=0,
        )
        assert call.type is CallTypeEnum.BIG_MELDED_KAN
        assert len(call.tiles) == 4

    def test_small_melded_kan_call(self) -> None:
        call = Call(
            type=CallTypeEnum.SMALL_MELDED_KAN,
            tiles=[Tile(18), Tile(18), Tile(18), Tile(18)],
            call_idx=0,
        )
        assert call.type is CallTypeEnum.SMALL_MELDED_KAN
        assert len(call.tiles) == 4
