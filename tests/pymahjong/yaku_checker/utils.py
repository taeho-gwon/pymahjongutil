from pymahjong.hand_checker.riichi_checker import RiichiChecker
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.agari_info import AgariInfo


def assert_yaku_check(test_input, expected, yaku, agari_info=None):
    if agari_info is None:
        agari_info = AgariInfo()

    hand = get_hand_from_code(test_input)
    result = any(
        yaku.is_satisfied(division, agari_info)
        for division in RiichiChecker(hand).calculate_divisions(
            is_tsumo_agari=agari_info.is_tsumo_agari
        )
    )
    assert result == expected
