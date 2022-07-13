from src.deficiency_calculator import calculate_deficiency
from src.schema.count import HandCount
from src.schema.efficiency_data import EfficiencyData
from src.schema.tile import Tile, Tiles


def calculate_efficiency(hand_count: HandCount) -> list[EfficiencyData]:
    deficiency = calculate_deficiency(hand_count)
    efficiency = []

    for discard_candidate in filter(
        lambda t: hand_count.concealed_count[t] > 0, Tiles.ALL
    ):
        hand_count.concealed_count[discard_candidate] -= 1
        if deficiency == calculate_deficiency(hand_count):
            ukeire, ukeire_count = calculate_ukeire(hand_count, deficiency)
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


def calculate_ukeire(hand_count: HandCount, deficiency: int) -> tuple[list[Tile], int]:
    ukeire = []
    ukeire_count = 0
    for draw_candidate in filter(
        lambda t: hand_count.concealed_count[t] < 4, Tiles.ALL
    ):
        hand_count.concealed_count[draw_candidate] += 1
        if deficiency - 1 == calculate_deficiency(hand_count):
            ukeire.append(draw_candidate)
            ukeire_count += 5 - hand_count[draw_candidate]
        hand_count.concealed_count[draw_candidate] -= 1

    return ukeire, ukeire_count
