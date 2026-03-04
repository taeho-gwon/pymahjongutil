from dataclasses import dataclass

from pymahjongutil.schema.tile_index import TileIndex


@dataclass
class GameTile:
    tile_index: TileIndex
    is_red: bool = False
