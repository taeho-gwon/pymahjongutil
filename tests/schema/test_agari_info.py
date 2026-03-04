import pytest

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.tile import Tiles


class TestAgariInfoWindIdx:
    def test_round_wind_idx_east(self) -> None:
        info = AgariInfo(round_wind=WindEnum.EAST)
        assert info.round_wind_idx == Tiles.WINDS[0]

    def test_round_wind_idx_south(self) -> None:
        info = AgariInfo(round_wind=WindEnum.SOUTH)
        assert info.round_wind_idx == Tiles.WINDS[1]

    def test_player_wind_idx_west(self) -> None:
        info = AgariInfo(player_wind=WindEnum.WEST)
        assert info.player_wind_idx == Tiles.WINDS[2]

    def test_player_wind_idx_north(self) -> None:
        info = AgariInfo(player_wind=WindEnum.NORTH)
        assert info.player_wind_idx == Tiles.WINDS[3]

    def test_loser_wind_idx_east(self) -> None:
        info = AgariInfo(loser_wind=WindEnum.EAST)
        assert info.loser_wind_idx == Tiles.WINDS[0]

    def test_loser_wind_idx_south(self) -> None:
        info = AgariInfo(loser_wind=WindEnum.SOUTH)
        assert info.loser_wind_idx == Tiles.WINDS[1]


class TestAgariInfoSeat:
    def test_player_seat_east(self) -> None:
        info = AgariInfo(player_wind=WindEnum.EAST)
        assert info.player_seat == 0

    def test_player_seat_south(self) -> None:
        info = AgariInfo(player_wind=WindEnum.SOUTH)
        assert info.player_seat == 1

    def test_player_seat_west(self) -> None:
        info = AgariInfo(player_wind=WindEnum.WEST)
        assert info.player_seat == 2

    def test_player_seat_north(self) -> None:
        info = AgariInfo(player_wind=WindEnum.NORTH)
        assert info.player_seat == 3

    def test_loser_seat_east(self) -> None:
        info = AgariInfo(loser_wind=WindEnum.EAST)
        assert info.loser_seat == 0

    def test_loser_seat_north(self) -> None:
        info = AgariInfo(loser_wind=WindEnum.NORTH)
        assert info.loser_seat == 3


class TestAgariInfoIsDealer:
    def test_is_dealer_when_east(self) -> None:
        info = AgariInfo(player_wind=WindEnum.EAST)
        assert info.is_dealer is True

    def test_is_not_dealer_when_south(self) -> None:
        info = AgariInfo(player_wind=WindEnum.SOUTH)
        assert info.is_dealer is False

    def test_is_not_dealer_when_west(self) -> None:
        info = AgariInfo(player_wind=WindEnum.WEST)
        assert info.is_dealer is False

    def test_is_not_dealer_when_north(self) -> None:
        info = AgariInfo(player_wind=WindEnum.NORTH)
        assert info.is_dealer is False


class TestAgariInfoDefaults:
    def test_default_values(self) -> None:
        info = AgariInfo()
        assert info.is_tsumo_agari is False
        assert info.round_wind is WindEnum.EAST
        assert info.player_wind is WindEnum.EAST
        assert info.loser_wind is WindEnum.EAST
        assert info.is_ready_hand is False
        assert info.is_double_ready_hand is False
        assert info.is_one_shot is False
        assert info.is_last_draw is False
        assert info.is_last_discard is False
        assert info.is_dead_wall_draw is False
        assert info.is_robbing_a_quad is False
        assert info.is_first_turn is False
