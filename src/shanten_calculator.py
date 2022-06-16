from src.schema.count import HandCount, TileCount
from src.schema.tile import Tiles


def calculate_shanten(hand_count: HandCount) -> int:
    return min(
        _calculate_normal_shanten(hand_count),
        _calculate_seven_pairs_shanten(hand_count),
        _calculate_thirteen_orphans_shanten(hand_count),
    )


def _calculate_normal_shanten(hand_count: HandCount) -> int:
    return 100
    # concealed_counts = hand.concealed_counts
    # num_call = len(hand.calls)
    # best_shanten = [8]
    #
    # for tile in Tiles.ALL:
    #     if concealed_counts[tile] >= 2:
    #         concealed_counts[tile] -= 2
    #         _erase_complete_set(0, concealed_counts, num_call, 1, best_shanten)
    #         concealed_counts[tile] += 2
    #
    # _erase_complete_set(0, concealed_counts, num_call, 0, best_shanten)
    # return best_shanten[0]


def _erase_complete_set(
    idx: int,
    counts: TileCount,
    num_completes: int,
    num_pairs: int,
    best_shanten: list[int],
):
    idx = counts.get_last_nonzero_idx(idx)
    if idx == len(Tiles.ALL):
        _erase_partial_set(0, counts, num_completes, 0, num_pairs, best_shanten)
        return

    if counts[idx] >= 3:
        counts[idx] -= 3
        _erase_complete_set(idx, counts, num_completes + 1, num_pairs, best_shanten)
        counts[idx] += 3

    if (
        Tiles.ALL[idx] in Tiles.STRAIGHT_STARTS
        and counts[idx + 1] >= 1
        and counts[idx + 2] >= 1
    ):
        counts[idx] -= 1
        counts[idx + 1] -= 1
        counts[idx + 2] -= 1
        _erase_complete_set(idx, counts, num_completes + 1, num_pairs, best_shanten)
        counts[idx] += 1
        counts[idx + 1] += 1
        counts[idx + 2] += 1

    _erase_complete_set(idx + 1, counts, num_completes, num_pairs, best_shanten)


def _erase_partial_set(
    idx: int,
    counts: TileCount,
    num_completes: int,
    num_partials: int,
    num_pairs: int,
    best_shanten: list[int],
):
    idx = counts.get_last_nonzero_idx(idx)
    if idx == len(Tiles.ALL) or num_partials + num_completes >= 4:
        current_shanten = 8 - (num_completes * 2) - num_partials - num_pairs
        best_shanten[0] = min(best_shanten[0], current_shanten)
        return

    if counts[idx] >= 2:
        counts[idx] -= 2
        _erase_partial_set(
            idx, counts, num_completes, num_partials + 1, num_pairs, best_shanten
        )
        counts[idx] += 2

    if Tiles.ALL[idx] in Tiles.STRAIGHT_STARTS and counts[idx + 2] >= 1:
        counts[idx] -= 1
        counts[idx + 2] -= 1
        _erase_partial_set(
            idx, counts, num_completes, num_partials + 1, num_pairs, best_shanten
        )
        counts[idx] += 1
        counts[idx + 2] += 1

    if Tiles.ALL[idx] in Tiles.PARTIAL_STRAIGHT_STARTS and counts[idx + 1] >= 1:
        counts[idx] -= 1
        counts[idx + 1] -= 1
        _erase_partial_set(
            idx, counts, num_completes, num_partials + 1, num_pairs, best_shanten
        )
        counts[idx] += 1
        counts[idx + 1] += 1


def _calculate_seven_pairs_shanten(hand_count: HandCount) -> int:
    if hand_count.call_count.total_count > 0:
        return 100

    concealed_count = hand_count.concealed_count
    num_excess = sum((x - 2 for x in concealed_count.counts if x > 2))
    num_single = sum(1 for x in concealed_count.counts if x == 1)
    return num_excess + (
        (num_single - num_excess - 1) // 2 if num_single > num_excess else 0
    )


def _calculate_thirteen_orphans_shanten(hand_count: HandCount) -> int:
    if hand_count.call_count.total_count > 0:
        return 100

    concealed_count = hand_count.concealed_count
    num_terminals_and_honors = sum(
        1 for tile in Tiles.TERMINALS_AND_HONORS if concealed_count[tile] > 0
    )
    has_terminals_and_honors_pair = any(
        concealed_count[tile] >= 2 for tile in Tiles.TERMINALS_AND_HONORS
    )
    return 13 - num_terminals_and_honors - int(has_terminals_and_honors_pair)
