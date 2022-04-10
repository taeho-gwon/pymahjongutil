from src.constants import Tiles
from src.schema.hand import Hand
from src.schema.tile import TileCount


def check_agari_normal(hand: Hand) -> bool:
    hand_counts = hand.concealed_counts
    return _check_agari_tile_normal_rec(0, hand_counts, False)


def _check_agari_tile_normal_rec(idx: int, hand_counts: TileCount, has_head: bool):
    pass


def check_agari_seven_pair(hand: Hand) -> bool:
    hand_counts = hand.counts
    return not hand.is_opened and all(hand_counts[tile] == 2 for tile in hand_counts)


def check_agari_thirteen_orphans(hand: Hand) -> bool:
    return (
        not hand.is_opened
        and len(count := hand.counts) == 13
        and all(orphan in count for orphan in Tiles.TERMINALS_AND_HONORS)
    )
