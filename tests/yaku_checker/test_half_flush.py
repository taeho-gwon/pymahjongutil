import pytest

from pymahjongutil.yaku_checker.half_flush import HalfFlush
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11123456789999s", False),
        ("33345699m,pon111m,smk2222m", False),
        ("22334455667788p", False),
        ("223344556677p11z", True),
        ("33345699m,pon111z,smk2222m", True),
        ("33345699m,pon111z,smk2222p", False),
    ],
)
def test_half_flush(test_input, expected):
    assert_yaku_check(test_input, expected, HalfFlush())
