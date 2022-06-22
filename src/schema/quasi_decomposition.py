from __future__ import annotations

from pydantic import BaseModel

from src.schema.tile import Tile


class DecompositionPart(BaseModel):
    tiles: list[Tile]


class QuasiDecomposition(BaseModel):
    parts: list[DecompositionPart]


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

    def cost(self, ke, km):
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
    def create_from_qdcmp(qdcmp: QuasiDecomposition):
        return QuasiDecompositionType(
            meld_cnt=0,
            pmeld_cnt=0,
            head_cnt=0,
            incomplete_head_cnt=0,
            can_make_head_from_remainder=True,
            can_make_meld_from_remainder=True,
            can_conflict_head_meld=True,
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
