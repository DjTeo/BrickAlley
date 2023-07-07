from constants import *
from obstacle import Obstacle
from random import *


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.obstacle_list: list(Obstacle) = []
        self.types = [0, 1, 2, 3]  # running enenmy, ball, heart, coin
        self.weights = OBSTACLES_WEIGHTS

    def update(self):
        [obstacle.sprite.update() for obstacle in self.obstacle_list]

    def remove_obstacle(self):
        del self.obstacle_list[0]

    def closest_enemy(self):
        return self.obstacle_list[0].x, self.obstacle_list[0].y

    def spawn_obstacle(self):
        y = PLAYER_LEFT_END + random() + random()
        while y >= PLAYER_RIGHT_END:
            y = PLAYER_LEFT_END + random() + random()
        x = self.game.player.x + 25 + y
        type = choices(self.types, self.weights)[0]
        obstacle = Obstacle(x, y, type, self.game)
        self.obstacle_list.append(obstacle)
