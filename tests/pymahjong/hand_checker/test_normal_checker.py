import pytest

from pymahjong.hand_checker.normal_checker import NormalChecker
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.count import HandCount

normal_checker = NormalChecker()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", True),
        ("123s456p99m,cok111-1z,cok3-333z", True),
        ("1133s4455p99m1177z", False),
        ("19m19s19p12334567z", False),
    ],
)
def test_check_agari(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert normal_checker.check_agari(hand_count) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 1),
        ("123m456p789s1111z", 2),
        # ("123m4569999p789s", 2),  mahjong module fix test
        ("123m456p789s11122z", 0),
        ("135m466p479s1122z", 4),
        ("334m33889p1457s4z", 5),
        ("3558m4p25668s345z", 6),
        ("1199m4p1147s13457z", 6),
        ("1199m1199p1199s12z", 4),
        ("19m149s18p1223456z", 8),
        ("69m5678p2789s344z7p", 3),
        ("9m5678p12789s344z7p", 2),
    ],
)
def test_calculate_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert normal_checker.calculate_deficiency(hand_count) == expected
