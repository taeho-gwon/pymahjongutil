import pytest

from src.hand_parser.hand_parser import get_hand_from_code


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", True),
        ("123s123456789p99m", False),
        ("123s456p99m,cok111-1z,cok3-333z", False)
    ]
)
def test_hand_is_opened(test_input, expected):
    hand = get_hand_from_code(test_input)
    assert hand.is_opened == expected
