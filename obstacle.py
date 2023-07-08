from constants import *
from helper import Helper
from sprite_object import *


class Obstacle:

    def __init__(self, x, y, type: int, game):
        self.x = x
        self.y = y
        self.type = type
        self.game = game
        self.obstacle_speed = 0.1
        if self.type == 0:
            self.size = 0.2
            self.sprite = AnimatedSprite(self.game,
                                         pos=(x, y),
                                         path=Helper.animated_sprites_dir +
                                         '/runSprite/1.png',
                                         shift=0.25)
        elif self.type == 1:
            self.size = 0.15
            self.sprite = AnimatedSprite(self.game,
                                         path=Helper.animated_sprites_dir +
                                         '/ballSprite/1.png',
                                         pos=(x, y),
                                         scale=0.4,
                                         shift=1.25)
        elif self.type == 2:
            self.size = 0.1
            self.sprite = AnimatedSprite(self.game,
                                         path=Helper.animated_sprites_dir +
                                         '/heartSprite/1.png',
                                         pos=(x, y),
                                         scale=1.2,
                                         shift=0.25)
        elif self.type == 3:
            self.size = 0.1
            self.sprite = AnimatedSprite(self.game,
                                         path=Helper.animated_sprites_dir +
                                         '/coinSprite/1.png',
                                         pos=(x, y),
                                         scale=0.6,
                                         shift=0.55)

    def update(self):
        self.movement()
        self.sprite.update(self.x, self.y)

    def movement(self):
        self.x -= self.obstacle_speed