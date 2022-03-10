import pytest

from src.enum.common import CallType, TileType
from src.hand_parser.hand_parser import get_hand_from_code
from src.schema.call import Call
from src.schema.hand import Hand
from src.schema.tile import Tile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123p45699s,chi123s,pon5-55z",
            Hand(
                concealed_tiles=[
                    Tile(type=TileType.PIN, value=1),
                    Tile(type=TileType.PIN, value=2),
                    Tile(type=TileType.PIN, value=3),
                    Tile(type=TileType.SOU, value=4),
                    Tile(type=TileType.SOU, value=5),
                    Tile(type=TileType.SOU, value=6),
                    Tile(type=TileType.SOU, value=9),
                ],
                calls=[
                    Call(
                        type=CallType.CHII,
                        tiles=[
                            Tile(type=TileType.SOU, value=1),
                            Tile(type=TileType.SOU, value=2),
                            Tile(type=TileType.SOU, value=3),
                        ],
                        call_idx=0,
                    ),
                    Call(
                        type=CallType.PON,
                        tiles=[
                            Tile(type=TileType.DRAGON, value=1),
                            Tile(type=TileType.DRAGON, value=1),
                            Tile(type=TileType.DRAGON, value=1),
                        ],
                        call_idx=1,
                    ),
                ],
                draw_tile=Tile(type=TileType.SOU, value=9),
            ),
        ),
        (
            "19m19p19s1234567z",
            Hand(
                concealed_tiles=[
                    Tile(type=TileType.MAN, value=1),
                    Tile(type=TileType.MAN, value=9),
                    Tile(type=TileType.PIN, value=1),
                    Tile(type=TileType.PIN, value=9),
                    Tile(type=TileType.SOU, value=1),
                    Tile(type=TileType.SOU, value=9),
                    Tile(type=TileType.WIND, value=1),
                    Tile(type=TileType.WIND, value=2),
                    Tile(type=TileType.WIND, value=3),
                    Tile(type=TileType.WIND, value=4),
                    Tile(type=TileType.DRAGON, value=1),
                    Tile(type=TileType.DRAGON, value=2),
                    Tile(type=TileType.DRAGON, value=3),
                ],
                calls=[],
            ),
        ),
    ],
)
def test_get_hand_from_code(test_input, expected):
    assert get_hand_from_code(test_input) == expected
