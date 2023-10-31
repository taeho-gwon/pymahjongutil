import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.win_by_last_discard import WinByLastDiscard
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_last_discard, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_win_by_last_discard(is_last_discard, expected):
    agari_info = AgariInfo(is_last_discard=is_last_discard)
    assert_yaku_check("123456789m11199p", expected, WinByLastDiscard(), agari_info)
