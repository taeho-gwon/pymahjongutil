from mahjong.shanten import Shanten

from pymahjong.schema.count import HandCount

shanten_calculator = Shanten()


def calculate_deficiency(hand_count: HandCount) -> int:
    return min(
        calculate_normal_deficiency(hand_count),
        calculate_seven_pairs_deficiency(hand_count),
        calculate_thirteen_orphans_deficiency(hand_count),
    )


def calculate_normal_deficiency(hand_count: HandCount) -> int:
    return (
        shanten_calculator.calculate_shanten_for_regular_hand(
            hand_count.concealed_count.convert_to_list34()
        )
        + 1
    )


def calculate_seven_pairs_deficiency(hand_count: HandCount) -> int:
    return (
        shanten_calculator.calculate_shanten_for_chiitoitsu_hand(
            hand_count.concealed_count.convert_to_list34()
        )
        + 1
    )


def calculate_thirteen_orphans_deficiency(hand_count: HandCount) -> int:
    return (
        shanten_calculator.calculate_shanten_for_kokushi_hand(
            hand_count.concealed_count.convert_to_list34()
        )
        + 1
    )
