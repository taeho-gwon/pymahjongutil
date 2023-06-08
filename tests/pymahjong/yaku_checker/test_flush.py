import pytest

from pymahjong.schema.agari_info import AgariInfo
from pymahjong.yaku_checker.flush import Flush
from tests.pymahjong.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("11123456789999s", True),
        ("33345699m,pon111m,smk2222m", True),
        ("22334455667788p", True),
        ("223344556677p11z", False),
        ("33345699m,pon111z,smk2222m", False),
    ],
)
def test_flush(test_input, expected):
    assert_yaku_check(test_input, expected, Flush(), AgariInfo())
