import pytest

from pymahjongutil.enum.common import CallTypeEnum, DivisionPartTypeEnum
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.count import TileCount
from pymahjongutil.schema.division import Division, DivisionPart
from pymahjongutil.schema.tile import Tile, Tiles


class TestDivisionPartFactoryMethods:
    def test_create_head(self) -> None:
        part = DivisionPart.create_head(tile=0, is_concealed=True)
        assert part.type is DivisionPartTypeEnum.HEAD
        assert part.is_concealed is True
        assert part.counts[0] == 2
        assert part.counts.num_tiles == 2

    def test_create_triple(self) -> None:
        part = DivisionPart.create_triple(tile=9, is_concealed=True)
        assert part.type is DivisionPartTypeEnum.TRIPLE
        assert part.is_concealed is True
        assert part.counts[9] == 3
        assert part.counts.num_tiles == 3

    def test_create_triple_not_concealed(self) -> None:
        part = DivisionPart.create_triple(tile=27, is_concealed=False)
        assert part.type is DivisionPartTypeEnum.TRIPLE
        assert part.is_concealed is False
        assert part.counts[27] == 3

    def test_create_straight(self) -> None:
        part = DivisionPart.create_straight(tile=0, is_concealed=True)
        assert part.type is DivisionPartTypeEnum.SEQUENCE
        assert part.is_concealed is True
        assert part.counts[0] == 1
        assert part.counts[1] == 1
        assert part.counts[2] == 1
        assert part.counts.num_tiles == 3

    def test_create_thirteen_orphans(self) -> None:
        part = DivisionPart.create_thirteen_orphans(
            head_tile=0, is_concealed=True
        )
        assert part.type is DivisionPartTypeEnum.THIRTEEN_ORPHANS
        assert part.is_concealed is True
        # 13 terminals/honors + 1 duplicate head = 14 tiles
        assert part.counts.num_tiles == 14
        # Head tile appears twice
        assert part.counts[0] == 2

    def test_create_from_call_chii(self) -> None:
        call = Call(
            type=CallTypeEnum.CHII,
            tiles=[Tile(0), Tile(1), Tile(2)],
            call_idx=0,
        )
        part = DivisionPart.create_from_call(call)
        assert part.type is DivisionPartTypeEnum.SEQUENCE
        assert part.is_concealed is False

    def test_create_from_call_pon(self) -> None:
        call = Call(
            type=CallTypeEnum.PON,
            tiles=[Tile(9), Tile(9), Tile(9)],
            call_idx=0,
        )
        part = DivisionPart.create_from_call(call)
        assert part.type is DivisionPartTypeEnum.TRIPLE
        assert part.is_concealed is False

    def test_create_from_call_concealed_kan(self) -> None:
        call = Call(
            type=CallTypeEnum.CONCEALED_KAN,
            tiles=[Tile(18), Tile(18), Tile(18), Tile(18)],
            call_idx=0,
        )
        part = DivisionPart.create_from_call(call)
        assert part.type is DivisionPartTypeEnum.QUAD
        assert part.is_concealed is True

    def test_create_from_call_big_melded_kan(self) -> None:
        call = Call(
            type=CallTypeEnum.BIG_MELDED_KAN,
            tiles=[Tile(27), Tile(27), Tile(27), Tile(27)],
            call_idx=0,
        )
        part = DivisionPart.create_from_call(call)
        assert part.type is DivisionPartTypeEnum.QUAD
        assert part.is_concealed is False

    def test_create_from_call_small_melded_kan(self) -> None:
        call = Call(
            type=CallTypeEnum.SMALL_MELDED_KAN,
            tiles=[Tile(31), Tile(31), Tile(31), Tile(31)],
            call_idx=0,
        )
        part = DivisionPart.create_from_call(call)
        assert part.type is DivisionPartTypeEnum.QUAD
        assert part.is_concealed is False


class TestDivisionPartIsTripletOrQuad:
    def test_head_is_not_triplet_or_quad(self) -> None:
        part = DivisionPart.create_head(tile=0, is_concealed=True)
        assert part.is_triplet_or_quad is False

    def test_sequence_is_not_triplet_or_quad(self) -> None:
        part = DivisionPart.create_straight(tile=0, is_concealed=True)
        assert part.is_triplet_or_quad is False

    def test_triple_is_triplet_or_quad(self) -> None:
        part = DivisionPart.create_triple(tile=0, is_concealed=True)
        assert part.is_triplet_or_quad is True

    def test_quad_is_triplet_or_quad(self) -> None:
        call = Call(
            type=CallTypeEnum.CONCEALED_KAN,
            tiles=[Tile(0), Tile(0), Tile(0), Tile(0)],
            call_idx=0,
        )
        part = DivisionPart.create_from_call(call)
        assert part.is_triplet_or_quad is True

    def test_thirteen_orphans_is_not_triplet_or_quad(self) -> None:
        part = DivisionPart.create_thirteen_orphans(
            head_tile=0, is_concealed=True
        )
        assert part.is_triplet_or_quad is False


class TestDivisionProperties:
    def _make_standard_division(self) -> Division:
        """Create a standard division: 1m head, 123m, 456p, concealed 999s, open 111z."""
        parts = [
            DivisionPart.create_head(tile=0, is_concealed=True),
            DivisionPart.create_straight(tile=0, is_concealed=True),
            DivisionPart.create_straight(tile=12, is_concealed=True),
            DivisionPart.create_triple(tile=26, is_concealed=True),
            DivisionPart.create_triple(tile=27, is_concealed=False),
        ]
        return Division(parts=parts, agari_tile=Tile(0), is_opened=True)

    def test_tile_count(self) -> None:
        division = self._make_standard_division()
        tc = division.tile_count
        # 2 (head) + 3 + 3 + 3 + 3 = 14
        assert tc.num_tiles == 14

    def test_num_concealed_triplets(self) -> None:
        division = self._make_standard_division()
        # Only tile=26 triple is concealed triplet_or_quad
        assert division.num_concealed_triplets == 1

    def test_num_concealed_triplets_with_concealed_kan(self) -> None:
        call = Call(
            type=CallTypeEnum.CONCEALED_KAN,
            tiles=[Tile(31), Tile(31), Tile(31), Tile(31)],
            call_idx=0,
        )
        parts = [
            DivisionPart.create_head(tile=0, is_concealed=True),
            DivisionPart.create_triple(tile=9, is_concealed=True),
            DivisionPart.create_triple(tile=18, is_concealed=True),
            DivisionPart.create_straight(tile=0, is_concealed=True),
            DivisionPart.create_from_call(call),
        ]
        division = Division(parts=parts, agari_tile=Tile(0), is_opened=False)
        # 2 concealed triples + 1 concealed kan = 3
        assert division.num_concealed_triplets == 3

    def test_num_quads_zero(self) -> None:
        division = self._make_standard_division()
        assert division.num_quads == 0

    def test_num_quads_with_kans(self) -> None:
        call1 = Call(
            type=CallTypeEnum.CONCEALED_KAN,
            tiles=[Tile(0), Tile(0), Tile(0), Tile(0)],
            call_idx=0,
        )
        call2 = Call(
            type=CallTypeEnum.BIG_MELDED_KAN,
            tiles=[Tile(9), Tile(9), Tile(9), Tile(9)],
            call_idx=1,
        )
        parts = [
            DivisionPart.create_head(tile=27, is_concealed=True),
            DivisionPart.create_from_call(call1),
            DivisionPart.create_from_call(call2),
            DivisionPart.create_straight(tile=18, is_concealed=True),
            DivisionPart.create_triple(tile=31, is_concealed=False),
        ]
        division = Division(parts=parts, agari_tile=Tile(27), is_opened=True)
        assert division.num_quads == 2
