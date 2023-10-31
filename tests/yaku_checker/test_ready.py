import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.ready import Ready
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_ready_hand, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_ready(is_ready_hand, expected):
    agari_info = AgariInfo(is_ready_hand=is_ready_hand)
    assert_yaku_check("123456789m11199p", expected, Ready(), agari_info)
