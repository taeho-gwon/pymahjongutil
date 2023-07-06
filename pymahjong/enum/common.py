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
    SEQUENCE = auto()
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


class YakuEnum(UpperStrEnum):
    READY = auto()
    SELF_DRAW = auto()
    ONE_SHOT = auto()
    DEAD_WALL_DRAW = auto()
    ROBBING_A_QUAD = auto()
    WIN_BY_LAST_DRAW = auto()
    WIN_BY_LAST_DISCARD = auto()
    ALL_SEQUENCES = auto()
    IDENTICAL_SEQUENCES = auto()
    WHITE_DRAGON = auto()
    GREEN_DRAGON = auto()
    RED_DRAGON = auto()
    PLAYER_WIND = auto()
    ROUND_WIND = auto()
    ALL_SIMPLES = auto()

    DOUBLE_READY = auto()
    SEVEN_PAIRS = auto()
    THREE_COLOR_SEQUENCES = auto()
    STRAIGHT = auto()
    ALL_TRIPLETS = auto()
    THREE_CONCEALED_TRIPLETS = auto()
    THREE_COLOR_TRIPLETS = auto()
    THREE_QUADS = auto()
    HALF_OUTSIDE_HAND = auto()
    ALL_TERMINALS_AND_HONORS = auto()
    SMALL_THREE_DRAGONS = auto()

    TWO_SETS_OF_IDENTICAL_SEQUENCES = auto()
    PURE_OUTSIDE_HAND = auto()
    HALF_FLUSH = auto()
    FLUSH = auto()

    HEAVENLY_HAND = auto()
    EARTHLY_HAND = auto()
    FOUR_CONCEALED_TRIPLETS = auto()
    THIRTEEN_ORPHANS = auto()
    NINE_GATES = auto()
    ALL_GREENS = auto()
    ALL_HONORS = auto()
    ALL_TERMINALS = auto()
    BIG_THREE_DRAGONS = auto()
    SMALL_FOUR_WINDS = auto()
    BIG_FOUR_WINDS = auto()
    FOUR_QUADS = auto()


class WindEnum(UpperStrEnum):
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTH = auto()
