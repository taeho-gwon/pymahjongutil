from enum import Enum, auto


class UpperStrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()


class TileTypeEnum(UpperStrEnum):
    MAN = auto()
    PIN = auto()
    SOU = auto()
    WIND = auto()
    DRAGON = auto()
    ETC = auto()


class CallTypeEnum(UpperStrEnum):
    CHII = auto()
    PON = auto()
    CONCEALED_KAN = auto()
    BIG_MELDED_KAN = auto()
    SMALL_MELDED_KAN = auto()


class DivisionPartTypeEnum(UpperStrEnum):
    HEAD = auto()
    STRAIGHT = auto()
    TRIPLE = auto()
    QUAD = auto()
    THIRTEEN_ORPHANS = auto()


class HandShapeFuReasonEnum(UpperStrEnum):
    SEVEN_PAIRS = auto()
    THIRTEEN_ORPHANS = auto()
    BASE = auto()


class WaitFuReasonEnum(UpperStrEnum):
    HEAD_WAIT = auto()
    CLOSED_WAIT = auto()
    EDGE_WAIT = auto()


class AgariTypeFuReasonEnum(UpperStrEnum):
    CONCEALED_RON = auto()
    TSUMO = auto()
    OPENED_PINFU = auto()


class HeadFuReasonEnum(UpperStrEnum):
    DOUBLE_WIND_HEAD = auto()
    VALUE_HEAD = auto()


class BodyFuReasonEnum(UpperStrEnum):
    OPENED_NORMAL_TRIPLE = auto()
    OPENED_OUTSIDE_TRIPLE = auto()
    CONCEALED_NORMAL_TRIPLE = auto()
    CONCEALED_OUTSIDE_TRIPLE = auto()

    OPENED_NORMAL_QUAD = auto()
    OPENED_OUTSIDE_QUAD = auto()
    CONCEALED_NORMAL_QUAD = auto()
    CONCEALED_OUTSIDE_QUAD = auto()


FuReasonEnum = (
    HandShapeFuReasonEnum
    | WaitFuReasonEnum
    | HeadFuReasonEnum
    | AgariTypeFuReasonEnum
    | BodyFuReasonEnum
)
