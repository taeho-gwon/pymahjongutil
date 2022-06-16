from src.schema.count import HandCount, TileCount
from src.schema.hand import Hand
from src.schema.tile import Tiles


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


def check_agari_seven_pair(hand_count: HandCount) -> bool:
    head_count = sum(
        1 for tile in Tiles.ALL if hand_count.concealed_count.counts[tile] == 2
    )
    return head_count == 7


def check_agari_thirteen_orphans(hand_count: HandCount) -> bool:
    orphan_pair_count = sum(
        1
        for tile in Tiles.TERMINALS_AND_HONORS
        if hand_count.concealed_count.counts[tile] == 2
    )
    orphan_count = sum(
        1
        for tile in Tiles.TERMINALS_AND_HONORS
        if hand_count.concealed_count.counts[tile] >= 1
    )
    return orphan_count == 13 and orphan_pair_count == 1
