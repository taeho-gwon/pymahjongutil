import pytest

from pymahjongutil.yaku_checker.three_quads import ThreeQuads
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11z,cok2222z,smk3333z,cok4444z,bmk5555z", False),
        ("11z,pon222z,smk3333z,cok4444z,bmk5555z", True),
    ],
)
def test_three_quads(test_input, expected):
    assert_yaku_check(test_input, expected, ThreeQuads())
