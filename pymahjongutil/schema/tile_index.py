from pymahjongutil.enum.common import WindEnum


class TileIndex(int):
    """Tile index type representing a valid mahjong tile (0-33)."""

    def __new__(cls, value: int) -> "TileIndex":
        if not (0 <= value <= 33):
            raise ValueError(f"TileIndex must be between 0 and 33, got {value}")
        return super().__new__(cls, value)

    @property
    def is_number_tile(self) -> bool:
        return self < 27

    @property
    def is_honor_tile(self) -> bool:
        return self >= 27

    @property
    def suit_number(self) -> int:
        return self % 9

    @property
    def is_terminal(self) -> bool:
        return self.is_number_tile and self.suit_number in (0, 8)

    @property
    def is_terminal_or_honor(self) -> bool:
        return self.is_terminal or self.is_honor_tile

    @property
    def is_sequence_start(self) -> bool:
        return self.is_number_tile and self.suit_number <= 6

    @property
    def is_side_wait_start(self) -> bool:
        return self.is_number_tile and self.suit_number <= 7

    @property
    def is_left_edge_wait_start(self) -> bool:
        return self.is_number_tile and self.suit_number == 6

    @property
    def is_right_edge_wait_start(self) -> bool:
        return self.is_number_tile and self.suit_number == 0

    @staticmethod
    def create_from_wind_enum(wind: WindEnum) -> "TileIndex":
        wind_base = 27
        wind_offset = {
            WindEnum.EAST: 0,
            WindEnum.SOUTH: 1,
            WindEnum.WEST: 2,
            WindEnum.NORTH: 3,
        }
        return TileIndex(wind_base + wind_offset[wind])
