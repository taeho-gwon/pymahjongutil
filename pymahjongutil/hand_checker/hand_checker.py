from abc import ABC, abstractmethod

from pymahjongutil.schema.count import HandCount
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.efficiency_data import EfficiencyData
from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.tile import Tile, Tiles


class HandChecker(ABC):
    def __init__(self, hand: Hand):
        self.hand = hand
        self.hand_count = HandCount.create_from_hand(hand)
        self.total_count = self.hand_count.total_count

    @abstractmethod
    def calculate_deficiency(self) -> int:
        pass

    @abstractmethod
    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        pass

    def calculate_divisions(self, is_tsumo_agari: bool) -> list[Division]:
        if (
            self.hand.last_tile is None
            or self.hand_count.concealed_count[self.hand.last_tile.value] == 0
        ):
            raise ValueError("agari tile is invalid")
        if not self.check_agari():
            return []
        return self._calculate_divisions(self.hand.last_tile, is_tsumo_agari)

    def calculate_efficiency(self) -> list[EfficiencyData]:
        deficiency = self.calculate_deficiency()
        efficiency = []

        for discard_candidate in filter(
            lambda t: self.hand_count.concealed_count[t] > 0, Tiles.DEFAULTS
        ):
            self.hand_count.concealed_count[discard_candidate] -= 1
            if deficiency == self.calculate_deficiency():
                ukeire, num_ukeire = self.calculate_ukeire(deficiency)
                efficiency.append(
                    EfficiencyData(
                        discard_tile=discard_candidate,
                        ukeire=ukeire,
                        num_ukeire=num_ukeire,
                    )
                )
            self.hand_count.concealed_count[discard_candidate] += 1

        efficiency.sort()
        return efficiency

    def calculate_ukeire(self, deficiency: int) -> tuple[list[int], int]:
        ukeire = []
        num_ukeire = 0
        for draw_candidate in filter(
            lambda t: self.hand_count.concealed_count[t] < 4, Tiles.DEFAULTS
        ):
            self.hand_count.concealed_count[draw_candidate] += 1
            if deficiency - 1 == self.calculate_deficiency():
                ukeire.append(draw_candidate)
                num_ukeire += 5 - self.hand_count[draw_candidate]
            self.hand_count.concealed_count[draw_candidate] -= 1

        return ukeire, num_ukeire

    def check_agari(self) -> bool:
        if self.hand_count.concealed_count.num_tiles % 3 != 2:
            raise ValueError("hand_count is invalid")
        return self.calculate_deficiency() == 0
