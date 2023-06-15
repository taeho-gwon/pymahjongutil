from pydantic import BaseModel

from pymahjong.schema.tile import Tile, Tiles


class AgariInfo(BaseModel):
    is_tsumo_agari: bool = False
    round_wind: Tile = Tiles.WINDS[0]
    player_wind: Tile = Tiles.WINDS[0]
    loser_wind: Tile = Tiles.WINDS[0]
    is_ready_hand: bool = False
    is_double_ready_hand: bool = False
    is_one_shot: bool = False
    is_last_draw: bool = False
    is_last_discard: bool = False
    is_dead_wall_draw: bool = False
    is_robbing_a_quad: bool = False
    is_first_turn: bool = False
