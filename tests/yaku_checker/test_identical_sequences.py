import pytest

from pymahjongutil.yaku_checker.identical_sequences import IdenticalSequences
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("112233789m11199p", True),
        ("11122334789m999p", False),
        ("11112233789m999p", True),
        ("11123789m999p,chi123m", True),
    ],
)
def test_identical_sequences(test_input, expected):
    assert_yaku_check(test_input, expected, IdenticalSequences())
