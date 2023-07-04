from constants import *
import pygame
import math


class Player:

    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.forward_speed = PLAYER_STARTING_SPEED
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pygame.time.get_ticks()
        # diagonal movement correction
        self.diag_move_corr = 1 / math.sqrt(2)

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
            self.game.object_renderer.game_over()
            pygame.display.flip()
            pygame.time.delay(1500)
            # self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        pass
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1 and not self.shot and not self.game.weapon.reloading:
        #         self.game.sound.shotgun.play()
        #         self.shot = True
        #         self.game.weapon.reloading = True

    def movement(self, delta_time):

        dx, dy = self.forward_speed * delta_time, 0
        speed = PLAYER_SIDEWAYS_SPEED * delta_time

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            dy -= speed
        if keys[pygame.K_d]:
            dy += speed

        self.check_movement(dx, dy, delta_time)

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * delta_time
        self.angle %= math.tau

    def check_movement(self, dx, dy, delta_time):
        scale = PLAYER_SIZE_SCALE / delta_time
        self.x += dx
        if self.y + dy < 2.9 and self.y + dy > 1.1:
            self.y += dy

    def draw(self, screen):
        pygame.draw.line(screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + GAME_WIDTH * math.cos(self.angle),
                      self.y * 100 + GAME_WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(screen, 'green', (self.x * 100, self.y * 100), 15)

    # def mouse_control(self):
    #     mx, my = pygame.mouse.get_pos()
    #     if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
    #         pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
    #     self.rel = pygame.mouse.get_rel()[0]
    #     self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
    #     self.angle += self.rel * MOUSE_SENSITIVITY * delta_time

    def update(self, delta_time):
        self.movement(delta_time)
        # self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)