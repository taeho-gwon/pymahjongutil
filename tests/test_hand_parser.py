import pytest

from pymahjong.enum.common import CallTypeEnum, TileTypeEnum
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.call import Call
from pymahjong.schema.hand import Hand
from pymahjong.schema.tile import Tile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123p45699s,chi123s,pon5-55z",
            Hand(
                concealed_tiles=[
                    Tile(type=TileTypeEnum.PIN, value=1),
                    Tile(type=TileTypeEnum.PIN, value=2),
                    Tile(type=TileTypeEnum.PIN, value=3),
                    Tile(type=TileTypeEnum.SOU, value=4),
                    Tile(type=TileTypeEnum.SOU, value=5),
                    Tile(type=TileTypeEnum.SOU, value=6),
                    Tile(type=TileTypeEnum.SOU, value=9),
                ],
                calls=[
                    Call(
                        type=CallTypeEnum.CHII,
                        tiles=[
                            Tile(type=TileTypeEnum.SOU, value=1),
                            Tile(type=TileTypeEnum.SOU, value=2),
                            Tile(type=TileTypeEnum.SOU, value=3),
                        ],
                        call_idx=0,
                    ),
                    Call(
                        type=CallTypeEnum.PON,
                        tiles=[
                            Tile(type=TileTypeEnum.DRAGON, value=1),
                            Tile(type=TileTypeEnum.DRAGON, value=1),
                            Tile(type=TileTypeEnum.DRAGON, value=1),
                        ],
                        call_idx=1,
                    ),
                ],
                last_tile=Tile(type=TileTypeEnum.SOU, value=9),
            ),
        ),
        (
            "19m19p19s1234567z",
            Hand(
                concealed_tiles=[
                    Tile(type=TileTypeEnum.MAN, value=1),
                    Tile(type=TileTypeEnum.MAN, value=9),
                    Tile(type=TileTypeEnum.PIN, value=1),
                    Tile(type=TileTypeEnum.PIN, value=9),
                    Tile(type=TileTypeEnum.SOU, value=1),
                    Tile(type=TileTypeEnum.SOU, value=9),
                    Tile(type=TileTypeEnum.WIND, value=1),
                    Tile(type=TileTypeEnum.WIND, value=2),
                    Tile(type=TileTypeEnum.WIND, value=3),
                    Tile(type=TileTypeEnum.WIND, value=4),
                    Tile(type=TileTypeEnum.DRAGON, value=1),
                    Tile(type=TileTypeEnum.DRAGON, value=2),
                    Tile(type=TileTypeEnum.DRAGON, value=3),
                ],
                calls=[],
            ),
        ),
    ],
)
def test_get_hand_from_code(test_input, expected):
    assert get_hand_from_code(test_input) == expected
