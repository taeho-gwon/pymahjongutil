import pytest

from pymahjong.yaku_checker.yakuman.all_terminals import AllTerminals
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("111999p111999s11m", True),
        ("11m,pon999p,cok1111s,bmk9999s,pon111p", True),
        ("199m1199p1199s11z1m", False),
    ],
)
def test_all_terminals(test_input, expected):
    assert_yaku_check(test_input, expected, AllTerminals())
