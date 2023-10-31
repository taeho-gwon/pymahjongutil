import pytest

from pymahjongutil.yaku_checker.all_simples import AllSimples
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("34m445566p67888s2m", True),
        ("66777888m678p77s6m", True),
        ("13m456p22345678s2m", False),
        ("2333m444p555s666z2m", False),
    ],
)
def test_all_simples(test_input, expected):
    assert_yaku_check(test_input, expected, AllSimples())
