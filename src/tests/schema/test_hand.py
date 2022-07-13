import pytest

from src.enum.common import TileTypeEnum
from src.hand_parser import get_hand_from_code
from src.schema.tile import Tile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", True),
        ("123s123456789p99m", False),
        ("123s456p99m,cok111-1z,cok3-333z", False),
    ],
)
def test_hand_is_opened(test_input, expected):
    hand = get_hand_from_code(test_input)
    assert hand.is_opened == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123s456p99m,chi123s,chi12-3s",
            [
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.PIN, value=4),
                Tile(type=TileTypeEnum.PIN, value=5),
                Tile(type=TileTypeEnum.PIN, value=6),
                Tile(type=TileTypeEnum.MAN, value=9),
                Tile(type=TileTypeEnum.MAN, value=9),
            ],
        ),
        (
            "123s123456789p99m",
            [
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.PIN, value=1),
                Tile(type=TileTypeEnum.PIN, value=2),
                Tile(type=TileTypeEnum.PIN, value=3),
                Tile(type=TileTypeEnum.PIN, value=4),
                Tile(type=TileTypeEnum.PIN, value=5),
                Tile(type=TileTypeEnum.PIN, value=6),
                Tile(type=TileTypeEnum.PIN, value=7),
                Tile(type=TileTypeEnum.PIN, value=8),
                Tile(type=TileTypeEnum.PIN, value=9),
                Tile(type=TileTypeEnum.MAN, value=9),
                Tile(type=TileTypeEnum.MAN, value=9),
            ],
        ),
        (
            "123s456p99m,cok111-1z,cok3-333z",
            [
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.PIN, value=4),
                Tile(type=TileTypeEnum.PIN, value=5),
                Tile(type=TileTypeEnum.PIN, value=6),
                Tile(type=TileTypeEnum.MAN, value=9),
                Tile(type=TileTypeEnum.MAN, value=9),
            ],
        ),
    ],
)
def test_hand_iter_concealed_tiles(test_input, expected):
    hand = get_hand_from_code(test_input)
    assert list(hand.iter_concealed_tiles) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123s456p99m,chi123s,chi12-3s",
            [
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.PIN, value=4),
                Tile(type=TileTypeEnum.PIN, value=5),
                Tile(type=TileTypeEnum.PIN, value=6),
                Tile(type=TileTypeEnum.MAN, value=9),
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.MAN, value=9),
            ],
        ),
        (
            "123s123456789p99m",
            [
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.PIN, value=1),
                Tile(type=TileTypeEnum.PIN, value=2),
                Tile(type=TileTypeEnum.PIN, value=3),
                Tile(type=TileTypeEnum.PIN, value=4),
                Tile(type=TileTypeEnum.PIN, value=5),
                Tile(type=TileTypeEnum.PIN, value=6),
                Tile(type=TileTypeEnum.PIN, value=7),
                Tile(type=TileTypeEnum.PIN, value=8),
                Tile(type=TileTypeEnum.PIN, value=9),
                Tile(type=TileTypeEnum.MAN, value=9),
                Tile(type=TileTypeEnum.MAN, value=9),
            ],
        ),
        (
            "123s456p99m,cok111-1z,cok3-333z",
            [
                Tile(type=TileTypeEnum.SOU, value=1),
                Tile(type=TileTypeEnum.SOU, value=2),
                Tile(type=TileTypeEnum.SOU, value=3),
                Tile(type=TileTypeEnum.PIN, value=4),
                Tile(type=TileTypeEnum.PIN, value=5),
                Tile(type=TileTypeEnum.PIN, value=6),
                Tile(type=TileTypeEnum.MAN, value=9),
                Tile(type=TileTypeEnum.WIND, value=1),
                Tile(type=TileTypeEnum.WIND, value=1),
                Tile(type=TileTypeEnum.WIND, value=1),
                Tile(type=TileTypeEnum.WIND, value=1),
                Tile(type=TileTypeEnum.WIND, value=3),
                Tile(type=TileTypeEnum.WIND, value=3),
                Tile(type=TileTypeEnum.WIND, value=3),
                Tile(type=TileTypeEnum.WIND, value=3),
                Tile(type=TileTypeEnum.MAN, value=9),
            ],
        ),
    ],
)
def test_hand_iter_tiles(test_input, expected):
    hand = get_hand_from_code(test_input)
    assert list(hand.iter_tiles) == expected
