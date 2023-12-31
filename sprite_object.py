import pygame as pg
from constants import *
import os
from collections import deque

#Tutorial
class SpriteObject:

    def __init__(self, game, path, pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        self.time_now = 0

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.dx * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append(
            (self.dx, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta_rays = self.theta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (
                GAME_WIDTH + self.IMAGE_HALF_WIDTH) and self.dx > 0.5:
            self.get_sprite_projection()

    def update(self, x, y, delta_time):
        self.x = x
        self.y = y
        self.get_sprite()
        

#Tutorial
class AnimatedSprite(SpriteObject):

    def __init__(self,
                 game,
                 path,
                 pos=(15.5, 2.5),
                 scale=0.8,
                 shift=0.16,
                 animation_time=0.15):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = 0
        self.animation_trigger = False

    def update(self, x, y, delta_time):
        super().update(x, y, delta_time)
        self.check_animation_time(delta_time)
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]
    
    def check_animation_time(self, delta_time):
        self.animation_trigger = False
        self.time_now += delta_time
        if self.time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = self.time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
