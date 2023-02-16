import pytest

from pymahjong.hand_checker.seven_pair_checker import SevenPairChecker
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.count import HandCount

seven_pair_checker = SevenPairChecker()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", False),
        ("123s123456789p99m", False),
        ("123s456p99m,cok111-1z,cok3-333z", False),
        ("1133s4455p99m1177z", True),
    ],
)
def test_check_agari(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert seven_pair_checker.check_agari(hand_count) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 6),
        ("123m456p789s11122z", 5),
        ("135m466p479s1122z", 4),
        ("334m33889p1457s4z", 4),
        ("3558m4p25668s345z", 5),
        ("1199m4p1147s13457z", 4),
        ("1199m1199p1199s12z", 1),
        ("19m149s18p1223456z", 6),
        ("69m5678p2789s344z7p", 5),
    ],
)
def test_calculate_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert seven_pair_checker.calculate_deficiency(hand_count) == expected
