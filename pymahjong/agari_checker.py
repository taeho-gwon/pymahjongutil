from typing import Callable

from pymahjong.deficiency_calculator import (
    calculate_normal_deficiency,
    calculate_seven_pairs_deficiency,
    calculate_thirteen_orphans_deficiency,
)
from pymahjong.schema.count import HandCount


def validate_hand_count_for_agari_checking(func: Callable[[HandCount], bool]):
    def validate(hand_count: HandCount):
        if hand_count.concealed_count.total_count % 3 != 2:
            raise ValueError("hand_count is invalid")
        return func(hand_count)

    return validate


@validate_hand_count_for_agari_checking
def check_normal_agari(hand_count: HandCount) -> bool:
    return calculate_normal_deficiency(hand_count) == 0


@validate_hand_count_for_agari_checking
def check_seven_pairs_agari(hand_count: HandCount) -> bool:
    return calculate_seven_pairs_deficiency(hand_count) == 0


@validate_hand_count_for_agari_checking
def check_thirteen_orphans_agari(hand_count: HandCount) -> bool:
    return calculate_thirteen_orphans_deficiency(hand_count) == 0
