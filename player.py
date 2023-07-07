from constants import *
import pygame
from helper import Helper


class Player:

    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.forward_speed = PLAYER_STARTING_SPEED
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 700
        self.player_hit = False
        self.coins_collected = 0
        self.time_prev = pygame.time.get_ticks()
        self.respawn_timer = OBSTACLES_RESPAWN
        self.player_pain = Helper.PrepareSound("player_pain.wav", 0.75)
        self.collect_sound = Helper.PrepareSound("collect.wav")
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

    def check_win(self):
        if self.x >= END_DISTANCE:
            self.game.victory = True
            # pg.time.delay(1500)
            # self.game.new_game()

    #PLAYER STATS
    def get_damage(self, damage):
        self.health -= damage
        self.player_hit = True
        self.player_pain.play()
        if self.health < 1:
            self.health = 0
            self.game.game_over = True

    def recover_health(self, amount):
        if self.health < 100:
            if self.health + amount > 100:
                self.health = 100
            else:
                self.health += amount

    def total_score(self):
        return int(self.x) + self.coins_collected * COINS_SCORE + self.health

    def movement(self, delta_time):
        dx, dy = self.forward_speed * delta_time, 0
        speed = PLAYER_SIDEWAYS_SPEED * delta_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dy -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dy += speed

        self.check_movement(dx, dy)

    #BORDERS
    def check_movement(self, dx, dy):
        self.x += dx
        if self.y + dy < PLAYER_RIGHT_END and self.y + dy > PLAYER_LEFT_END:
            self.y += dy

    #COLLISIONS
    def check_collision(self):
        closest = self.game.object_handler.closest_enemy()
        if closest.y < self.y + PLAYER_SIZE_SCALE and closest.y > self.y - PLAYER_SIZE_SCALE:
            if closest.x <= self.x + 0.3:
                if closest.type == 0:
                    self.get_damage(5)
                elif closest.type == 1:
                    self.get_damage(15)
                elif closest.type == 2:
                    self.recover_health(5)
                    self.collect_sound.play()
                elif closest.type == 3:
                    self.coins_collected += 1
                    self.collect_sound.play()
                self.game.object_handler.remove_obstacle()
        elif closest.x <= self.x:
            self.game.object_handler.remove_obstacle()

    def update(self, delta_time):
        self.timer = pygame.time.get_ticks()
        self.movement(delta_time)
        self.check_win()
        if self.game.object_handler.obstacle_list:
            self.check_collision()

        if self.timer - self.time_prev > self.respawn_timer:  # and self.game.object_handler.enemies < 5: removed, no point if spawning one at a time
            self.game.object_handler.spawn_obstacle()
            self.time_prev = self.timer

    def draw(self, screen):
        if (self.timer //
                self.animation_frequency) % self.animation_stages == 0:
            screen.blit(self.right_hand,
                        (GAME_WIDTH - GAME_WIDTH / 2, GAME_HEIGHT * 0.65))
            screen.blit(self.left_hand, (GAME_WIDTH / 4, GAME_HEIGHT * 0.65))

        elif (self.timer //
              self.animation_frequency) % self.animation_stages == 1:
            screen.blit(self.left_hand_up,
                        (GAME_WIDTH * 0.15, GAME_HEIGHT / 2))

        elif (self.timer //
              self.animation_frequency) % self.animation_stages == 2:
            screen.blit(self.right_hand,
                        (GAME_WIDTH - GAME_WIDTH / 2, GAME_HEIGHT * 0.65))
            screen.blit(self.left_hand, (GAME_WIDTH / 4, GAME_HEIGHT * 0.65))
        elif (self.timer //
              self.animation_frequency) % self.animation_stages == 3:
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