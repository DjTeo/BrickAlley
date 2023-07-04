from constants import *
import pygame
import math

from helper import Helper


class Player:

    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.forward_speed = PLAYER_STARTING_SPEED
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pygame.time.get_ticks()
        self.player_hit = False
        self.player_pain = Helper.PrepareSound("player_pain.wav")
        self.blood_screen = Helper.LoadTexture('blood_texture.png', RES)

    def recover_health(self):
        if self.check_health_recovery_delay(
        ) and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            pass
            # self.game.object_renderer.game_over()
            # pygame.display.flip()
            # pygame.time.delay(1500)
            # self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.player_hit = True
        self.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        pass

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

    def update(self, delta_time):
        self.movement(delta_time)
        # self.mouse_control()
        self.recover_health()

    def draw(self, screen):
        if self.player_hit:
            screen.blit(self.blood_screen, (0, 0))
            self.player_hit = False

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)