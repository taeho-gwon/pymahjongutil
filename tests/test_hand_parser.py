import pytest

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.hand_parser import get_hand_from_code
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.tile import Tile


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "123p45699s,chi123s,pon5-55z",
            Hand(
                concealed_tiles=[
                    Tile(value=9),
                    Tile(value=10),
                    Tile(value=11),
                    Tile(value=21),
                    Tile(value=22),
                    Tile(value=23),
                    Tile(value=26),
                ],
                calls=[
                    Call(
                        type=CallTypeEnum.CHII,
                        tiles=[
                            Tile(value=18),
                            Tile(value=19),
                            Tile(value=20),
                        ],
                        call_idx=0,
                    ),
                    Call(
                        type=CallTypeEnum.PON,
                        tiles=[
                            Tile(value=31),
                            Tile(value=31),
                            Tile(value=31),
                        ],
                        call_idx=1,
                    ),
                ],
                last_tile=Tile(value=26),
            ),
        ),
        (
            "19m19p19s1234567z",
            Hand(
                concealed_tiles=[
                    Tile(value=0),
                    Tile(value=8),
                    Tile(value=9),
                    Tile(value=17),
                    Tile(value=18),
                    Tile(value=26),
                    Tile(value=27),
                    Tile(value=28),
                    Tile(value=29),
                    Tile(value=30),
                    Tile(value=31),
                    Tile(value=32),
                    Tile(value=33),
                ],
                calls=[],
            ),
        ),
    ],
)
def test_get_hand_from_code(test_input, expected):
    assert get_hand_from_code(test_input) == expected
