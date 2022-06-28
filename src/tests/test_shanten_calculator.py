import pytest

from src.hand_parser import get_hand_from_code
from src.schema.count import HandCount
from src.shanten_calculator import calculate_shanten


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 0),
        ("123m456p789s11122z", -1),
        ("135m466p479s1122z", 3),
        ("334m33889p1457s4z", 3),
        ("3558m4p25668s345z", 4),
        ("1199m4p1147s13457z", 3),
        ("1199m1199p1199s12z", 0),
        ("19m149s18p1223456z", 1),
        ("69m5678p2789s344z7p", 2),
    ],
)
def test_calculate_shanten(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert calculate_shanten(hand_count) == expected
