import pytest

from pymahjongutil.yaku_checker.all_sequences import AllSequences
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("34m445566p67888s2m", True),
        ("66777888m678p77s6m", True),
        ("13m456p22345678s2m", False),
        ("12m456p22345678s3m", False),
        ("89m456p22345678s7m", False),
        ("2333m444p555s666z2m", False),
        ("34m445566p678s77z2m", False),
    ],
)
def test_all_sequences(test_input, expected):
    assert_yaku_check(test_input, expected, AllSequences())
