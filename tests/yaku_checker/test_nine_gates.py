import pytest

from pymahjongutil.yaku_checker.nine_gates import NineGates
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11134556789992s", True),
        ("11113456789992m", True),
        ("11134567882p,pon999p", False),
    ],
)
def test_nine_gates(test_input, expected):
    assert_yaku_check(test_input, expected, NineGates())
