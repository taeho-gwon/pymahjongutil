import pytest

from pymahjongutil.yaku_checker.seven_pairs import SevenPairs
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1199m1199s1199p11z", True),
        ("22334455667788m", True),
        ("12233444m112233p", False),
    ],
)
def test_seven_pairs(test_input, expected):
    assert_yaku_check(test_input, expected, SevenPairs())
