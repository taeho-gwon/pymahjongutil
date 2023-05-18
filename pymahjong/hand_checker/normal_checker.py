from copy import deepcopy
from typing import Iterable

from pymahjong.hand_checker.hand_checker import HandChecker
from pymahjong.schema.count import TileCount
from pymahjong.schema.division import Division, DivisionPart
from pymahjong.schema.tile import Tile, Tiles


class NormalChecker(HandChecker):
    def calculate_deficiency(self) -> int:
        return (
            self.shanten_calculator.calculate_shanten_for_regular_hand(
                self.hand_count.concealed_count.counts
            )
            + 1
        )

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        call_parts = [DivisionPart.create_from_call(call) for call in self.hand.calls]
        return [
            Division(parts=concealed_parts + call_parts, agari_tile=agari_tile)
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
            body_divisions.append(
                DivisionPart.create_triple(Tile(idx), is_concealed=True)
            )
            yield from self._calculate_iter_body_divisions(
                tile_counts, idx, body_divisions
            )
            body_divisions.pop()
            tile_counts.counts[idx] += 3

        if idx < 27 and idx % 9 < 7:
            straight_count = tile_counts.counts[idx]
            tile_counts.counts[idx] -= straight_count
            tile_counts.counts[idx + 1] -= straight_count
            tile_counts.counts[idx + 2] -= straight_count

            body_divisions.append(
                DivisionPart.create_straight(Tile(idx), is_concealed=True)
            )
            yield from self._calculate_iter_body_divisions(
                tile_counts, idx, body_divisions
            )
            body_divisions.pop()

            tile_counts.counts[idx] += straight_count
            tile_counts.counts[idx + 1] += straight_count
            tile_counts.counts[idx + 2] += straight_count

    def _create_divisions_from_parts(
        self,
        head: Tile,
        body_parts: list[DivisionPart],
        agari_tile: Tile,
        is_tsumo_agari: bool,
    ) -> Iterable[list[DivisionPart]]:
        if head == agari_tile:
            yield [DivisionPart.create_head(head, is_tsumo_agari)] + body_parts[:]
        for idx, body_part in enumerate(body_parts):
            if body_part.counts[agari_tile] > 0:
                new_divisions = (
                    [deepcopy(body_part)] + body_parts[:idx] + body_parts[idx + 1 :]
                )
                new_divisions[0].is_concealed = is_tsumo_agari
                yield new_divisions
