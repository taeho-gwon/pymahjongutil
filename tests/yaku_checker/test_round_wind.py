import pytest

from pymahjongutil.enum.common import WindEnum
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.round_wind import RoundWind
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, round_wind, expected",
    [
        ("22789m456s123p111z", WindEnum.EAST, True),
        ("22789m456s123p222z", WindEnum.EAST, False),
        ("22789m456s123p333z", WindEnum.EAST, False),
        ("22789m456s123p444z", WindEnum.EAST, False),
        ("22789m456s123p444z", WindEnum.NORTH, True),
    ],
)
def test_round_wind(test_input, round_wind, expected):
    assert_yaku_check(
        test_input, expected, RoundWind(), AgariInfo(round_wind=round_wind)
    )
