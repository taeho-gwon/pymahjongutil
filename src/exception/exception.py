class TileInputError(Exception):
    def __init__(self, tile_code: str):
        self.tile_code = tile_code

    def __str__(self):
        return self.tile_code + "is not a valid tile_code"
