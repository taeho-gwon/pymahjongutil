import pytest

from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.yaku_checker.four_concealed_triplets import FourConcealedTriplets
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22444666788892m", False),
        ("22444666888992m", True),
        ("24446668889992m", True),
    ],
)
def test_four_concealed_triplets_tsumo(test_input, expected):
    assert_yaku_check(
        test_input, expected, FourConcealedTriplets(), AgariInfo(is_tsumo_agari=True)
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("22444666788892m", False),
        ("22444666888992m", False),
        ("24446668889992m", True),
    ],
)
def test_four_concealed_triplets_ron(test_input, expected):
    assert_yaku_check(
        test_input, expected, FourConcealedTriplets(), AgariInfo(is_tsumo_agari=False)
    )
