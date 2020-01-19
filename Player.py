import pygame as pg
from Classes.Config import Cfg
from Classes.TileType import TileType


class Player:
    def __init__(self, x0, y0, color0, name0):
        self.health = Cfg.health_start
        self.walls = Cfg.walls_start
        self.bombs = Cfg.bombs_start
        self.x = x0
        self.y = y0
        self.color = color0
        self.name = name0
        self.fitness = 0

    def move_up(self, game_map):
        if self.y > 0 and not game_map.is_wall(self.x, self.y - 1):
            self.y -= 1

    def move_down(self, game_map):
        if self.y < Cfg.map_y_tiles - 1 and not game_map.is_wall(self.x, self.y + 1):
            self.y += 1

    def move_left(self, game_map):
        if self.x > 0 and not game_map.is_wall(self.x - 1, self.y):
            self.x -= 1

    def move_right(self, game_map):
        if self.x < Cfg.map_x_tiles - 1 and not game_map.is_wall(self.x + 1, self.y):
            self.x += 1

    def harvest(self, game_map):
        tile_resource = game_map.grid[self.x][self.y]
        if tile_resource == TileType.tile_amo and self.bombs < Cfg.bombs_max:
            self.fitness += Cfg.bombs_fitness_harvest_reward
            print("Bombs")

            self.bombs += 1
            game_map.grid[self.x][self.y] = TileType.tile_burnt
        elif tile_resource == TileType.tile_forest and self.walls < Cfg.walls_max:
            self.fitness += Cfg.walls_fitness_harvest_reward
            print("Walls")

            self.walls += 1
            game_map.grid[self.x][self.y] = TileType.tile_burnt
        elif tile_resource == TileType.tile_health and self.health < Cfg.health_max:
            self.fitness += Cfg.health_fitness_harvest_reward
            print("Health")

            self.health += 1
            game_map.grid[self.x][self.y] = TileType.tile_burnt

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x * Cfg.map_display_scale, self.y * Cfg.map_display_scale,
                                       Cfg.map_display_scale, Cfg.map_display_scale))

    def print(self):
        print(str(self.name) + "[Health: " + str(self.health) + ", Bombs: "
              + str(self.bombs) + ", Walls: " + str(self.walls) + "]")
