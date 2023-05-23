from pymahjong.hand_checker.riichi_checker import RiichiChecker
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.agari_info import AgariInfo


def assert_yaku_check(test_input, expected, yaku):
    hand = get_hand_from_code(test_input)
    result = any(
        yaku.is_satisfied(division, AgariInfo())
        for division in RiichiChecker(hand).calculate_divisions(True)
    )
    assert result == expected
