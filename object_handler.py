from constants import *
from obstacle import Obstacle
from random import *


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.obstacle_list = []
        self.types = [0, 1, 2]#, 3]  # running enenmy, ball, heart, coin
        self.weights = OBSTACLES_WEIGHTS
        
    def update(self):
        [obstacle.update() for obstacle in self.obstacle_list]

    def remove_obstacle(self):
        del self.obstacle_list[0]

    def closest_enemy(self) -> Obstacle:
        return self.obstacle_list[0]

    def spawn_obstacle(self):
        y = PLAYER_LEFT_END + random() + random()
        while y >= PLAYER_RIGHT_END:
            y = PLAYER_LEFT_END + random() + random()
        x = self.game.player.x + 25 + y
        type = choices(self.types, self.weights)[0]
        obstacle = Obstacle(x, y, type, self.game)
        self.obstacle_list.append(obstacle)
        
    def spawn_coin(self):
        y = PLAYER_LEFT_END + random() + random()
        while y >= PLAYER_RIGHT_END:
            y = PLAYER_LEFT_END + random() + random()
        x = self.game.player.x + 25 + y
        obstacle=Obstacle(x,y,3,self.game)
        self.obstacle_list.append(obstacle)
