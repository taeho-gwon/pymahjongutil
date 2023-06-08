import pytest

from pymahjong.yaku_checker.half_flush import HalfFlush
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11123456789999s", True),
        ("33345699m,pon111m,smk2222m", True),
        ("22334455667788p", True),
        ("223344556677p11z", True),
        ("33345699m,pon111z,smk2222m", True),
        ("33345699m,pon111z,smk2222p", False),
    ],
)
def test_half_flush(test_input, expected):
    assert_yaku_check(test_input, expected, HalfFlush())
