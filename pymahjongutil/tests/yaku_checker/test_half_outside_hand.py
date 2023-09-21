import pytest

from pymahjongutil.yaku_checker.half_outside_hand import HalfOutsideHand
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("12399m,chi123p,cok7777z,chi789s", True),
        ("11199m111999p111z", True),
        ("11199m111999p111s", False),
        ("111222333m99p999s", False),
        ("11122233m999p999s", False),
    ],
)
def test_half_outside_hand(test_input, expected):
    assert_yaku_check(test_input, expected, HalfOutsideHand())
