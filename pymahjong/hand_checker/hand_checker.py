from abc import ABC, abstractmethod

from pymahjong.schema.count import HandCount
from pymahjong.schema.efficiency_data import EfficiencyData
from pymahjong.schema.tile import Tile, Tiles


class HandChecker(ABC):
    @abstractmethod
    def calculate_deficiency(self, hand_count: HandCount) -> int:
        pass

    def calculate_efficiency(self, hand_count: HandCount) -> list[EfficiencyData]:
        deficiency = self.calculate_deficiency(hand_count)
        efficiency = []

        for discard_candidate in filter(
            lambda t: hand_count.concealed_count[t] > 0, Tiles.DEFAULTS
        ):
            hand_count.concealed_count[discard_candidate] -= 1
            if deficiency == self.calculate_deficiency(hand_count):
                ukeire, ukeire_count = self.calculate_ukeire(hand_count, deficiency)
                efficiency.append(
                    EfficiencyData(
                        discard_tile=discard_candidate,
                        ukeire=ukeire,
                        ukeire_count=ukeire_count,
                    )
                )
            hand_count.concealed_count[discard_candidate] += 1

        efficiency.sort()
        return efficiency

    def calculate_ukeire(
        self, hand_count: HandCount, deficiency: int
    ) -> tuple[list[Tile], int]:
        ukeire = []
        ukeire_count = 0
        for draw_candidate in filter(
            lambda t: hand_count.concealed_count[t] < 4, Tiles.DEFAULTS
        ):
            hand_count.concealed_count[draw_candidate] += 1
            if deficiency - 1 == self.calculate_deficiency(hand_count):
                ukeire.append(draw_candidate)
                ukeire_count += 5 - hand_count[draw_candidate]
            hand_count.concealed_count[draw_candidate] -= 1

        return ukeire, ukeire_count

    def check_agari(self, hand_count: HandCount) -> bool:
        if hand_count.concealed_count.total_count % 3 != 2:
            raise ValueError("hand_count is invalid")
        return self.calculate_deficiency(hand_count) == 0
