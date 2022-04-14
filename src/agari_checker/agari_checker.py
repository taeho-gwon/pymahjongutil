from src.schema.hand import Hand
from src.schema.tile import TileCount, Tiles


def check_agari_normal(hand: Hand) -> bool:
    hand_counts = hand.concealed_counts
    return _check_agari_tile_normal_rec(0, hand_counts, False)


def _check_agari_tile_normal_rec(idx: int, hand_counts: TileCount, has_head: bool):
    while idx < len(Tiles.ALL):
        if hand_counts[Tiles.ALL[idx]] != 0:
            break
        idx += 1
    else:
        return True
    return False


def check_agari_seven_pair(hand: Hand) -> bool:
    hand_counts = hand.counts
    head_counts = sum(1 for tile in Tiles.ALL if hand_counts[tile] == 2)
    zero_counts = sum(1 for tile in Tiles.ALL if hand_counts[tile] == 0)
    return not hand.is_opened and head_counts == 7 and zero_counts == 27


def check_agari_thirteen_orphans(hand: Hand) -> bool:
    hand_counts = hand.counts
    orphan_pair_counts = sum(
        1 for tile in Tiles.TERMINALS_AND_HONORS if hand_counts[tile] == 2
    )

    return (
        not hand.is_opened
        and orphan_pair_counts == 1
        and all(1 <= hand_counts[orphan] <= 2 for orphan in Tiles.TERMINALS_AND_HONORS)
    )
