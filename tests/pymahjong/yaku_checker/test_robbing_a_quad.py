import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.robbing_a_quad import RobbingAQuad
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "is_robbing_a_quad, expected",
    [
        (True, True),
        (False, False),
    ],
)
def test_is_robbing_a_quad(is_robbing_a_quad, expected):
    agari_info = AgariInfo(is_robbing_a_quad=is_robbing_a_quad)
    assert_yaku_check("123456789m11199p", expected, RobbingAQuad(), agari_info)
