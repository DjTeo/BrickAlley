from helper import Helper
from sprite_object import *
# from npc import *
from random import *


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.anim_sprite_path = Helper.animated_sprites_dir
        self.sprite_selector = 0
        self.obstacle_type = []
        self.enemies = 0
        self.types = [0, 1, 2, 3]  # running enenmy, ball, heart,
        self.weights = OBSTACLES_WEIGHTS
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}

    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        #πηγα να  κανω tuple list το sprite list αλλα μου φφωναζει για το update οποτε εφτιαξα μια παραλληλη λιστα
        self.sprite_list.append(sprite)
        self.obstacle_type.append(self.sprite_selector)
        self.enemies += 1

    def remove_sprite(self):
        del self.sprite_list[0]
        del self.obstacle_type[0]
        self.enemies -= 1

    def closest_enemy(self):
        return self.sprite_list[0].x, self.sprite_list[0].y

    def spawn_obstacle(self):
        y = PLAYER_LEFT_END + random() + random()
        while y >= PLAYER_RIGHT_END:
            y = PLAYER_LEFT_END + random() + random()
        x = self.game.player.x + 25 + y
        self.sprite_selector = choices(self.types, self.weights)[0]
        if self.sprite_selector == 0:
            self.add_sprite(
                AnimatedSprite(self.game,
                               pos=(x, y),
                               path=self.anim_sprite_path + '/runSprite/1.png',
                               shift=0.25))
        elif self.sprite_selector == 1:
            self.add_sprite(
                AnimatedSprite(self.game,
                               path=self.anim_sprite_path +
                               '/ballSprite/1.png',
                               pos=(x, y),
                               scale=0.4,
                               shift=1.25))
        elif self.sprite_selector == 2:
            self.add_sprite(
                AnimatedSprite(self.game,
                               path=self.anim_sprite_path +
                               '/heartSprite/1.png',
                               pos=(x, y),
                               scale=1.2,
                               shift=0.25))
        elif self.sprite_selector == 3:
            self.add_sprite(
                AnimatedSprite(self.game,
                               path=self.anim_sprite_path +
                               '/coinSprite/1.png',
                               pos=(x, y),
                               scale=0.6,
                               shift=0.55))
