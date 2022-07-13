from functools import partial, reduce
from itertools import dropwhile, product, tee
from typing import Iterable

from src.enum.common import DecompositionPartTypeEnum
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
    iter_types = get_iter_block_qdcmp_types(hand_count, knowledge_base)
    type_set = reduce(
        lambda s1, s2: set(type1 + type2 for type1, type2 in product(s1, s2)),
        iter_types,
    )
    return min(
        (qdcmp_type.cost(knowledge_base) for qdcmp_type in type_set), default=100
    )


def get_iter_block_qdcmp_types(
    hand_count: HandCount, knowledge_base: KnowledgeBase
) -> Iterable[set[QuasiDecompositionType]]:
    blocks = [Tiles.MANS, Tiles.PINS, Tiles.SOUS] + [[t] for t in Tiles.HONORS]
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
        yield set(map(create_from_qdcmp, iter_block_qdcmps))


def iter_qdcmps(tile_counts: TileCount, remaining_counts: TileCount):
    qdcmp = QuasiDecomposition(
        parts=[],
        remainder=TileCount.create_from_tiles([], block=tile_counts.block),
    )

    def _iter_qdcmps_rec(
        _tile_counts: TileCount,
        _remaining_counts: TileCount,
        _qdcmp: QuasiDecomposition,
        _iter_tile: Iterable[Tile],
    ):
        _iter_tile, _iter_tile_tmp = tee(
            dropwhile(lambda x: _tile_counts[x] == 0, _iter_tile)
        )
        try:
            tile = next(_iter_tile_tmp)
        except StopIteration:
            if _qdcmp.is_valid:
                yield _qdcmp
            return

        _tile_counts[tile] -= 1
        _qdcmp.remainder[tile] += 1
        _iter_tile, _iter_tile_tmp = tee(_iter_tile)
        yield from _iter_qdcmps_rec(
            _tile_counts, _remaining_counts, _qdcmp, _iter_tile_tmp
        )
        _qdcmp.remainder[tile] -= 1

        if _tile_counts[tile] >= 2:
            _tile_counts[tile] -= 2
            _qdcmp.append(tile_count=TileCount.create_from_tiles([tile] * 3))
            _iter_tile, _iter_tile_tmp = tee(_iter_tile)
            yield from _iter_qdcmps_rec(
                _tile_counts, _remaining_counts, _qdcmp, _iter_tile_tmp
            )
            _qdcmp.pop()
            _tile_counts[tile] += 2

        if _tile_counts[tile.next] >= 1 and _tile_counts[tile.next.next] >= 1:
            _tile_counts[tile.next] -= 1
            _tile_counts[tile.next.next] -= 1
            _qdcmp.append(
                tile_count=TileCount.create_from_tiles(
                    [tile, tile.next, tile.next.next]
                )
            )
            _iter_tile, _iter_tile_tmp = tee(_iter_tile)
            yield from _iter_qdcmps_rec(
                _tile_counts, _remaining_counts, _qdcmp, _iter_tile_tmp
            )
            _qdcmp.pop()
            _tile_counts[tile.next] += 1
            _tile_counts[tile.next.next] += 1

        if _tile_counts[tile] >= 1:
            _tile_counts[tile] -= 1
            _qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile] * 2),
                is_incompletable_pair=_remaining_counts[tile] == 0,
                type=DecompositionPartTypeEnum.PAIR,
            )
            _iter_tile, _iter_tile_tmp = tee(_iter_tile)
            yield from _iter_qdcmps_rec(
                _tile_counts, _remaining_counts, _qdcmp, _iter_tile_tmp
            )
            _qdcmp.pop()
            _tile_counts[tile] += 1

        if _tile_counts[tile.next] >= 1 and (
            _tile_counts[tile.next.next] > 0 or _remaining_counts[tile.prev] > 0
        ):
            _tile_counts[tile.next] -= 1
            _qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile, tile.next]),
                type=DecompositionPartTypeEnum.PCHOW,
            )
            _iter_tile, _iter_tile_tmp = tee(_iter_tile)
            yield from _iter_qdcmps_rec(
                _tile_counts, _remaining_counts, _qdcmp, _iter_tile_tmp
            )
            _qdcmp.pop()
            _tile_counts[tile.next] += 1

        if _tile_counts[tile.next.next] >= 1 and _remaining_counts[tile.next] > 0:
            _tile_counts[tile.next.next] -= 1
            _qdcmp.append(
                tile_count=TileCount.create_from_tiles([tile, tile.next.next]),
                type=DecompositionPartTypeEnum.PCHOW,
            )
            _iter_tile, _iter_tile_tmp = tee(_iter_tile)
            yield from _iter_qdcmps_rec(
                _tile_counts, _remaining_counts, _qdcmp, _iter_tile_tmp
            )
            _qdcmp.pop()
            _tile_counts[tile.next.next] += 1

        _tile_counts[tile] += 1

    yield from _iter_qdcmps_rec(
        tile_counts, remaining_counts, qdcmp, iter(tile_counts.block)
    )


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
