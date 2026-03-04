import re
from itertools import chain

from pymahjongutil.enum.common import CallTypeEnum
from pymahjongutil.schema.call import Call
from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.tile import Tile


def get_hand_from_code(code: str) -> Hand:
    tiles_code, *call_codes = code.split(",")
    tiles = get_tiles_from_code(tiles_code)
    calls = [get_call_from_code(call_code) for call_code in call_codes]
    last_tile: Tile | None = None

    if len(tiles) % 3 == 2:
        *tiles, last_tile = tiles

    return Hand(concealed_tiles=tiles, calls=calls, last_tile=last_tile)


def get_tiles_from_code(code: str) -> list[Tile]:
    pattern = re.compile("([1-9]+)([mpsz])")
    matches = pattern.findall(code)
    if "".join([x + y for (x, y) in matches]) != code:
        raise ValueError(f"{code} is not a valid tile_code")

    return list(
        chain.from_iterable(
            get_tiles_from_match(nums, tile_type_code)
            for nums, tile_type_code in matches
        )
    )


def get_tiles_from_match(nums: str, tile_type_code: str) -> list[Tile]:
    return [get_tile_from_code(num + tile_type_code) for num in nums]


def get_call_from_code(code: str) -> Call:
    call_type_code_mapper = {
        "chi": CallTypeEnum.CHII,
        "pon": CallTypeEnum.PON,
        "cok": CallTypeEnum.CONCEALED_KAN,
        "bmk": CallTypeEnum.BIG_MELDED_KAN,
        "smk": CallTypeEnum.SMALL_MELDED_KAN,
    }

    call_type_code = code[:3]
    if call_type_code not in call_type_code_mapper:
        raise ValueError(f"{call_type_code} is not a valid call type code")

    return Call(
        type=call_type_code_mapper[call_type_code],
        tiles=get_tiles_from_code(code[3:].replace("-", "")),
        call_idx=max(code[3:].find("-"), 0),
    )


def get_tile_from_code(tile_code: str) -> Tile:
    tile_type_code_mapper = {
        "m": 0,
        "p": 9,
        "s": 18,
        "z": 27,
    }
    tile_number = int(tile_code[0])
    tile_type_code = tile_code[1]
    if tile_type_code not in tile_type_code_mapper:
        raise ValueError(f"{tile_type_code} is not a valid tile type code")
    max_number = 7 if tile_type_code == "z" else 9
    if not (1 <= tile_number <= max_number):
        raise ValueError(f"{tile_code} is not a valid tile code")
    return Tile(value=tile_type_code_mapper[tile_type_code] + tile_number - 1)
