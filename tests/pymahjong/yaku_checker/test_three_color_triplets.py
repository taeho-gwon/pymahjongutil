import pytest

from pymahjong.yaku_checker.three_color_triplets import ThreeColorTriplets
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("222m222p22278999s", True),
        ("222m11z,cok2222p,pon222s,chi123s", True),
        ("22234m222p222333s", False),
        ("222m222p333s22233z", False),
    ],
)
def test_three_color_triplets(test_input, expected):
    assert_yaku_check(test_input, expected, ThreeColorTriplets())
