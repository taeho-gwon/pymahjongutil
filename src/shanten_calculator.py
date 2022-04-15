from src.schema.hand import Hand


def calculate_shanten(hand: Hand) -> int:
    return min(
        _calculate_normal_shanten(hand),
        _calculate_seven_pairs_shanten(hand),
        _calculate_thirteen_orphans_shanten(hand),
    )


def _calculate_normal_shanten(hand: Hand) -> int:
    return 0


def _calculate_seven_pairs_shanten(hand: Hand) -> int:
    return 0


def _calculate_thirteen_orphans_shanten(hand: Hand) -> int:
    return 0
