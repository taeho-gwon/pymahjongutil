import pytest

from pymahjong.yaku_checker.yakuman.thirteen_orphans import ThirteenOrphans
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("19m19s19p12345677z", True),
        ("99m19s19p1234567z1m", True),
    ],
)
def test_thirteen_orphans(test_input, expected):
    assert_yaku_check(test_input, expected, ThirteenOrphans())
