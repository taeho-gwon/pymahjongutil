from __future__ import annotations

from pydantic import BaseModel

from src.enum.common import DecompositionPartType
from src.schema.count import TileCount
from src.schema.tile import Tile, Tiles


class KnowledgeBase(TileCount):
    def can_make_head(self, tile: Tile) -> bool:
        return self.counts[tile] > 0

    def can_make_meld(self, tile: Tile) -> bool:
        if self.counts[tile] >= 2:
            return True
        if self.counts[tile.prev.prev] > 0 and self.counts[tile.prev] > 0:
            return True
        if self.counts[tile.prev] > 0 and self.counts[tile.next] > 0:
            return True
        if self.counts[tile.next] > 0 and self.counts[tile.next.next] > 0:
            return True
        return False

    @property
    def is_containing_head(self):
        return any(count >= 2 for count in self.counts)

    @property
    def is_containing_meld(self):
        if any(count >= 3 for count in self.counts):
            return True

        for tile in Tiles.ALL:
            if (
                self.counts[tile] >= 1
                and self.counts[tile.next] >= 1
                and self.counts[tile.next.next] >= 1
            ):
                return True
        return False


class DecompositionPart(BaseModel):
    tile_count: TileCount
    is_incompletable_pair: bool = False
    type: DecompositionPartType = DecompositionPartType.MELD


class QuasiDecomposition(BaseModel):
    parts: list[DecompositionPart]
    remainder: TileCount

    def append(
        self,
        tile_count: TileCount,
        is_incompletable_pair: bool = False,
        type: DecompositionPartType = DecompositionPartType.MELD,
    ):
        self.parts.append(
            DecompositionPart(
                tile_count=tile_count,
                is_incompletable_pair=is_incompletable_pair,
                type=type,
            )
        )

    def pop(self):
        self.parts.pop()

    @property
    def is_valid(self):
        if len(self.parts) == 4 and all(
            part.type is not DecompositionPartType.PAIR for part in self.parts
        ):
            return False
        return sum(1 for part in self.parts if part.is_incompletable_pair) < 2


class QuasiDecompositionType(BaseModel):
    meld_cnt: int
    pmeld_cnt: int
    head_cnt: int
    incomplete_head_cnt: int
    can_make_head_from_remainder: bool
    can_make_meld_from_remainder: bool
    can_conflict_head_meld: bool

    class Config:
        frozen = True

    def cost(self, knowledge_base: KnowledgeBase):
        ke = knowledge_base.is_containing_head
        km = knowledge_base.is_containing_meld
        if self.head_cnt == 0 and not self.can_make_head_from_remainder and not ke:
            return 100
        if (
            self.meld_cnt + self.pmeld_cnt <= 4
            and not self.can_make_head_from_remainder
            and not self.can_make_meld_from_remainder
            and not ke
            and not km
        ):
            return 100
        if (
            self.meld_cnt + self.pmeld_cnt - self.incomplete_head_cnt
            and not self.can_make_meld_from_remainder
            and not km
        ):
            return 100
        if (
            self.meld_cnt + self.pmeld_cnt <= 3
            and self.head_cnt == 0
            and not ke
            and not km
            and self.can_conflict_head_meld
        ):
            return 100
        if self.meld_cnt + self.pmeld_cnt > 4:
            return 4 - self.meld_cnt
        if self.meld_cnt + self.pmeld_cnt == 4:
            if self.incomplete_head_cnt == 0 and self.can_make_head_from_remainder:
                return 4 - self.meld_cnt + 1
            elif self.head_cnt > 0 and self.can_make_meld_from_remainder:
                return 4 - self.meld_cnt + 1
            else:
                return 4 - self.meld_cnt + 2

        mcost = 2 if self.can_make_meld_from_remainder else 3
        ecost = 1 if self.can_make_head_from_remainder else 2
        if self.incomplete_head_cnt == 1:
            return self.pmeld_cnt - 1 + mcost * (4 - self.pmeld_cnt - self.meld_cnt + 1)
        elif self.head_cnt == 0:
            return (
                self.pmeld_cnt
                + mcost * (4 - self.pmeld_cnt - self.meld_cnt)
                + ecost
                + (1 if self.can_conflict_head_meld else 0)
            )
        else:
            return min(
                self.pmeld_cnt + mcost * (4 - self.pmeld_cnt - self.meld_cnt),
                self.pmeld_cnt - 1 + mcost * (4 - self.pmeld_cnt - self.meld_cnt + 1),
            )

    @staticmethod
    def create_from_qdcmp(
        knowledge_base: KnowledgeBase, qdcmp: QuasiDecomposition
    ) -> QuasiDecompositionType:
        meld_cnt, pmeld_cnt, head_cnt, incomplete_head_cnt = 0, 0, 0, 0

        for part in qdcmp.parts:
            if part.type == DecompositionPartType.MELD:
                meld_cnt += 1
            elif part.type == DecompositionPartType.PCHOW:
                pmeld_cnt += 1
            elif part.is_incompletable_pair:
                head_cnt += 1
                incomplete_head_cnt += 1
            else:
                head_cnt += 1
                pmeld_cnt += 1

        return QuasiDecompositionType(
            meld_cnt=meld_cnt,
            pmeld_cnt=pmeld_cnt,
            head_cnt=head_cnt,
            incomplete_head_cnt=incomplete_head_cnt,
            can_make_head_from_remainder=any(
                knowledge_base.can_make_head(tile)
                for tile in Tiles.ALL
                if qdcmp.remainder[tile] > 0
            ),
            can_make_meld_from_remainder=any(
                knowledge_base.can_make_meld(tile)
                for tile in Tiles.ALL
                if qdcmp.remainder[tile] > 0
            ),
            can_conflict_head_meld=False,
        )

    def __add__(self, other: QuasiDecompositionType) -> QuasiDecompositionType:
        can_conflict_head_meld = (
            self.can_conflict_head_meld
            and not other.can_make_head_from_remainder
            and not other.can_make_meld_from_remainder
        ) or (
            other.can_conflict_head_meld
            and not self.can_make_head_from_remainder
            and not self.can_make_meld_from_remainder
        )

        return QuasiDecompositionType(
            meld_cnt=self.meld_cnt + other.meld_cnt,
            pmeld_cnt=self.pmeld_cnt + other.pmeld_cnt,
            head_cnt=self.head_cnt + other.head_cnt,
            incomplete_head_cnt=self.incomplete_head_cnt + other.incomplete_head_cnt,
            can_make_head_from_remainder=self.can_make_head_from_remainder
            or other.can_make_head_from_remainder,
            can_make_meld_from_remainder=self.can_make_meld_from_remainder
            or other.can_make_meld_from_remainder,
            can_conflict_head_meld=can_conflict_head_meld,
        )
