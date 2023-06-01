import pytest

from pymahjong.yaku_checker.yakuman.all_greens import AllGreens
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22334466888s666z", True),
        ("22233344466688s", True),
        ("2344666688s666z5s", False),
    ],
)
def test_all_greens(test_input, expected):
    assert_yaku_check(test_input, expected, AllGreens())
