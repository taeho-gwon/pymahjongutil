from dataclasses import dataclass

from pymahjongutil.schema.game_tile import GameTile


@dataclass
class Wall:
    tiles: list[GameTile]

    def __post_init__(self) -> None:
        if len(self.tiles) != 136:
            raise ValueError(f"Wall must have exactly 136 tiles, got {len(self.tiles)}")

    @property
    def live_wall(self) -> list[GameTile]:
        return self.tiles[:122]

    @property
    def dead_wall(self) -> list[GameTile]:
        return self.tiles[122:]

    @property
    def dora_indicators(self) -> list[GameTile]:
        return [self.tiles[132], self.tiles[130], self.tiles[128], self.tiles[126]]

    @property
    def ura_dora_indicators(self) -> list[GameTile]:
        return [self.tiles[133], self.tiles[131], self.tiles[129], self.tiles[127]]

    @property
    def rinshan_tiles(self) -> list[GameTile]:
        return [self.tiles[134], self.tiles[135], self.tiles[122], self.tiles[123]]
