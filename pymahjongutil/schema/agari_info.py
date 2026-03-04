from dataclasses import dataclass

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.tile import Tiles
from pymahjongutil.schema.tile_index import TileIndex



@dataclass
class AgariInfo:
    is_tsumo_agari: bool = False
    round_wind: WindEnum = WindEnum.EAST
    player_wind: WindEnum = WindEnum.EAST
    loser_wind: WindEnum = WindEnum.EAST
    is_ready_hand: bool = False
    is_double_ready_hand: bool = False
    is_one_shot: bool = False
    is_last_draw: bool = False
    is_last_discard: bool = False
    is_dead_wall_draw: bool = False
    is_robbing_a_quad: bool = False
    is_first_turn: bool = False

    @property
    def round_wind_idx(self) -> TileIndex:
        return TileIndex.create_from_wind_enum(self.round_wind)

    @property
    def player_wind_idx(self) -> TileIndex:
        return TileIndex.create_from_wind_enum(self.player_wind)

    @property
    def loser_wind_idx(self) -> TileIndex:
        return TileIndex.create_from_wind_enum(self.loser_wind)

    @property
    def player_seat(self) -> int:
        return self.player_wind_idx - Tiles.WINDS[0]

    @property
    def loser_seat(self) -> int:
        return self.loser_wind_idx - Tiles.WINDS[0]

    @property
    def is_dealer(self) -> bool:
        return self.player_wind is WindEnum.EAST
