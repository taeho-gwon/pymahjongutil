import pytest

from pymahjong.yaku_checker.two_sets_of_identical_sequences import (
    TwoSetsOfIdenticalSequences,
)
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("223344m445566p88s", True),
        ("666677778888m77s", True),
        ("123m456p22345678s", False),
        ("22333m444p555s666z", False),
    ],
)
def test_two_sets_of_identical_sequences(test_input, expected):
    assert_yaku_check(test_input, expected, TwoSetsOfIdenticalSequences())
