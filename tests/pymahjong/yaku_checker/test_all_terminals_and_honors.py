import pytest

from pymahjong.yaku_checker.all_terminals_and_honors import AllTerminalsAndHonors
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1199m111999p111z1m", True),
        ("11199m111999p111s", True),
        ("11122233344455z", True),
        ("1199m1199p1199s11z", True),
        ("111222333m99p999s", False),
        ("11122233m999p999s", False),
        ("1399m2m,chi123p,cok7777z,chi789s", False),
    ],
)
def test_all_terminals_and_honors(test_input, expected):
    assert_yaku_check(test_input, expected, AllTerminalsAndHonors())
