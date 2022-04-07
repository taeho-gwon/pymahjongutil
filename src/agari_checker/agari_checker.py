from typing import Iterable

from src.schema.hand import Hand
from src.schema.tile import Tile


def check_agari_normal(hand: Hand) -> bool:
    hand_counts = hand.concealed_counts
    tile_iter = Tile.all()
    return _check_agari_tile_normal_rec(tile_iter, hand_counts, False)


def _check_agari_tile_normal_rec(
    tile_iter: Iterable[Tile], hand_counts: dict[Tile, int], has_head: bool
):
    return True


def check_agari_seven_pair(hand: Hand) -> bool:
    return not hand.is_opened and all(
        tile_count == 2 for tile_count in hand.counts.values()
    )


def check_agari_thirteen_orphans(hand: Hand) -> bool:
    return (
        not hand.is_opened
        and len(count := hand.counts) == 13
        and all(orphan in count for orphan in Tile.terminals_and_honors())
    )
