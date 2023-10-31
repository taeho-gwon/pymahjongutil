import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.one_shot import OneShot
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_one_shot, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_ready(is_one_shot, expected):
    agari_info = AgariInfo(is_one_shot=is_one_shot)
    assert_yaku_check("123456789m11199p", expected, OneShot(), agari_info)
