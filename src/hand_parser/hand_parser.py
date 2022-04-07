import re
from itertools import chain
from typing import Optional

from src.enum.common import CallType, TileType
from src.exception.exception import TileInputError
from src.schema.call import Call
from src.schema.hand import Hand
from src.schema.tile import TILE_TYPE_CNT, Tile


def get_hand_from_code(code: str) -> Hand:
    tiles_code, *call_codes = code.split(",")
    tiles = get_tiles_from_code(tiles_code)
    calls = [get_call_from_code(call_code) for call_code in call_codes]
    last_tile: Optional[Tile] = None

    if len(tiles) % 3 == 2:
        *tiles, last_tile = tiles

    return Hand(concealed_tiles=tiles, calls=calls, last_tile=last_tile)


def get_tiles_from_code(code: str) -> list[Tile]:
    pattern = re.compile("([1-9]+)([mpsz])")
    matches = pattern.findall(code)
    if "".join([x + y for (x, y) in matches]) != code:
        raise TileInputError(code)

    return list(
        chain.from_iterable(
            get_tiles_from_match(nums, tile_type_code)
            for nums, tile_type_code in matches
        )
    )


def get_tiles_from_match(nums: str, tile_type_code: str) -> list[Tile]:
    tiles = []
    tile_type_code_mapper = {
        "m": TileType.MAN,
        "p": TileType.PIN,
        "s": TileType.SOU,
        "z": TileType.WIND,
    }

    for num in nums:
        tile_num = int(num)
        if tile_type_code == "z" and tile_num > TILE_TYPE_CNT[TileType.WIND]:
            tile_num -= TILE_TYPE_CNT[TileType.WIND]
            tile_type = TileType.DRAGON
        else:
            tile_type = tile_type_code_mapper[tile_type_code]
        tiles.append(Tile(type=tile_type, value=tile_num))

    return tiles


def get_call_from_code(code: str) -> Call:
    call_type_code_mapper = {
        "chi": CallType.CHII,
        "pon": CallType.PON,
        "cok": CallType.CONCEALED_KAN,
        "bmk": CallType.BIG_MELDED_KAN,
        "smk": CallType.SMALL_MELDED_KAN,
    }

    return Call(
        type=call_type_code_mapper[code[:3]],
        tiles=get_tiles_from_code(code[3:].replace("-", "")),
        call_idx=max(code[3:].find("-"), 0),
    )


if __name__ == "__main__":
    print(get_hand_from_code("123s456p99s"))
