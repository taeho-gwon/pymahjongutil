import pytest

from pymahjong.deficiency_calculator import (
    calculate_normal_deficiency,
    calculate_seven_pairs_deficiency,
    calculate_thirteen_orphans_deficiency,
)
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.count import HandCount


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 1),
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
def test_calculate_normal_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert calculate_normal_deficiency(hand_count) == expected


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
def test_calculate_seven_pairs_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert calculate_seven_pairs_deficiency(hand_count) == expected


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
def test_calculate_thirteen_orphans_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert calculate_thirteen_orphans_deficiency(hand_count) == expected
