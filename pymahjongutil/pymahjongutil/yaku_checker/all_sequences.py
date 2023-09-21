from pymahjongutil.enum.common import DivisionPartTypeEnum, YakuEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.tile import Tile, Tiles
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


class AllSequences(BaseYaku):
    def __init__(self):
        super().__init__(YakuEnum.ALL_SEQUENCES)

    def is_satisfied(self, division: Division, agari_info: AgariInfo):
        if division.is_opened or division.parts[0].type is DivisionPartTypeEnum.HEAD:
            return False

        num_sequences = sum(
            1 for part in division.parts if part.type is DivisionPartTypeEnum.SEQUENCE
        )
        if num_sequences < 4:
            return False

        head = next(
            part for part in division.parts if part.type is DivisionPartTypeEnum.HEAD
        )
        if (
            head.counts[agari_info.player_wind_idx] > 0
            or head.counts[agari_info.round_wind_idx] > 0
            or head.counts[Tiles.DRAGONS[0]] > 0
            or head.counts[Tiles.DRAGONS[1]] > 0
            or head.counts[Tiles.DRAGONS[2]] > 0
        ):
            return False

        idx = division.parts[0].counts.find_earliest_nonzero_index()
        if division.agari_tile == Tile(value=idx + 1):
            return False

        if division.agari_tile == Tile(value=idx) and idx % 9 == 6:
            return False

        if division.agari_tile == Tile(value=idx + 2) and idx % 9 == 0:
            return False

        return True
