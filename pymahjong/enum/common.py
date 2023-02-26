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


class DecompositionPartTypeEnum(UpperStrEnum):
    MELD = auto()
    PAIR = auto()
    PCHOW = auto()
