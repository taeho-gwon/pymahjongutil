from copy import deepcopy
from typing import Iterable

from pymahjongutil.hand_checker.hand_checker import HandChecker
from pymahjongutil.schema.count import TileCount
from pymahjongutil.schema.division import Division, DivisionPart
from pymahjongutil.schema.tile import Tile, Tiles


class NormalChecker(HandChecker):
    def calculate_deficiency(self) -> int:
        concealed_count = self.hand_count.concealed_count.copy(deep=True)
        num_call = len(self.hand_count.call_counts)
        best_deficiency = [10]

        for t in (tile for tile in range(34) if concealed_count[tile] >= 2):
            concealed_count[t] -= 2
            self._erase_complete_set(0, concealed_count, num_call, 1, best_deficiency)
            concealed_count[t] += 2

        self._erase_complete_set(0, concealed_count, num_call, 0, best_deficiency)

        return best_deficiency[0]

    def _erase_complete_set(
        self,
        index: int,
        concealed_count: TileCount,
        num_complete_sets: int,
        num_pair: int,
        best_deficiency,
    ):
        index = concealed_count.find_earliest_nonzero_index(index)
        if index >= len(Tiles.DEFAULTS):
            self._erase_partial_set(
                0, concealed_count, num_complete_sets, 0, num_pair, best_deficiency
            )
            return

        if concealed_count[index] >= 3:
            concealed_count[index] -= 3
            self._erase_complete_set(
                index, concealed_count, num_complete_sets + 1, num_pair, best_deficiency
            )
            concealed_count[index] += 3

        if (
            index in Tiles.STRAIGHT_STARTS
            and concealed_count[index + 1] > 0
            and concealed_count[index + 2] > 0
        ):
            concealed_count[index : index + 3] -= 1
            self._erase_complete_set(
                index, concealed_count, num_complete_sets + 1, num_pair, best_deficiency
            )
            concealed_count[index : index + 3] += 1

        self._erase_complete_set(
            index + 1, concealed_count, num_complete_sets, num_pair, best_deficiency
        )

    def _erase_partial_set(
        self,
        index: int,
        concealed_count: TileCount,
        num_complete_sets: int,
        num_partial_sets: int,
        num_pair: int,
        best_deficiency,
    ):
        index = concealed_count.find_earliest_nonzero_index(index)
        if index >= 34:
            can_make_pair = num_pair == 1 or any(
                concealed_count[tile] == 1 and self.total_count[tile] < 4
                for tile in range(34)
            )
            current_deficiency = (
                10
                - (num_complete_sets * 2)
                - num_partial_sets
                - num_pair
                - can_make_pair
            )
            if current_deficiency < best_deficiency[0]:
                best_deficiency[0] = current_deficiency
            return

        if num_complete_sets + num_partial_sets < 4:
            if concealed_count[index] == 2 and self.total_count[index] < 4:
                concealed_count[index] -= 2
                self._erase_partial_set(
                    index,
                    concealed_count,
                    num_complete_sets,
                    num_partial_sets + 1,
                    num_pair,
                    best_deficiency,
                )
                concealed_count[index] += 2

            if (
                index in Tiles.PARTIAL_STRAIGHT_STARTS
                and concealed_count[index + 1] > 0
                and (
                    self.total_count[index + 2] < 4
                    or (index % 9 > 0 and self.total_count[index - 1] < 4)
                )
            ):
                concealed_count[index : index + 2] -= 1
                self._erase_partial_set(
                    index,
                    concealed_count,
                    num_complete_sets,
                    num_partial_sets + 1,
                    num_pair,
                    best_deficiency,
                )
                concealed_count[index : index + 2] += 1

            if (
                index in Tiles.STRAIGHT_STARTS
                and concealed_count[index + 2] > 0
                and self.total_count[index + 1] < 4
            ):
                concealed_count[index : index + 3 : 2] -= 1
                self._erase_partial_set(
                    index,
                    concealed_count,
                    num_complete_sets,
                    num_partial_sets + 1,
                    num_pair,
                    best_deficiency,
                )
                concealed_count[index : index + 3 : 2] += 1

        self._erase_partial_set(
            index + 1,
            concealed_count,
            num_complete_sets,
            num_partial_sets,
            num_pair,
            best_deficiency,
        )

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        call_parts = [DivisionPart.create_from_call(call) for call in self.hand.calls]
        return [
            Division(
                parts=concealed_parts + call_parts,
                agari_tile=agari_tile,
                is_opened=self.hand.is_opened,
            )
            for concealed_parts in self._calculate_iter_concealed_parts(
                agari_tile, is_tsumo_agari
            )
        ]

    def _calculate_iter_concealed_parts(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> Iterable[list[DivisionPart]]:
        head_candidates = (
            head
            for head in Tiles.DEFAULTS
            if self.hand_count.concealed_count[head] >= 2
        )
        tile_counts = deepcopy(self.hand_count.concealed_count)
        for head in head_candidates:
            tile_counts[head] -= 2
            body_divisions_iter = self._calculate_iter_body_divisions(tile_counts)
            for body_parts in body_divisions_iter:
                yield from self._create_divisions_from_parts(
                    head, body_parts, agari_tile, is_tsumo_agari
                )
            tile_counts[head] += 2

    def _calculate_iter_body_divisions(
        self,
        tile_counts: TileCount,
        idx: int = 0,
        body_divisions: list[DivisionPart] | None = None,
    ) -> Iterable[list[DivisionPart]]:
        if body_divisions is None:
            body_divisions = []
            idx = 0

        while idx < len(Tiles.DEFAULTS) and tile_counts.counts[idx] == 0:
            idx += 1

        if idx >= len(Tiles.DEFAULTS):
            yield body_divisions[:]
            return

        if tile_counts.counts[idx] >= 3:
            tile_counts.counts[idx] -= 3
            body_divisions.append(DivisionPart.create_triple(idx, is_concealed=True))
            yield from self._calculate_iter_body_divisions(
                tile_counts, idx, body_divisions
            )
            body_divisions.pop()
            tile_counts.counts[idx] += 3

        if idx < 27 and idx % 9 < 7:
            straight_count = tile_counts.counts[idx]
            if min(tile_counts.counts[idx : idx + 3]) != straight_count:
                return

            tile_counts.counts[idx] -= straight_count
            tile_counts.counts[idx + 1] -= straight_count
            tile_counts.counts[idx + 2] -= straight_count

            for _ in range(straight_count):
                body_divisions.append(
                    DivisionPart.create_straight(idx, is_concealed=True)
                )
            yield from self._calculate_iter_body_divisions(
                tile_counts, idx, body_divisions
            )
            for _ in range(straight_count):
                body_divisions.pop()

            tile_counts.counts[idx] += straight_count
            tile_counts.counts[idx + 1] += straight_count
            tile_counts.counts[idx + 2] += straight_count

    def _create_divisions_from_parts(
        self,
        head_idx: int,
        body_parts: list[DivisionPart],
        agari_tile: Tile,
        is_tsumo_agari: bool,
    ) -> Iterable[list[DivisionPart]]:
        if head_idx == agari_tile.value:
            yield [DivisionPart.create_head(head_idx, is_tsumo_agari)] + body_parts[:]
        for idx, body_part in enumerate(body_parts):
            if body_part.counts[agari_tile.value] > 0:
                new_divisions = (
                    [deepcopy(body_part)]
                    + body_parts[:idx]
                    + body_parts[idx + 1 :]
                    + [DivisionPart.create_head(head_idx, True)]
                )
                new_divisions[0].is_concealed = is_tsumo_agari
                yield new_divisions
