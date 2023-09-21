import pytest

from pymahjongutil.yaku_checker.small_three_dragons import SmallThreeDragons
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("123999m55666777z", True),
        ("888s66z,pon222m,cok5555z,bmk7777z", True),
        ("12399m555666777z", False),
        ("22m888s,pon555z,cok6666z,bmk7777z", False),
        ("11223399m556677z", False),
    ],
)
def test_small_three_dragons(test_input, expected):
    assert_yaku_check(test_input, expected, SmallThreeDragons())
