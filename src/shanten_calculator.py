from functools import partial, reduce
from itertools import product
from typing import Iterable

from src.enum.common import DecompositionPartType
from src.schema.count import HandCount, TileCount
from src.schema.quasi_decomposition import (
    KnowledgeBase,
    QuasiDecomposition,
    QuasiDecompositionType,
)
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
    knowledge_base: KnowledgeBase = KnowledgeBase(
        counts=[4 - hand_count[t] for t in Tiles.ALL]
    )
    types: list[set[QuasiDecompositionType]] = [
        set(
            map(
                partial(QuasiDecompositionType.create_from_qdcmp, knowledge_base),
                iter_qdcmps(hand_count, block),
            )
        )
        for block in blocks
    ]

    type_set: set[QuasiDecompositionType] = reduce(combine_typeset, types)
    return min(
        (qdcmp_type.cost(knowledge_base) - 1 for qdcmp_type in type_set), default=100
    )


def combine_typeset(
    type_set1: set[QuasiDecompositionType], type_set2: set[QuasiDecompositionType]
) -> set[QuasiDecompositionType]:
    return set(type1 + type2 for type1, type2 in product(type_set1, type_set2))


def iter_qdcmps(hand_count: HandCount, block: list[Tile]):
    states = {t: [hand_count.concealed_count[t], 4 - hand_count[t]] for t in block}
    qdcmp = QuasiDecomposition(
        parts=[TileCount(counts=call_count) for call_count in hand_count.call_counts],
        remainder=TileCount.create_from_tiles([]),
    )

    def _iter_qdcmps_rec(
        states: dict[Tile, list[int]],
        qdcmp: QuasiDecomposition,
        iter_tile: Iterable[Tile],
    ):
        try:
            tile = next(t for t in iter_tile if states[t][0] > 0)
        except StopIteration:
            if qdcmp.is_valid:
                yield qdcmp
            return

        states[tile][0] -= 1
        qdcmp.remainder[tile] += 1
        yield from _iter_qdcmps_rec(states, qdcmp, iter_tile)
        qdcmp.remainder[tile] -= 1

        if states[tile][0] >= 2:
            states[tile][0] -= 2
            qdcmp.append(tile_count=TileCount.create_from_tiles([tile] * 3))
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile)
            qdcmp.pop()
            states[tile][0] += 2

        prev_state = states.get(tile.prev, [0, 0])
        next_state = states.get(tile.next, [0, 0])
        next2_state = states.get(tile.next.next, [0, 0])
        if next_state[0] >= 1 and next2_state[0] >= 1:
            next_state[0] -= 1
            next2_state[0] -= 1
            qdcmp.append(
                tile_count=TileCount.create_from_tiles(
                    [tile, tile.next, tile.next.next]
                )
            )
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile)
            qdcmp.pop()
            next_state[0] += 1
            next2_state[0] += 1

        if states[tile][0] >= 1:
            states[tile][0] -= 1
            qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile] * 2),
                is_incompletable_pair=states[tile][1] == 0,
                type=DecompositionPartType.PAIR,
            )
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile)
            qdcmp.pop()
            states[tile][0] += 1

        if next_state[0] >= 1 and (next2_state[1] > 0 or prev_state[1] > 0):
            next_state[0] -= 1
            qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile, tile.next]),
                type=DecompositionPartType.PCHOW,
            )
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile)
            qdcmp.pop()
            next_state[0] += 1

        if next2_state[0] >= 1 and next_state[1] > 0:
            next2_state[0] -= 1
            qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile, tile.next.next]),
                type=DecompositionPartType.PCHOW,
            )
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile)
            qdcmp.pop()
            next2_state[0] += 1

        states[tile][0] += 1

    yield from _iter_qdcmps_rec(states, qdcmp, iter(block))


def _calculate_seven_pairs_shanten(hand_count: HandCount) -> int:
    if hand_count.call_counts:
        return 100

    concealed_count = hand_count.concealed_count
    num_excess = sum((x - 2 for x in concealed_count.counts if x > 2))
    num_single = sum(1 for x in concealed_count.counts if x == 1)
    return num_excess + (
        (num_single - num_excess - 1) // 2 if num_single > num_excess else 0
    )


def _calculate_thirteen_orphans_shanten(hand_count: HandCount) -> int:
    if hand_count.call_counts:
        return 100

    concealed_count = hand_count.concealed_count
    num_terminals_and_honors = sum(
        1 for tile in Tiles.TERMINALS_AND_HONORS if concealed_count[tile] > 0
    )
    has_terminals_and_honors_pair = any(
        concealed_count[tile] >= 2 for tile in Tiles.TERMINALS_AND_HONORS
    )
    return 13 - num_terminals_and_honors - int(has_terminals_and_honors_pair)
