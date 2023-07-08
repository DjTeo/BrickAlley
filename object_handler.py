from constants import *
from obstacle import Obstacle
from random import *


class ObjectHandler:

    def __init__(self,
                 game,
                 weights=OBSTACLES_WEIGHTS,
                 leftWall=LEFT_WALL,
                 rightWall=RIGHT_WALL,
                 obstacle_timer=OBSTACLES_RESPAWN,
                 obstacle_min_timer=OBSTACLES_MIN_RESPAWN,
                 coin_timer=COIN_RESPAWN,
                 end_distance=END_DISTANCE,
                 endless=False):
        self.game = game
        self.obstacle_list = []
        self.types = [0, 1, 2]  # running enenmy, ball, heart
        self.weights = weights
        self.startingHeartRate = weights[-1]
        self.leftWall = leftWall + 1
        self.rightWall = rightWall
        self.endless = endless
        self.obstacle_time_prev = 0
        self.obstacle_timer = obstacle_timer
        self.obstacle_min_timer = obstacle_min_timer
        self.coin_timer = coin_timer
        self.coin_prev_timer = 0
        self.timer = 0
        self.end_distance = end_distance

    def update(self, delta_time):
        self.timer += delta_time

        [obstacle.update(delta_time) for obstacle in self.obstacle_list]

        self.obstacle_time_prev = self.check_spawn(self.obstacle_time_prev,
                                                   self.obstacle_timer,
                                                   self.spawn_obstacle)
        self.coin_prev_timer = self.check_spawn(self.coin_prev_timer,
                                                self.coin_timer,
                                                self.spawn_coin)

        self.increase_dif(delta_time)

    def remove_obstacle(self, obstacle):
        self.obstacle_list.remove(obstacle)

    def closest_enemy(self) -> Obstacle:
        closest = min(self.obstacle_list, key=lambda x: x.x)
        return closest

    def spawn_obstacle(self):
        if self.endless:
            self.heart_rate_down(int(self.game.player.x))
        y = self.calcualte_y_pos()
        x = self.game.player.x + MAX_DEPTH - y
        type = choices(self.types, self.weights)[0]
        obstacle = Obstacle(self.game, x, y, type)
        self.obstacle_list.append(obstacle)

    def spawn_coin(self):
        y = self.calcualte_y_pos()
        x = self.game.player.x + MAX_DEPTH - y
        obstacle = Obstacle(self.game, x, y, 3)
        self.obstacle_list.append(obstacle)

    def calcualte_y_pos(self):
        y = self.leftWall + 0.1 + random() * (self.rightWall - self.leftWall)
        while y >= self.rightWall - 0.1:
            y = self.leftWall + 0.1 + random() * (self.rightWall -
                                                  self.leftWall)
        return y

    def heart_rate_down(self, distance: int):
        heartDown = distance // ENDLESS_HEART_DECREASE
        heartRate = self.startingHeartRate - heartDown
        if heartRate < 1:
            heartRate = 1 - (heartDown - self.startingHeartRate) * 0.1
        if heartRate <= 0:
            heartRate = 0.1
        self.weights[-1] = heartRate
        # print(self.weights)

    # Spawn object if needed
    def check_spawn(self, time_prev, timer, spawner):
        if self.timer - time_prev > timer and self.end_distance - int(
                self.game.player.x) >= 20:
            spawner()
            return self.timer
        return time_prev

    # DIFFICULTY MOD
    def increase_dif(self, delta_time):
        if self.obstacle_timer > self.obstacle_min_timer:
            self.obstacle_timer -= 0.015 * delta_time
        else:
            self.obstacle_timer = self.obstacle_min_timer