from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.schema.yaku_rule import YakuRule
from pymahjongutil.yaku_checker import YAKU_DICT


class RiichiDefaultRule:
    def __init__(self):
        yaku_info_dict: dict[YakuEnum, tuple[int, int, bool, list[YakuEnum]]] = {
            YakuEnum.READY: (1, 0, False, []),
            YakuEnum.SELF_DRAW: (
                1,
                0,
                False,
                [YakuEnum.HEAVENLY_HAND, YakuEnum.EARTHLY_HAND],
            ),
            YakuEnum.ONE_SHOT: (1, 0, False, []),
            YakuEnum.DEAD_WALL_DRAW: (1, 1, False, []),
            YakuEnum.ROBBING_A_QUAD: (1, 1, False, []),
            YakuEnum.WIN_BY_LAST_DRAW: (1, 1, False, []),
            YakuEnum.WIN_BY_LAST_DISCARD: (1, 1, False, []),
            YakuEnum.ALL_SEQUENCES: (1, 0, False, []),
            YakuEnum.IDENTICAL_SEQUENCES: (
                1,
                0,
                False,
                [YakuEnum.TWO_SETS_OF_IDENTICAL_SEQUENCES],
            ),
            YakuEnum.WHITE_DRAGON: (1, 1, False, [YakuEnum.BIG_THREE_DRAGONS]),
            YakuEnum.GREEN_DRAGON: (1, 1, False, [YakuEnum.BIG_THREE_DRAGONS]),
            YakuEnum.RED_DRAGON: (1, 1, False, [YakuEnum.BIG_THREE_DRAGONS]),
            YakuEnum.PLAYER_WIND: (1, 1, False, [YakuEnum.BIG_FOUR_WINDS]),
            YakuEnum.ROUND_WIND: (1, 1, False, [YakuEnum.BIG_FOUR_WINDS]),
            YakuEnum.ALL_SIMPLES: (1, 1, False, []),
            YakuEnum.DOUBLE_READY: (2, 0, False, []),
            YakuEnum.SEVEN_PAIRS: (2, 0, False, []),
            YakuEnum.THREE_COLOR_SEQUENCES: (2, 1, False, []),
            YakuEnum.STRAIGHT: (2, 1, False, []),
            YakuEnum.ALL_TRIPLETS: (
                2,
                2,
                False,
                [
                    YakuEnum.FOUR_CONCEALED_TRIPLETS,
                    YakuEnum.BIG_FOUR_WINDS,
                    YakuEnum.FOUR_QUADS,
                ],
            ),
            YakuEnum.THREE_CONCEALED_TRIPLETS: (
                2,
                2,
                False,
                [YakuEnum.FOUR_CONCEALED_TRIPLETS],
            ),
            YakuEnum.THREE_COLOR_TRIPLETS: (2, 2, False, []),
            YakuEnum.THREE_QUADS: (2, 2, False, [YakuEnum.FOUR_QUADS]),
            YakuEnum.HALF_OUTSIDE_HAND: (
                2,
                1,
                False,
                [YakuEnum.ALL_TERMINALS_AND_HONORS, YakuEnum.PURE_OUTSIDE_HAND],
            ),
            YakuEnum.ALL_TERMINALS_AND_HONORS: (
                2,
                2,
                False,
                [
                    YakuEnum.THIRTEEN_ORPHANS,
                    YakuEnum.ALL_TERMINALS,
                    YakuEnum.ALL_HONORS,
                ],
            ),
            YakuEnum.SMALL_THREE_DRAGONS: (2, 2, False, []),
            YakuEnum.TWO_SETS_OF_IDENTICAL_SEQUENCES: (3, 0, False, []),
            YakuEnum.PURE_OUTSIDE_HAND: (3, 2, False, [YakuEnum.ALL_TERMINALS]),
            YakuEnum.HALF_FLUSH: (3, 2, False, [YakuEnum.FLUSH, YakuEnum.ALL_GREENS]),
            YakuEnum.FLUSH: (6, 5, False, [YakuEnum.NINE_GATES]),
            YakuEnum.HEAVENLY_HAND: (13, 0, True, []),
            YakuEnum.EARTHLY_HAND: (13, 0, True, []),
            YakuEnum.FOUR_CONCEALED_TRIPLETS: (13, 0, True, []),
            YakuEnum.THIRTEEN_ORPHANS: (13, 0, True, []),
            YakuEnum.NINE_GATES: (13, 0, True, []),
            YakuEnum.ALL_GREENS: (13, 13, True, []),
            YakuEnum.ALL_HONORS: (13, 13, True, []),
            YakuEnum.ALL_TERMINALS: (13, 13, True, []),
            YakuEnum.BIG_THREE_DRAGONS: (13, 13, True, []),
            YakuEnum.SMALL_FOUR_WINDS: (13, 13, True, []),
            YakuEnum.BIG_FOUR_WINDS: (13, 13, True, []),
            YakuEnum.FOUR_QUADS: (13, 13, True, []),
        }

        self.yaku_rule_dict: dict[YakuEnum, YakuRule] = {
            yaku: YakuRule(
                han_normal=yaku_info[0],
                han_opened=yaku_info[1],
                is_yakuman=yaku_info[2],
                high_yakus=yaku_info[3],
                checker=YAKU_DICT[yaku](),
            )
            for yaku, yaku_info in yaku_info_dict.items()
        }
