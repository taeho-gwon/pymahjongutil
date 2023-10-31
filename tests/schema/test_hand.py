import pytest

from pymahjongutil.hand_parser import get_hand_from_code


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
            [18, 19, 20, 12, 13, 14, 8, 8],
        ),
        (
            "123s123456789p99m",
            [18, 19, 20, 9, 10, 11, 12, 13, 14, 15, 16, 17, 8, 8],
        ),
        (
            "123s456p99m,cok111-1z,cok3-333z",
            [18, 19, 20, 12, 13, 14, 8, 8],
        ),
    ],
)
def test_hand_iter_concealed_tiles(test_input, expected):
    hand = get_hand_from_code(test_input)
    for tile, value in zip(hand.iter_concealed_tiles, expected):
        assert tile.value == value


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123s456p99m,chi123s,chi12-3s",
            [18, 19, 20, 12, 13, 14, 8, 18, 19, 20, 18, 19, 20, 8],
        ),
        (
            "123s123456789p99m",
            [18, 19, 20, 9, 10, 11, 12, 13, 14, 15, 16, 17, 8, 8],
        ),
        (
            "123s456p99m,cok111-1z,cok3-333z",
            [18, 19, 20, 12, 13, 14, 8, 27, 27, 27, 27, 29, 29, 29, 29, 8],
        ),
    ],
)
def test_hand_iter_tiles(test_input, expected):
    hand = get_hand_from_code(test_input)
    for tile, value in zip(hand.iter_tiles, expected):
        assert tile.value == value
