import pytest

from src.agari_checker import (
    check_agari_normal,
    check_agari_seven_pair,
    check_agari_thirteen_orphans,
)
from src.hand_parser import get_hand_from_code
from src.schema.count import HandCount


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", False),
        ("123s123456789p99m", False),
        ("123s456p99m,cok111-1z,cok3-333z", False),
        ("1133s4455p99m1177z", True),
    ],
)
def test_check_agari_seven_pair(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert check_agari_seven_pair(hand_count) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", False),
        ("123s456p99m,cok111-1z,cok3-333z", False),
        ("1133s4455p99m1177z", False),
        ("19m19s19p12334567z", True),
    ],
)
def test_check_agari_thirteen_orphans(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert check_agari_thirteen_orphans(hand_count) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", True),
        ("123s456p99m,cok111-1z,cok3-333z", True),
        ("1133s4455p99m1177z", False),
        ("19m19s19p12334567z", False),
    ],
)
def test_check_agari_normal(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert check_agari_normal(hand_count) == expected
