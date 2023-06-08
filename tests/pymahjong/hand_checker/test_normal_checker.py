import pytest

from pymahjong.hand_checker.normal_checker import NormalChecker
from pymahjong.hand_parser import get_hand_from_code, get_tile_from_code
from pymahjong.schema.efficiency_data import EfficiencyData


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
    assert NormalChecker(hand).check_agari() == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123m456p789s1112z", 1),
        ("123m456p789s1111z", 2),
        ("123m4569999p789s", 2),
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
    assert NormalChecker(hand).calculate_deficiency() == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "69m5678p2789s344z7p",
            [
                (
                    "9m",
                    [
                        "4m",
                        "5m",
                        "6m",
                        "7m",
                        "8m",
                        "6p",
                        "9p",
                        "1s",
                        "2s",
                        "3s",
                        "4s",
                        "3z",
                        "4z",
                    ],
                    46,
                ),
                (
                    "3z",
                    [
                        "4m",
                        "5m",
                        "6m",
                        "7m",
                        "8m",
                        "9m",
                        "6p",
                        "9p",
                        "1s",
                        "2s",
                        "3s",
                        "4s",
                        "4z",
                    ],
                    46,
                ),
                (
                    "6m",
                    ["7m", "8m", "9m", "6p", "9p", "1s", "2s", "3s", "4s", "3z", "4z"],
                    38,
                ),
                (
                    "2s",
                    ["4m", "5m", "6m", "7m", "8m", "9m", "6p", "9p", "3z", "4z"],
                    34,
                ),
            ],
        ),
    ],
)
def test_calculate_efficiency(test_input, expected):
    hand = get_hand_from_code(test_input)
    expected_efficiency = [
        EfficiencyData(
            discard_tile=get_tile_from_code(discard_tile_code),
            ukeire=list(map(get_tile_from_code, ukeire_codes)),
            num_ukeire=num_ukeire,
        )
        for discard_tile_code, ukeire_codes, num_ukeire in expected
    ]

    assert NormalChecker(hand).calculate_efficiency() == expected_efficiency
