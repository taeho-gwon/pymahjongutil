import pytest

from pymahjong.hand_checker.thirteen_orphan_checker import ThirteenOrphanChecker
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.count import HandCount

thirteen_orphan_checker = ThirteenOrphanChecker()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123s456p99m,chi123s,chi12-3s", False),
        ("123s456p99m,cok111-1z,cok3-333z", False),
        ("1133s4455p99m1177z", False),
        ("19m19s19p12334567z", True),
    ],
)
def test_check_thirteen_orphans_agari(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert thirteen_orphan_checker.check_agari(hand_count) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 9),
        ("123m456p789s11122z", 9),
        ("135m466p479s1122z", 9),
        ("334m33889p1457s4z", 11),
        ("3558m4p25668s345z", 11),
        ("1199m4p1147s13457z", 5),
        ("1199m1199p1199s12z", 5),
        ("19m149s18p1223456z", 2),
        ("69m5678p2789s344z7p", 9),
    ],
)
def test_calculate_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert thirteen_orphan_checker.calculate_deficiency(hand_count) == expected
