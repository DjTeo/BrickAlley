from constants import *
from obstacle import Obstacle
from random import *


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.obstacle_list = []
        self.types = [0, 1, 2]  # running enenmy, ball, heart
        self.weights = OBSTACLES_WEIGHTS

    def update(self, delta_time):
        [obstacle.update(delta_time) for obstacle in self.obstacle_list]

    def remove_obstacle(self, obstacle):
        self.obstacle_list.remove(obstacle)

    def closest_enemy(self) -> Obstacle:
        closest = min(self.obstacle_list, key=lambda x: x.x)
        return closest

    def spawn_obstacle(self):
        y = PLAYER_LEFT_END + random() + random()
        while y >= PLAYER_RIGHT_END:
            y = PLAYER_LEFT_END + random() + random()
        x = self.game.player.x + MAX_DEPTH - y
        type = choices(self.types, self.weights)[0]
        obstacle = Obstacle(self.game, x, y, type)
        self.obstacle_list.append(obstacle)

    def spawn_coin(self):
        y = PLAYER_LEFT_END + random() + random()
        while y >= PLAYER_RIGHT_END:
            y = PLAYER_LEFT_END + random() + random()
        x = self.game.player.x + MAX_DEPTH - y
        obstacle = Obstacle(self.game, x, y, 3)
        self.obstacle_list.append(obstacle)
