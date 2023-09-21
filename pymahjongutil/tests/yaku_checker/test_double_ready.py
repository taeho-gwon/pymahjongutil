import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.double_ready import DoubleReady
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_double_ready_hand, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_double_ready(is_double_ready_hand, expected):
    agari_info = AgariInfo(is_double_ready_hand=is_double_ready_hand)
    assert_yaku_check("123456789m11199p", expected, DoubleReady(), agari_info)
