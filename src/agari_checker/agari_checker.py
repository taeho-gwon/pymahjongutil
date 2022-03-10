from collections import Counter

from src.schema.hand import Hand
from src.schema.tile import Tile


def check_agari_seven_pair(hand: Hand) -> bool:
    if hand.is_opened:
        return False

    count = Counter(hand.concealed_tiles)
    if hand.draw_tile is not None:
        count[hand.draw_tile] += 1

    return all(tile_count == 2 for tile_count in count.values())


def check_agari_thirteen_orphans(hand: Hand) -> bool:
    if hand.is_opened:
        return False

    count = Counter(hand.concealed_tiles)
    if hand.draw_tile is not None:
        count[hand.draw_tile] += 1

    if len(count) != 13:
        return False

    return all(orphan in count for orphan in Tile.terminals_and_honors())
