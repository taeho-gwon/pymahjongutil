from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tiles
from pymahjong.yaku_checker.yakuman.base_yakuman import BaseYakuman


class Chiihou(BaseYakuman):
    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        return (
            agari_info.is_first_turn
            and agari_info.player_wind != Tiles.WINDS[0]
            and agari_info.is_tsumo_agari
        )