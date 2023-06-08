import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.three_concealed_triplets import ThreeConcealedTriplets
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22444666788892m", True),
        ("22444666888992m", False),
        ("24446668889992m", False),
    ],
)
def test_three_concealed_triplets_tsumo(test_input, expected):
    assert_yaku_check(
        test_input, expected, ThreeConcealedTriplets(), AgariInfo(is_tsumo_agari=True)
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22444666788892m", False),
        ("22444666888992m", True),
        ("24446668889992m", False),
    ],
)
def test_three_concealed_triplets_ron(test_input, expected):
    assert_yaku_check(
        test_input, expected, ThreeConcealedTriplets(), AgariInfo(is_tsumo_agari=False)
    )
