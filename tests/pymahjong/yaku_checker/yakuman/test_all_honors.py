import pytest

from pymahjong.yaku_checker.yakuman.all_honors import AllHonors
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11122233344455z", True),
        ("22z,pon111z,cok3333z,bmk5555z,pon777z", True),
        ("11223344556677z", True),
        ("11m223344556677z", False),
        ("111222333444z11m", False),
    ],
)
def test_all_honors(test_input, expected):
    assert_yaku_check(test_input, expected, AllHonors())
