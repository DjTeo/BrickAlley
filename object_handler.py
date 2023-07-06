from sprite_object import *
# from npc import *
from random import choices, randrange
import random


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'assets/sprites/npc/'
        self.static_sprite_path = 'assets/sprites/static_sprites/'
        self.anim_sprite_path = 'assets/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        
        self.sprite_selector=0
        self.obstacle_type=[]
        
        # add_npc = self.add_npc
        self.npc_positions = {}

        # spawn npc
        self.enemies = 0  # npc count
        # self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        # self.spawn_npc()

        # sprite map
        #coords are normalized into squares. if x>3 or x<1 then they go outside the map
        #add_sprite(AnimatedSprite(game))
        #add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        
        #add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'ballSprite/1.png', pos=(14.5, 1.5)))
        # add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        # add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))

        # npc map
        #add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        # add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        # add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        # add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        # add_npc(SoldierNPC(game, pos=(4.0, 29.0)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 14.5)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))
        # add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))
    def spawn_npc(self):
        for i in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]
            pos = x, y = randrange(self.game.map.cols), randrange(
                self.game.map.rows)
            while (pos
                   in self.game.map.world_map) or (pos
                                                   in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(
                    self.game.map.rows)
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def update(self):
        self.npc_positions = {
            npc.map_pos
            for npc in self.npc_list if npc.alive
        }
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        # self.check_win()
        
    def add_npc(self, npc):
        self.npc_list.append(npc)

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
        y = 1.1 + 1.7 * random.random()
        x = self.game.player.x + 20 + y
        self.sprite_selector=random.randrange(0,3)
        if self.sprite_selector==0:
            self.add_sprite(AnimatedSprite((self.game), pos=(x, y)))
        elif self.sprite_selector==1:
            self.add_sprite(AnimatedSprite(self.game, path=self.anim_sprite_path + 'ballSprite/1.png', pos=(x,y),scale=0.4,shift=1.25))
        elif self.sprite_selector==2:
            self.add_sprite(AnimatedSprite(self.game, path=self.anim_sprite_path + 'heartSprite/1.png', pos=(x,y),scale=1.2,shift=0.35))
        

        
        
