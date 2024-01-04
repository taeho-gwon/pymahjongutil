from dataclasses import dataclass

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.tile import Tile


@dataclass
class Call:
    type: CallTypeEnum
    tiles: list[Tile]
    call_idx: int
