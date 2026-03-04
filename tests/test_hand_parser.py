import pytest

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.hand_parser import (
    get_call_from_code,
    get_hand_from_code,
    get_tile_from_code,
    get_tiles_from_code,
)
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.tile import Tile


class TestGetTileFromCode:
    @pytest.mark.parametrize(
        "code, expected_value",
        [
            ("1m", 0),
            ("5m", 4),
            ("9m", 8),
            ("1p", 9),
            ("9p", 17),
            ("1s", 18),
            ("9s", 26),
            ("1z", 27),
            ("7z", 33),
        ],
    )
    def test_valid_codes(self, code: str, expected_value: int) -> None:
        assert get_tile_from_code(code) == Tile(value=expected_value)

    @pytest.mark.parametrize(
        "code",
        [
            "1x",
            "3a",
            "5q",
        ],
    )
    def test_invalid_tile_type(self, code: str) -> None:
        with pytest.raises(ValueError, match="is not a valid tile type code"):
            get_tile_from_code(code)

    @pytest.mark.parametrize(
        "code",
        [
            "8z",
            "9z",
        ],
    )
    def test_out_of_range_honor(self, code: str) -> None:
        with pytest.raises(ValueError, match="is not a valid tile code"):
            get_tile_from_code(code)

    def test_zero_number(self) -> None:
        with pytest.raises(ValueError, match="is not a valid tile code"):
            get_tile_from_code("0m")


class TestGetTilesFromCode:
    @pytest.mark.parametrize(
        "code, expected_values",
        [
            ("123m", [0, 1, 2]),
            ("19p", [9, 17]),
            ("1z7z", [27, 33]),
            ("123m456p", [0, 1, 2, 12, 13, 14]),
        ],
    )
    def test_valid_codes(self, code: str, expected_values: list[int]) -> None:
        expected = [Tile(value=v) for v in expected_values]
        assert get_tiles_from_code(code) == expected

    @pytest.mark.parametrize(
        "code",
        [
            "abc",
            "12x",
            "m123",
        ],
    )
    def test_invalid_codes(self, code: str) -> None:
        with pytest.raises(ValueError, match="is not a valid tile_code"):
            get_tiles_from_code(code)


class TestGetCallFromCode:
    def test_chii(self) -> None:
        call = get_call_from_code("chi123s")
        assert call == Call(
            type=CallTypeEnum.CHII,
            tiles=[Tile(value=18), Tile(value=19), Tile(value=20)],
            call_idx=0,
        )

    def test_pon_with_call_idx(self) -> None:
        call = get_call_from_code("pon5-55z")
        assert call == Call(
            type=CallTypeEnum.PON,
            tiles=[Tile(value=31), Tile(value=31), Tile(value=31)],
            call_idx=1,
        )

    def test_concealed_kan(self) -> None:
        call = get_call_from_code("cok111-1z")
        assert call == Call(
            type=CallTypeEnum.CONCEALED_KAN,
            tiles=[
                Tile(value=27),
                Tile(value=27),
                Tile(value=27),
                Tile(value=27),
            ],
            call_idx=3,
        )

    def test_big_melded_kan(self) -> None:
        call = get_call_from_code("bmk2-222s")
        assert call == Call(
            type=CallTypeEnum.BIG_MELDED_KAN,
            tiles=[
                Tile(value=19),
                Tile(value=19),
                Tile(value=19),
                Tile(value=19),
            ],
            call_idx=1,
        )

    def test_small_melded_kan(self) -> None:
        call = get_call_from_code("smk33-33p")
        assert call == Call(
            type=CallTypeEnum.SMALL_MELDED_KAN,
            tiles=[
                Tile(value=11),
                Tile(value=11),
                Tile(value=11),
                Tile(value=11),
            ],
            call_idx=2,
        )

    def test_invalid_call_type(self) -> None:
        with pytest.raises(ValueError, match="is not a valid call type code"):
            get_call_from_code("xyz123m")


class TestGetHandFromCode:
    def test_hand_with_calls_and_last_tile(self) -> None:
        hand = get_hand_from_code("123p45699s,chi123s,pon5-55z")
        assert hand == Hand(
            concealed_tiles=[
                Tile(value=9),
                Tile(value=10),
                Tile(value=11),
                Tile(value=21),
                Tile(value=22),
                Tile(value=23),
                Tile(value=26),
            ],
            calls=[
                Call(
                    type=CallTypeEnum.CHII,
                    tiles=[Tile(value=18), Tile(value=19), Tile(value=20)],
                    call_idx=0,
                ),
                Call(
                    type=CallTypeEnum.PON,
                    tiles=[Tile(value=31), Tile(value=31), Tile(value=31)],
                    call_idx=1,
                ),
            ],
            last_tile=Tile(value=26),
        )

    def test_hand_without_calls(self) -> None:
        hand = get_hand_from_code("19m19p19s1234567z")
        assert hand == Hand(
            concealed_tiles=[
                Tile(value=0),
                Tile(value=8),
                Tile(value=9),
                Tile(value=17),
                Tile(value=18),
                Tile(value=26),
                Tile(value=27),
                Tile(value=28),
                Tile(value=29),
                Tile(value=30),
                Tile(value=31),
                Tile(value=32),
                Tile(value=33),
            ],
            calls=[],
        )
        assert hand.last_tile is None

    def test_hand_with_last_tile_no_calls(self) -> None:
        hand = get_hand_from_code("123456789m11122p")
        assert hand.last_tile is not None
        assert hand.last_tile == Tile(value=10)
        assert len(hand.concealed_tiles) == 13

    def test_hand_with_concealed_kan(self) -> None:
        # 12345m11p = 7 tiles, with kan that's 4+7=11, not 14
        # Need 8 concealed tiles (8 % 3 == 2) so last_tile is split off
        hand = get_hand_from_code("12345m111p,cok1-111z")
        assert hand == Hand(
            concealed_tiles=[
                Tile(value=0),
                Tile(value=1),
                Tile(value=2),
                Tile(value=3),
                Tile(value=4),
                Tile(value=9),
                Tile(value=9),
            ],
            calls=[
                Call(
                    type=CallTypeEnum.CONCEALED_KAN,
                    tiles=[
                        Tile(value=27),
                        Tile(value=27),
                        Tile(value=27),
                        Tile(value=27),
                    ],
                    call_idx=1,
                ),
            ],
            last_tile=Tile(value=9),
        )
