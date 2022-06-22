from functools import reduce
from itertools import product

from src.schema.count import HandCount
from src.schema.quasi_decomposition import QuasiDecomposition, QuasiDecompositionType
from src.schema.tile import Tile, Tiles


def calculate_shanten(hand_count: HandCount) -> int:
    return min(
        _calculate_normal_shanten(hand_count),
        _calculate_seven_pairs_shanten(hand_count),
        _calculate_thirteen_orphans_shanten(hand_count),
    )


def _calculate_normal_shanten(hand_count: HandCount) -> int:
    blocks: list[list[Tile]] = [Tiles.MANS, Tiles.PINS, Tiles.SOUS] + [
        [t] for t in Tiles.HONORS
    ]
    types: list[set[QuasiDecompositionType]] = [
        set(
            map(
                QuasiDecompositionType.create_from_qdcmp, iter_qdcmps(hand_count, block)
            )
        )
        for block in blocks
    ]
    type_set: set[QuasiDecompositionType] = reduce(combine_typeset, types)

    ke = any(
        hand_count.concealed_count[t] + hand_count.call_count[t] <= 2 for t in Tiles.ALL
    )
    km = any(
        hand_count.concealed_count[t] + hand_count.call_count[t] <= 1 for t in Tiles.ALL
    ) or any(
        hand_count.concealed_count[t] + hand_count.call_count[t] <= 3
        and hand_count.concealed_count[t.next] + hand_count.call_count[t.next] <= 3
        and hand_count.concealed_count[t.next.next] + hand_count.call_count[t.next.next]
        <= 3
        for t in Tiles.STRAIGHT_STARTS
    )
    return min((qdcmp_type.cost(ke, km) for qdcmp_type in type_set), default=100)


def combine_typeset(
    type_set1: set[QuasiDecompositionType], type_set2: set[QuasiDecompositionType]
) -> set[QuasiDecompositionType]:
    return set(type1 + type2 for type1, type2 in product(type_set1, type_set2))


def iter_qdcmps(hand_count: HandCount, block: list[Tile]):
    yield QuasiDecomposition(parts=[])


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
