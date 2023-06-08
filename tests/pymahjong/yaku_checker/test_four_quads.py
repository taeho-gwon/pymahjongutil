import pytest

from pymahjong.yaku_checker.four_quads import FourQuads
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11z,cok2222z,smk3333z,cok4444z,bmk5555z", True),
        ("11z,pon222z,smk3333z,cok4444z,bmk5555z", False),
    ],
)
def test_four_quads(test_input, expected):
    assert_yaku_check(test_input, expected, FourQuads())
