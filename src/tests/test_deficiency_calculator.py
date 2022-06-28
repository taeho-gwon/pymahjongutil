import pytest

from src.deficiency_calculator import calculate_deficiency
from src.hand_parser import get_hand_from_code
from src.schema.count import HandCount


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 1),
        ("123m456p789s11122z", 0),
        ("135m466p479s1122z", 4),
        ("334m33889p1457s4z", 4),
        ("3558m4p25668s345z", 5),
        ("1199m4p1147s13457z", 4),
        ("1199m1199p1199s12z", 1),
        ("19m149s18p1223456z", 2),
        ("69m5678p2789s344z7p", 3),
    ],
)
def test_calculate_deficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    hand_count = HandCount.create_from_hand(hand)
    assert calculate_deficiency(hand_count) == expected
