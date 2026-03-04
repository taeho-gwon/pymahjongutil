from pymahjongutil.enum.common import ActionTypeEnum, CallTypeEnum
from pymahjongutil.schema.game_call import GameCall
from pymahjongutil.schema.game_tile import GameTile
from pymahjongutil.schema.player_state import PlayerState
from pymahjongutil.schema.round_action import RoundAction
from pymahjongutil.schema.round_record import RoundRecord
from pymahjongutil.schema.round_result import RoundResult
from pymahjongutil.schema.round_state import RoundState

_ACTION_TO_CALL_TYPE: dict[ActionTypeEnum, CallTypeEnum] = {
    ActionTypeEnum.CHII: CallTypeEnum.CHII,
    ActionTypeEnum.PON: CallTypeEnum.PON,
    ActionTypeEnum.BIG_MELDED_KAN: CallTypeEnum.BIG_MELDED_KAN,
}


def _remove_tile_from_hand(hand: list[GameTile], tile: GameTile) -> None:
    for i, h in enumerate(hand):
        if h.tile_index == tile.tile_index and h.is_red == tile.is_red:
            hand.pop(i)
            return
    msg = f"Tile {tile} not found in hand"
    raise ValueError(msg)


def _find_called_tile_idx(tiles: list[GameTile], discard: GameTile) -> int:
    for i, t in enumerate(tiles):
        if t.tile_index == discard.tile_index and t.is_red == discard.is_red:
            return i
    msg = f"Called tile {discard} not found in action tiles"
    raise ValueError(msg)


class RoundManager:
    def __init__(self, state: RoundState) -> None:
        self._state = state
        self._initial_hands: list[list[GameTile]] = [
            list(p.hand) for p in state.players
        ]
        self._initial_scores: list[int] = [p.score for p in state.players]
        self._initial_riichi_sticks: int = state.riichi_sticks

    @property
    def state(self) -> RoundState:
        return self._state

    @staticmethod
    def create_from_record(record: RoundRecord) -> "RoundManager":
        players = [
            PlayerState(
                hand=list(hand),
                discards=[],
                calls=[],
                score=score,
            )
            for hand, score in zip(record.initial_hands, record.scores, strict=True)
        ]
        state = RoundState(
            round_wind=record.round_wind,
            round_number=record.round_number,
            honba=record.honba,
            riichi_sticks=record.riichi_sticks,
            dealer=record.dealer,
            current_player=record.dealer,
            wall=record.wall,
            draw_index=0,
            players=players,
        )
        return RoundManager(state)

    def apply_action(self, action: RoundAction) -> None:
        s = self._state
        player = s.players[action.actor]

        match action.type:
            case ActionTypeEnum.DRAW:
                player.hand.append(action.tiles[0])
                s.draw_index += 1
                s.current_player = action.actor

            case ActionTypeEnum.DISCARD:
                _remove_tile_from_hand(player.hand, action.tiles[0])
                player.discards.append(action.tiles[0])
                s.current_player = (action.actor + 1) % 4

            case ActionTypeEnum.RIICHI:
                _remove_tile_from_hand(player.hand, action.tiles[0])
                player.discards.append(action.tiles[0])
                player.is_riichi = True
                player.score -= 1000
                s.riichi_sticks += 1
                s.current_player = (action.actor + 1) % 4

            case (
                ActionTypeEnum.CHII | ActionTypeEnum.PON | ActionTypeEnum.BIG_MELDED_KAN
            ):
                self._apply_open_call(action, player, s)
                if action.type is ActionTypeEnum.BIG_MELDED_KAN:
                    s.dora_count += 1

            case ActionTypeEnum.CONCEALED_KAN:
                for t in action.tiles:
                    _remove_tile_from_hand(player.hand, t)
                player.calls.append(
                    GameCall(
                        type=CallTypeEnum.CONCEALED_KAN,
                        tiles=list(action.tiles),
                        call_idx=0,
                    )
                )
                s.dora_count += 1
                s.current_player = action.actor

            case ActionTypeEnum.SMALL_MELDED_KAN:
                self._apply_small_melded_kan(action, player)
                s.dora_count += 1
                s.current_player = action.actor

            case (
                ActionTypeEnum.TSUMO
                | ActionTypeEnum.RON
                | ActionTypeEnum.NINE_TILES_DRAW
            ):
                pass

        s.action_history.append(action)

    def _apply_open_call(
        self, action: RoundAction, player: PlayerState, state: RoundState
    ) -> None:
        assert action.target is not None
        target_player = state.players[action.target]
        last_discard = target_player.discards[-1]
        call_idx = _find_called_tile_idx(action.tiles, last_discard)

        for i, t in enumerate(action.tiles):
            if i != call_idx:
                _remove_tile_from_hand(player.hand, t)

        call_type = _ACTION_TO_CALL_TYPE[action.type]
        player.calls.append(
            GameCall(type=call_type, tiles=list(action.tiles), call_idx=call_idx)
        )
        state.current_player = action.actor

    def _apply_small_melded_kan(self, action: RoundAction, player: PlayerState) -> None:
        tile_index = action.tiles[0].tile_index
        pon_idx = -1
        for i, call in enumerate(player.calls):
            if call.type == CallTypeEnum.PON and call.tiles[0].tile_index == tile_index:
                pon_idx = i
                break

        if pon_idx == -1:
            msg = "No matching PON call found for SMALL_MELDED_KAN"
            raise ValueError(msg)

        for i, h in enumerate(player.hand):
            if h.tile_index == tile_index:
                player.hand.pop(i)
                break

        old_call = player.calls[pon_idx]
        player.calls[pon_idx] = GameCall(
            type=CallTypeEnum.SMALL_MELDED_KAN,
            tiles=list(action.tiles),
            call_idx=old_call.call_idx,
        )

    def to_record(self, result: RoundResult | None = None) -> RoundRecord:
        return RoundRecord(
            round_wind=self._state.round_wind,
            round_number=self._state.round_number,
            honba=self._state.honba,
            riichi_sticks=self._initial_riichi_sticks,
            scores=list(self._initial_scores),
            dealer=self._state.dealer,
            wall=self._state.wall,
            initial_hands=[list(h) for h in self._initial_hands],
            actions=list(self._state.action_history),
            result=result,
        )
