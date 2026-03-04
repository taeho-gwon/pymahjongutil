import pkgutil
from collections.abc import Callable
from importlib import import_module

from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.yaku_checker.base_yaku import BaseYaku


def snake_to_camel(s: str) -> str:
    return "".join(word.title() for word in s.split("_"))


def create_yaku_dict() -> dict[YakuEnum, Callable[[], BaseYaku]]:
    yaku_dict: dict[YakuEnum, Callable[[], BaseYaku]] = {}

    path = import_module(__name__).__path__
    module_names = (d[1] for d in pkgutil.iter_modules(path))
    for module_name in module_names:
        if module_name == "base_yaku" or module_name == "utils":
            continue

        mod = import_module(__name__ + "." + module_name)
        yaku_dict[YakuEnum(module_name.upper())] = getattr(
            mod, snake_to_camel(module_name)
        )

    return yaku_dict
