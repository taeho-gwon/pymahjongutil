from typing import Callable

from src.schema.count import HandCount, TileCount
from src.schema.tile import Tiles


def validate_hand_count_for_agari_checking(func: Callable[[HandCount], bool]):
    def validate(hand_count: HandCount):
        if hand_count.concealed_count.total_count % 3 != 2:
            raise ValueError("hand_count is invalid")
        return func(hand_count)

    return validate


@validate_hand_count_for_agari_checking
def check_agari_normal(hand_count: HandCount) -> bool:
    return _check_agari_tile_normal_rec(0, hand_count.concealed_count, False)


def _check_agari_tile_normal_rec(idx: int, tile_count: TileCount, has_head: bool):
    idx = tile_count.get_first_nonzero_idx(idx)
    if idx == len(Tiles.ALL):
        return True

    if not has_head and tile_count[idx] >= 2:
        tile_count[idx] -= 2
        if _check_agari_tile_normal_rec(idx, tile_count, True):
            return True
        tile_count[idx] += 2

    if tile_count[idx] >= 3:
        tile_count[idx] -= 3
        if _check_agari_tile_normal_rec(idx, tile_count, has_head):
            return True
        tile_count[idx] += 3

    if (
        Tiles.ALL[idx] in Tiles.STRAIGHT_STARTS
        and tile_count[idx + 1] >= 1
        and tile_count[idx + 2] >= 1
    ):
        tile_count[idx] -= 1
        tile_count[idx + 1] -= 1
        tile_count[idx + 2] -= 1
        if _check_agari_tile_normal_rec(idx, tile_count, has_head):
            return True
        tile_count[idx] += 1
        tile_count[idx + 1] += 1
        tile_count[idx + 2] += 1

    return False


@validate_hand_count_for_agari_checking
def check_agari_seven_pair(hand_count: HandCount) -> bool:
    head_count = sum(
        1 for tile in Tiles.ALL if hand_count.concealed_count.counts[tile] == 2
    )
    return head_count == 7


@validate_hand_count_for_agari_checking
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
