import pytest

from pymahjongutil.yaku_checker.three_color_sequences import ThreeColorSequences
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("234m234567p23488s", True),
        ("234m567p23488s,chi234p", True),
        ("111123s123p12399m", True),
        ("234m123456p234s11z", False),
        ("22333m444p555s666z", False),
    ],
)
def test_three_color_sequences(test_input, expected):
    assert_yaku_check(test_input, expected, ThreeColorSequences())
