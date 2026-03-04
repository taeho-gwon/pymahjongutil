from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.yaku_rule import YakuRule


class TestYakuRuleGetHan:
    def test_get_han_concealed(self) -> None:
        rule = YakuRule(yaku=YakuEnum.FLUSH, han_normal=6, han_opened=5)
        assert rule.get_han(is_opened=False) == 6

    def test_get_han_opened(self) -> None:
        rule = YakuRule(yaku=YakuEnum.FLUSH, han_normal=6, han_opened=5)
        assert rule.get_han(is_opened=True) == 5

    def test_get_han_zero_when_opened(self) -> None:
        rule = YakuRule(yaku=YakuEnum.READY, han_normal=1, han_opened=0)
        assert rule.get_han(is_opened=True) == 0

    def test_get_han_same_for_both(self) -> None:
        rule = YakuRule(yaku=YakuEnum.ALL_TRIPLETS, han_normal=2, han_opened=2)
        assert rule.get_han(is_opened=False) == 2
        assert rule.get_han(is_opened=True) == 2
