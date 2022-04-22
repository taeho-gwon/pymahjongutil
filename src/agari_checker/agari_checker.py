from src.schema.hand import Hand
from src.schema.tile import TileCount, Tiles


def check_agari_normal(hand: Hand) -> bool:
    hand_counts = hand.concealed_counts
    return _check_agari_tile_normal_rec(0, hand_counts, False)


def _check_agari_tile_normal_rec(idx: int, hand_counts: TileCount, has_head: bool):
    idx = hand_counts.get_last_nonzero_idx(idx)
    if idx == len(Tiles.ALL):
        return True

    if not has_head and hand_counts[idx] >= 2:
        hand_counts[idx] -= 2
        if _check_agari_tile_normal_rec(idx, hand_counts, True):
            return True
        hand_counts[idx] += 2

    if hand_counts[idx] >= 3:
        hand_counts[idx] -= 3
        if _check_agari_tile_normal_rec(idx, hand_counts, has_head):
            return True
        hand_counts[idx] += 3

    if (
        Tiles.ALL[idx] in Tiles.STRAIGHT_STARTS
        and hand_counts[idx + 1] >= 1
        and hand_counts[idx + 2] >= 1
    ):
        hand_counts[idx] -= 1
        hand_counts[idx + 1] -= 1
        hand_counts[idx + 2] -= 1
        if _check_agari_tile_normal_rec(idx, hand_counts, has_head):
            return True
        hand_counts[idx] += 1
        hand_counts[idx + 1] += 1
        hand_counts[idx + 2] += 1

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
