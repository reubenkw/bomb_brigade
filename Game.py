import pygame as pg
from Classes.Config import Cfg
from Classes.Map import Map
from Classes.Player import Player
from Classes.Bomb import Bomb
from Classes.TileType import TileType


class Game:
    def __init__(self, name1, name2):
        self.game_over = False
        self.tick = 0
        self.player1 = Player(34, 34, (57, 55, 91), name1)
        self.player2 = Player(29, 29, (255, 128, 128), name2)
        self.map = Map((Cfg.map_x_tiles, Cfg.map_y_tiles))
        self.bombs = []
        self.win = pg.display.set_mode((Cfg.display_x, Cfg.display_y))
        self.outcome = "Tie"
        pg.display.set_caption("Bomb Brigade")
        pg.init()

    def action_interpreter(self, player, action):
        if action == "MOVE_UP":
            player.move_up(self.map)
        elif action == "MOVE_DOWN":
            player.move_down(self.map)
        elif action == "MOVE_LEFT":
            player.move_left(self.map)
        elif action == "MOVE_RIGHT":
            player.move_right(self.map)
        elif action == "HARVEST":
            player.harvest(self.map)
        elif action == "BOMB" and player.bombs > 0:
            player.fitness += Cfg.bombs_fitness_place_reward

            self.bombs.append(Bomb(player.x, player.y, self.tick))
            player.bombs -= 1
            self.map.grid[player.x][player.y] = TileType.tile_bomb
        elif action == "WALL" and self.map.grid[player.x][player.y] not in [TileType.tile_wall, TileType.tile_bomb] \
                and player.walls > 0:
            player.fitness += Cfg.walls_fitness_place_reward

            self.map.grid[player.x][player.y] = TileType.tile_wall
            player.walls -= 1

    def loop(self, p1_action, p2_action):
        self.tick += 1

        if self.tick > 1000:
            self.game_over = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_over = True

        for bomb in self.bombs:
            if bomb.detonation_tick >= self.tick:
                bomb.explode(self.map, (self.player1, self.player2))
                self.bombs.remove(bomb)

        if self.player1.health <= 0 and self.player2.health <= 0:
            print("Both " + str(self.player1.name) + " and " + str(self.player2.name) + " died")
            self.game_over = True
        elif self.player1.health <= 0:
            print(self.player1.name, "died")
            self.outcome = self.player2.name
            self.game_over = True
        elif self.player2.health <= 0:
            print(self.player2.name, "died")
            self.outcome = self.player1.name
            self.game_over = True

        self.action_interpreter(self.player1, p1_action)
        self.action_interpreter(self.player2, p2_action)

        self.map.draw(self.win)
        self.player1.draw(self.win)
        self.player2.draw(self.win)
        pg.display.update()
