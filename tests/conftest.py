import pytest

from pymahjongutil.hand_parser import get_hand_from_code
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.hand import Hand


@pytest.fixture
def default_agari_info() -> AgariInfo:
    return AgariInfo()


@pytest.fixture
def make_hand() -> type:
    class HandFactory:
        @staticmethod
        def from_code(code: str) -> Hand:
            return get_hand_from_code(code)

    return HandFactory
