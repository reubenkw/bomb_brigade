from Classes.Config import Cfg
from Classes.TileType import TileType
import random
import pygame as pg


class Map:
    def __init__(self, size):
        self.width, self.height = size
        self.grid = [[0 for x in range(64)] for y in range(64)]
        self.tileTypes = [
            TileType((186, 199, 167), "Default"),
            TileType((248, 177, 149), "Burnt"),
            TileType((172, 141, 175), "Amo"),
            TileType((136, 158, 129), "Forest"),
            TileType((245, 176, 203), "Health"),
            TileType((82, 82, 78), "Wall"),
            TileType((244, 96, 96), "Bomb")
        ]
        self.resource_gen(Cfg.bombs_num_deposit, TileType.tile_amo, Cfg.bombs_deposit_size)
        self.resource_gen(Cfg.walls_num_deposit, TileType.tile_forest, Cfg.walls_deposit_size)
        self.resource_gen(Cfg.health_num_deposit, TileType.tile_health, Cfg.health_deposit_size)

    def res_recursive(self, pos, res_val, prob):
        x, y = pos
        self.grid[x][y] = res_val
        if x < self.width - 1 and self.grid[x + 1][y] != res_val and random.random() < prob:
            self.res_recursive((x + 1, y), res_val, prob - 0.01)
        if y < self.height - 1 and self.grid[x][y + 1] != res_val and random.random() < prob:
            self.res_recursive((x, y + 1), res_val, prob - 0.01)
        if x > 0 and self.grid[x - 1][y] != res_val and random.random() < prob:
            self.res_recursive((x - 1, y), res_val, prob - 0.01)
        if y > 0 and self.grid[x][y - 1] != res_val and random.random() < prob:
            self.res_recursive((x, y - 1), res_val, prob - 0.01)

    def resource_gen(self, num_deposits, res_val, prob):
        for _ in range(num_deposits):
            x = random.randint(0, 63)
            y = random.randint(0, 63)
            self.grid[x][y] = res_val
            self.res_recursive((x, y), res_val, prob)

    def draw(self, display):
        for x in range(self.width):
            for y in range(self.height):
                pg.draw.rect(display, self.tileTypes[self.grid[x][y]].color, (x * 10, y * 10, 10, 10))

    def is_wall(self, x, y):
        return self.grid[x][y] == TileType.tile_wall
