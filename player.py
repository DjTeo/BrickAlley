from constants import *
import pygame

from helper import Helper

from object_handler import *

class Player:

    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.forward_speed = PLAYER_STARTING_SPEED
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 700
        self.player_hit = False
        
        self.time_prev = pygame.time.get_ticks()
        self.respawn_timer=2000
        self.player_pain = Helper.PrepareSound("player_pain.wav")
        self.blood_screen = Helper.LoadTexture('blood_texture.png', RES)

        self.left_hand = Helper.LoadSprite('leftHand.png',
                                           (GAME_WIDTH / 4, GAME_HEIGHT / 2))
        self.right_hand = Helper.LoadSprite('rightHand.png',
                                            (GAME_WIDTH / 4, GAME_HEIGHT / 2))

        self.left_hand_up = Helper.LoadSprite(
            'leftHandUp.png', (GAME_WIDTH * 0.4, GAME_HEIGHT * 0.8))
        self.right_hand_up = Helper.LoadSprite(
            'rightHandUp.png', (GAME_WIDTH * 0.4, GAME_HEIGHT * 0.8))
        self.timer = 0
        self.animation_stages = 4
        self.animation_frequency = 180  #this should be related to player speed forward WIP

    def recover_health(self, time_now):
        if self.check_health_recovery_delay(
                time_now) and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self, time_now):
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
    
                
    def check_win(self):
        if self.x >= END_DISTANCE:
            self.game.victory = True
            # pg.time.delay(1500)
            # self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.player_hit = True
        self.player_pain.play()
        if self.health < 1:
            self.game.game_over = True

    def movement(self, delta_time):
        dx, dy = self.forward_speed * delta_time, 0
        speed = PLAYER_SIDEWAYS_SPEED * delta_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dy -= speed
        if keys[pygame.K_d]:
            dy += speed

        self.check_movement(dx, dy, delta_time)

    def check_movement(self, dx, dy, delta_time):
        scale = PLAYER_SIZE_SCALE / delta_time
        # TODO: Check for obstacle collision
        self.x += dx
        if self.y + dy < PLAYER_RIGHT_END and self.y + dy > PLAYER_LEFT_END:
            self.y += dy

    def check_collision(self):
        
        if self.game.object_handler.closest_enemy()[1]<self.y+0.1 and self.game.object_handler.closest_enemy()[1]>self.y-0.1:
            will_be_hit=True
            if will_be_hit and self.game.object_handler.closest_enemy()[0]<=self.x+0.3:
                #Player.get_damage()
                print('hit!')
                self.game.object_handler.remove_sprite()
                will_be_hit=False
        elif self.game.object_handler.closest_enemy()[0]<=self.x+0.3:
            self.game.object_handler.remove_sprite()
            print('missed')
        else:
            will_be_hit=False
        
        
            
        

    def update(self, delta_time):
        time_now = pygame.time.get_ticks()
        self.timer = ((time_now - self.time_prev) //
                      self.animation_frequency) % self.animation_stages
        self.movement(delta_time)
        # self.recover_health(time_now)
        self.check_win()
        
        if self.game.object_handler.sprite_list:
            self.check_collision()
            
        if self.game.object_handler.enemies<5 and self.timer-self.time_prev>self.respawn_timer:
            self.game.object_handler.spawn_obstacle()
            self.time_prev=self.timer
        
        
        

    def draw(self, screen):
        self.timer = pygame.time.get_ticks()  

        if (self.timer//self.animation_frequency) % self.animation_stages == 0:
            screen.blit(self.right_hand,
                        (GAME_WIDTH - GAME_WIDTH / 2, GAME_HEIGHT * 0.65))
            screen.blit(self.left_hand, (GAME_WIDTH / 4, GAME_HEIGHT * 0.65))

        elif (self.timer//self.animation_frequency) % self.animation_stages  == 1:
            screen.blit(self.left_hand_up,
                        (GAME_WIDTH * 0.15, GAME_HEIGHT / 2))

        elif (self.timer//self.animation_frequency) % self.animation_stages == 2:
            screen.blit(self.right_hand,
                        (GAME_WIDTH - GAME_WIDTH / 2, GAME_HEIGHT * 0.65))
            screen.blit(self.left_hand, (GAME_WIDTH / 4, GAME_HEIGHT * 0.65))
        elif (self.timer//self.animation_frequency) % self.animation_stages == 3:
            screen.blit(self.right_hand_up,
                        (GAME_WIDTH * 0.5, GAME_HEIGHT / 2))

        if self.player_hit:
            screen.blit(self.blood_screen, (0, 0))
            self.player_hit = False
            
            
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)