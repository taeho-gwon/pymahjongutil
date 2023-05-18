import pytest

from pymahjong.enum.common import CallTypeEnum
from pymahjong.hand_parser import get_hand_from_code
from pymahjong.schema.call import Call
from pymahjong.schema.hand import Hand
from pymahjong.schema.tile import Tile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123p45699s,chi123s,pon5-55z",
            Hand(
                concealed_tiles=[
                    Tile(9),
                    Tile(10),
                    Tile(11),
                    Tile(21),
                    Tile(22),
                    Tile(23),
                    Tile(26),
                ],
                calls=[
                    Call(
                        type=CallTypeEnum.CHII,
                        tiles=[
                            Tile(18),
                            Tile(19),
                            Tile(20),
                        ],
                        call_idx=0,
                    ),
                    Call(
                        type=CallTypeEnum.PON,
                        tiles=[
                            Tile(31),
                            Tile(31),
                            Tile(31),
                        ],
                        call_idx=1,
                    ),
                ],
                last_tile=Tile(26),
            ),
        ),
        (
            "19m19p19s1234567z",
            Hand(
                concealed_tiles=[
                    Tile(0),
                    Tile(8),
                    Tile(9),
                    Tile(17),
                    Tile(18),
                    Tile(26),
                    Tile(27),
                    Tile(28),
                    Tile(29),
                    Tile(30),
                    Tile(31),
                    Tile(32),
                    Tile(33),
                ],
                calls=[],
            ),
        ),
    ],
)
def test_get_hand_from_code(test_input, expected):
    assert get_hand_from_code(test_input) == expected
