import pkgutil
from importlib import import_module

from pymahjong.enum.common import YakuEnum


def snake_to_camel(s: str):
    return "".join(word.title() for word in s.split("_"))


YAKU_DICT = {}

path = import_module(__name__).__path__
module_names = (d[1] for d in pkgutil.iter_modules(path))
for module_name in module_names:
    if module_name == "base_yaku" or module_name == "utils":
        continue

    mod = import_module(__name__ + "." + module_name)
    YAKU_DICT[YakuEnum(module_name.upper())] = getattr(mod, snake_to_camel(module_name))
