class TileType:
    tile_default = 0
    tile_burnt = 1
    tile_amo = 2
    tile_forest = 3
    tile_health = 4
    tile_wall = 5
    tile_bomb = 6

    def __init__(self, color0, name0):
        self.color = color0
        self.name = name0
        self.count = 0
