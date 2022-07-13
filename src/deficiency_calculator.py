from functools import partial, reduce
from itertools import dropwhile, product, tee
from typing import Iterable

from src.enum.common import DecompositionPartType
from src.schema.count import HandCount, TileCount
from src.schema.quasi_decomposition import (
    KnowledgeBase,
    QuasiDecomposition,
    QuasiDecompositionType,
)
from src.schema.tile import Tile, Tiles


def calculate_normal_deficiency(hand_count: HandCount) -> int:
    knowledge_base = KnowledgeBase(
        counts={tile: 4 - hand_count[tile] for tile in Tiles.ALL}, block=Tiles.ALL
    )
    iter_types: Iterable[set[QuasiDecompositionType]] = get_iter_block_qdcmp_types(
        hand_count, knowledge_base
    )
    iter_types = list(iter_types)
    type_set: set[QuasiDecompositionType] = reduce(combine_typeset, iter_types)
    return min(
        (qdcmp_type.cost(knowledge_base) for qdcmp_type in type_set), default=100
    )


def get_iter_block_qdcmp_types(
    hand_count: HandCount, knowledge_base: KnowledgeBase
) -> Iterable[set[QuasiDecompositionType]]:
    blocks: list[list[Tile]] = [Tiles.MANS, Tiles.PINS, Tiles.SOUS] + [
        [t] for t in Tiles.HONORS
    ]
    create_from_qdcmp = partial(
        QuasiDecompositionType.create_from_qdcmp, knowledge_base
    )
    yield from (
        {create_from_qdcmp(QuasiDecomposition.create_from_call_count(call_count))}
        for call_count in hand_count.call_counts
    )

    for block in blocks:
        counts = {tile: hand_count.concealed_count.counts[tile] for tile in block}
        remaining_counts = {tile: 4 - hand_count[tile] for tile in block}
        iter_block_qdcmps = iter_qdcmps(
            TileCount(counts=counts, block=block),
            TileCount(counts=remaining_counts, block=block),
        )
        s = set(map(create_from_qdcmp, iter_block_qdcmps))
        yield s


def combine_typeset(
    type_set1: set[QuasiDecompositionType], type_set2: set[QuasiDecompositionType]
) -> set[QuasiDecompositionType]:
    return set(type1 + type2 for type1, type2 in product(type_set1, type_set2))


def iter_qdcmps(tile_counts: TileCount, remaining_counts: TileCount):
    states = {t: [tile_counts[t], remaining_counts[t]] for t in tile_counts.block}
    qdcmp = QuasiDecomposition(
        parts=[],
        remainder=TileCount.create_from_tiles([], block=tile_counts.block),
    )

    def _iter_qdcmps_rec(
        states: dict[Tile, list[int]],
        qdcmp: QuasiDecomposition,
        iter_tile: Iterable[Tile],
    ):
        iter_tile, iter_tile_tmp = tee(
            dropwhile(lambda x: states[x][0] == 0, iter_tile)
        )
        try:
            tile = next(iter_tile_tmp)
        except StopIteration:
            if qdcmp.is_valid:
                yield qdcmp
            return

        states[tile][0] -= 1
        qdcmp.remainder[tile] += 1
        iter_tile, iter_tile_tmp = tee(iter_tile)
        yield from _iter_qdcmps_rec(states, qdcmp, iter_tile_tmp)
        qdcmp.remainder[tile] -= 1

        if states[tile][0] >= 2:
            states[tile][0] -= 2
            qdcmp.append(tile_count=TileCount.create_from_tiles([tile] * 3))
            iter_tile, iter_tile_tmp = tee(iter_tile)
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile_tmp)
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
            iter_tile, iter_tile_tmp = tee(iter_tile)
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile_tmp)
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
            iter_tile, iter_tile_tmp = tee(iter_tile)
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile_tmp)
            qdcmp.pop()
            states[tile][0] += 1

        if next_state[0] >= 1 and (next2_state[1] > 0 or prev_state[1] > 0):
            next_state[0] -= 1
            qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile, tile.next]),
                type=DecompositionPartType.PCHOW,
            )
            iter_tile, iter_tile_tmp = tee(iter_tile)
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile_tmp)
            qdcmp.pop()
            next_state[0] += 1

        if next2_state[0] >= 1 and next_state[1] > 0:
            next2_state[0] -= 1
            qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile, tile.next.next]),
                type=DecompositionPartType.PCHOW,
            )
            iter_tile, iter_tile_tmp = tee(iter_tile)
            yield from _iter_qdcmps_rec(states, qdcmp, iter_tile_tmp)
            qdcmp.pop()
            next2_state[0] += 1

        states[tile][0] += 1

    yield from _iter_qdcmps_rec(states, qdcmp, iter(tile_counts.block))


def calculate_seven_pairs_deficiency(hand_count: HandCount) -> int:
    if hand_count.call_counts:
        return 100

    concealed_tile_count_values = hand_count.concealed_count.counts.values()
    num_excess = sum((x - 2 for x in concealed_tile_count_values if x > 2))
    num_single = sum(1 for x in concealed_tile_count_values if x == 1)
    return num_excess + (
        (num_single - num_excess + 1) // 2 if num_single >= num_excess else 1
    )


def calculate_thirteen_orphans_deficiency(hand_count: HandCount) -> int:
    if hand_count.call_counts:
        return 100

    concealed_count = hand_count.concealed_count
    num_terminals_and_honors = sum(
        1 for tile in Tiles.TERMINALS_AND_HONORS if concealed_count[tile] > 0
    )
    has_terminals_and_honors_pair = any(
        concealed_count[tile] >= 2 for tile in Tiles.TERMINALS_AND_HONORS
    )
    return 14 - num_terminals_and_honors - int(has_terminals_and_honors_pair)
