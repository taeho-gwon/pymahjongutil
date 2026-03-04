from pymahjongutil.enum.common import ActionTypeEnum, RoundResultTypeEnum, WindEnum
from pymahjongutil.schema.game_record import GameRecord
from pymahjongutil.schema.game_state import GameState
from pymahjongutil.schema.round_record import RoundRecord

_WIND_ORDER: list[WindEnum] = [
    WindEnum.EAST,
    WindEnum.SOUTH,
    WindEnum.WEST,
    WindEnum.NORTH,
]

_SPECIAL_DRAW_TYPES: set[RoundResultTypeEnum] = {
    RoundResultTypeEnum.FOUR_WINDS_DRAW,
    RoundResultTypeEnum.FOUR_KANS_DRAW,
    RoundResultTypeEnum.FOUR_RIICHI_DRAW,
    RoundResultTypeEnum.NINE_TILES_DRAW,
    RoundResultTypeEnum.THREE_RON_DRAW,
}

_WIN_TYPES: set[RoundResultTypeEnum] = {
    RoundResultTypeEnum.TSUMO,
    RoundResultTypeEnum.RON,
}


class GameManager:
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._initial_scores: list[int] = list(state.scores)

    @property
    def state(self) -> GameState:
        return self._state

    @staticmethod
    def create_new(scores: list[int] | None = None) -> "GameManager":
        if scores is None:
            scores = [25000, 25000, 25000, 25000]
        state = GameState(
            round_wind=WindEnum.EAST,
            round_number=1,
            honba=0,
            riichi_sticks=0,
            scores=list(scores),
        )
        return GameManager(state)

    @staticmethod
    def create_from_record(record: GameRecord) -> "GameManager":
        manager = GameManager.create_new(list(record.initial_scores))
        for round_record in record.rounds:
            manager.complete_round(round_record)
        return manager

    def complete_round(self, record: RoundRecord) -> None:
        if record.result is None:
            msg = "RoundRecord must have a result to complete a round"
            raise ValueError(msg)

        result = record.result
        s = self._state

        # 1. Apply point diffs
        for i in range(4):
            s.scores[i] += result.point_diffs[i]

        # 2. Count riichi actions in this round
        round_riichi_count = sum(
            1 for action in record.actions if action.type is ActionTypeEnum.RIICHI
        )

        # 3. Riichi sticks handling
        if result.type in _WIN_TYPES:
            s.riichi_sticks = 0
        else:
            s.riichi_sticks += round_riichi_count

        # 4. Dealer continuation logic
        dealer = s.dealer
        dealer_continues = False

        if result.type in _WIN_TYPES:
            dealer_continues = dealer in result.winners
        elif result.type is RoundResultTypeEnum.EXHAUSTIVE_DRAW:
            dealer_continues = (
                len(result.is_tenpai) > dealer and result.is_tenpai[dealer]
            )
        elif result.type in _SPECIAL_DRAW_TYPES:
            dealer_continues = True

        # 5. Advance round
        if dealer_continues:
            s.honba += 1
        else:
            if result.type in _WIN_TYPES:
                s.honba = 0
            else:
                s.honba += 1
            self._advance_round()

        # 6. Save record
        s.round_records.append(record)

    def _advance_round(self) -> None:
        s = self._state
        s.round_number += 1
        if s.round_number > 4:
            wind_idx = _WIND_ORDER.index(s.round_wind)
            next_idx = (wind_idx + 1) % len(_WIND_ORDER)
            s.round_wind = _WIND_ORDER[next_idx]
            s.round_number = 1

    def to_record(self) -> GameRecord:
        return GameRecord(
            initial_scores=list(self._initial_scores),
            rounds=list(self._state.round_records),
        )

    @property
    def is_game_over(self) -> bool:
        wind_idx = _WIND_ORDER.index(self._state.round_wind)
        south_idx = _WIND_ORDER.index(WindEnum.SOUTH)
        return wind_idx > south_idx
