from Classes.Config import Cfg


expRad = [
    (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4),
    (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3),
    (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
    (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
    (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
    (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1),
    (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2),
    (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3),
    (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4)
]


class Bomb:
    def __init__(self, x0, y0, crnt_tick):
        self.detonation_tick = crnt_tick + Cfg.bomb_delay
        self.x = x0
        self.y = y0

    def explode(self, tile_map, players):
        for square in expRad:
            xSquare, ySquare = square
            xSquare += self.x
            ySquare += self.y
            if tile_map.width > xSquare >= 0 and tile_map.height > ySquare >= 0:
                tile_map.tileTypes[tile_map.grid[xSquare][ySquare]].count -= 1
                tile_map.grid[xSquare][ySquare] = 1
                tile_map.tileTypes[1].count += 1
                for player in players:
                    if player.x == xSquare and player.y == ySquare:
                        player.health -= 1
