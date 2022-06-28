from typing import Callable

from src.deficiency_calculator import (
    calculate_normal_deficiency,
    calculate_seven_pairs_deficiency,
    calculate_thirteen_orphans_deficiency,
)
from src.schema.count import HandCount


def validate_hand_count_for_agari_checking(func: Callable[[HandCount], bool]):
    def validate(hand_count: HandCount):
        if hand_count.concealed_count.total_count % 3 != 2:
            raise ValueError("hand_count is invalid")
        return func(hand_count)

    return validate


@validate_hand_count_for_agari_checking
def check_agari_normal(hand_count: HandCount) -> bool:
    return calculate_normal_deficiency(hand_count) == 0


@validate_hand_count_for_agari_checking
def check_agari_seven_pair(hand_count: HandCount) -> bool:
    return calculate_seven_pairs_deficiency(hand_count) == 0


@validate_hand_count_for_agari_checking
def check_agari_thirteen_orphans(hand_count: HandCount) -> bool:
    return calculate_thirteen_orphans_deficiency(hand_count) == 0
