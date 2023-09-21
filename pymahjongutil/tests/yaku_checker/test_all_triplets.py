import pytest

from pymahjongutil.yaku_checker.all_triplets import AllTriplets
from tests.yaku_checker.utils import assert_yaku_check


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2244466688899m2m", True),
        ("22m,pon333p,bmk5555p,cok1111z,smk3333z", True),
        ("22223333444455m", False),
        ("22334455m111z,chi234m", False),
    ],
)
def test_all_triplets(test_input, expected):
    assert_yaku_check(test_input, expected, AllTriplets())
