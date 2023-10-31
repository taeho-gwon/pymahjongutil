import pytest

from pymahjongutil.yaku_checker.big_three_dragons import BigThreeDragons
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("12399m555666777z", True),
        ("22m888s,pon555z,cok6666z,bmk7777z", True),
        ("11223399m556677z", False),
    ],
)
def test_big_three_dragons(test_input, expected):
    assert_yaku_check(test_input, expected, BigThreeDragons())
