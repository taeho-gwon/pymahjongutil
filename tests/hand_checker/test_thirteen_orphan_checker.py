import pytest

from pymahjongutil.hand_checker.thirteen_orphan_checker import ThirteenOrphanChecker
from pymahjongutil.hand_parser import get_hand_from_code, get_tile_from_code
from pymahjongutil.schema.efficiency_data import EfficiencyData


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
    assert ThirteenOrphanChecker(hand).check_agari() == expected


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
    assert ThirteenOrphanChecker(hand).calculate_deficiency() == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "58m23p189s234566z9p",
            [
                ("5m", ["1m", "9m", "1p", "1z", "7z"], 20),
                ("8m", ["1m", "9m", "1p", "1z", "7z"], 20),
                ("2p", ["1m", "9m", "1p", "1z", "7z"], 20),
                ("3p", ["1m", "9m", "1p", "1z", "7z"], 20),
                ("8s", ["1m", "9m", "1p", "1z", "7z"], 20),
            ],
        ),
        (
            "19m19p159s1234567z",
            [
                (
                    "5s",
                    [
                        "1m",
                        "9m",
                        "1p",
                        "9p",
                        "1s",
                        "9s",
                        "1z",
                        "2z",
                        "3z",
                        "4z",
                        "5z",
                        "6z",
                        "7z",
                    ],
                    39,
                ),
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

    assert ThirteenOrphanChecker(hand).calculate_efficiency() == expected_efficiency
