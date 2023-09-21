import pytest

from pymahjong.hand_checker.seven_pair_checker import SevenPairChecker
from pymahjong.hand_parser import get_hand_from_code, get_tile_from_code
from pymahjong.schema.efficiency_data import EfficiencyData


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
    assert SevenPairChecker(hand).check_agari() == expected


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
    assert SevenPairChecker(hand).calculate_deficiency() == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "1188m557889p4466s",
            [
                ("7p", ["9p"], 3),
                ("9p", ["7p"], 3),
            ],
        ),
        (
            "11789m6789p45566s",
            [
                ("7m", ["8m", "9m", "6p", "7p", "8p", "9p", "4s"], 21),
                ("8m", ["7m", "9m", "6p", "7p", "8p", "9p", "4s"], 21),
                ("9m", ["7m", "8m", "6p", "7p", "8p", "9p", "4s"], 21),
                ("6p", ["7m", "8m", "9m", "7p", "8p", "9p", "4s"], 21),
                ("7p", ["7m", "8m", "9m", "6p", "8p", "9p", "4s"], 21),
                ("8p", ["7m", "8m", "9m", "6p", "7p", "9p", "4s"], 21),
                ("9p", ["7m", "8m", "9m", "6p", "7p", "8p", "4s"], 21),
                ("4s", ["7m", "8m", "9m", "6p", "7p", "8p", "9p"], 21),
            ],
        ),
    ],
)
def test_calculate_efficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    expected_efficiency = [
        EfficiencyData(
            discard_tile=get_tile_from_code(discard_tile_code).value,
            ukeire=[get_tile_from_code(ukeire).value for ukeire in ukeire_codes],
            num_ukeire=num_ukeire,
        )
        for discard_tile_code, ukeire_codes, num_ukeire in expected
    ]

    assert SevenPairChecker(hand).calculate_efficiency() == expected_efficiency
