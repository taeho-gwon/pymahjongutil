from src.schema.hand import Hand


def calculate_shanten(hand: Hand) -> int:
    return min(
        _calculate_normal_shanten(hand),
        _calculate_seven_pairs_shanten(hand),
        _calculate_thirteen_orphans_shanten(hand),
    )


def _calculate_normal_shanten(hand: Hand) -> int:
    return 100


def _calculate_seven_pairs_shanten(hand: Hand) -> int:
    if hand.is_opened:
        return 100

    hand_counts = hand.counts
    num_excess = sum((x - 2 for x in hand_counts if x > 2))
    num_single = sum(1 for x in hand_counts if x == 1)
    return num_excess + (
        (num_single - num_excess - 1) // 2 if num_single > num_excess else 0
    )


def _calculate_thirteen_orphans_shanten(hand: Hand) -> int:
    return 100
