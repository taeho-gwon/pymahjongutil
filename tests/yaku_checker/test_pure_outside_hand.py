import pytest

from pymahjongutil.yaku_checker.pure_outside_hand import PureOutsideHand
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("12399m,chi123p,cok7777z,chi789s", False),
        ("11199m111999p111z", False),
        ("11199m111999p111s", True),
        ("111222333m99p999s", True),
        ("11122233m999p999s", False),
    ],
)
def test_pure_outside_hand(test_input, expected):
    assert_yaku_check(test_input, expected, PureOutsideHand())
