import pytest

from pymahjongutil.schema.tile_index import TileIndex


class TestTileIndex:
    def test_valid_range(self) -> None:
        for i in range(34):
            assert TileIndex(i) == i

    def test_boundary_values(self) -> None:
        assert TileIndex(0) == 0
        assert TileIndex(33) == 33

    def test_invalid_negative(self) -> None:
        with pytest.raises(ValueError, match="TileIndex must be between 0 and 33"):
            TileIndex(-1)

    def test_invalid_too_large(self) -> None:
        with pytest.raises(ValueError, match="TileIndex must be between 0 and 33"):
            TileIndex(34)

    def test_int_compatibility(self) -> None:
        t = TileIndex(5)
        assert isinstance(t, int)
        assert t + 1 == 6
        assert t * 2 == 10

    def test_is_number_tile(self) -> None:
        for i in range(27):
            assert TileIndex(i).is_number_tile
        for i in range(27, 34):
            assert not TileIndex(i).is_number_tile

    def test_is_honor_tile(self) -> None:
        for i in range(27):
            assert not TileIndex(i).is_honor_tile
        for i in range(27, 34):
            assert TileIndex(i).is_honor_tile

    def test_suit_number(self) -> None:
        assert TileIndex(0).suit_number == 0
        assert TileIndex(8).suit_number == 8
        assert TileIndex(9).suit_number == 0
        assert TileIndex(17).suit_number == 8
        assert TileIndex(18).suit_number == 0
        assert TileIndex(26).suit_number == 8

    def test_is_terminal(self) -> None:
        terminals = {0, 8, 9, 17, 18, 26}
        for i in range(34):
            t = TileIndex(i)
            assert t.is_terminal == (i in terminals)

    def test_is_terminal_or_honor(self) -> None:
        terminal_or_honor = {0, 8, 9, 17, 18, 26} | set(range(27, 34))
        for i in range(34):
            t = TileIndex(i)
            assert t.is_terminal_or_honor == (i in terminal_or_honor)

    def test_is_sequence_start(self) -> None:
        for i in range(34):
            t = TileIndex(i)
            expected = i < 27 and i % 9 <= 6
            assert t.is_sequence_start == expected

    def test_is_side_wait_start(self) -> None:
        for i in range(34):
            t = TileIndex(i)
            expected = i < 27 and i % 9 <= 7
            assert t.is_side_wait_start == expected

    def test_is_left_edge_wait_start(self) -> None:
        left_edge = {6, 15, 24}
        for i in range(34):
            t = TileIndex(i)
            assert t.is_left_edge_wait_start == (i in left_edge)

    def test_is_right_edge_wait_start(self) -> None:
        right_edge = {0, 9, 18}
        for i in range(34):
            t = TileIndex(i)
            assert t.is_right_edge_wait_start == (i in right_edge)
