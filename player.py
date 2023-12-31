from constants import *
import pygame
from helper import Helper


class Player:

    def __init__(self,
                 game,
                 health=PLAYER_MAX_HEALTH,
                 max_speed=MAX_SPEED,
                 left_Wall=LEFT_WALL,
                 right_Wall=RIGHT_WALL,
                 end_distance=END_DISTANCE):
        self.game = game
        self.x = 0
        self.y = (left_Wall + right_Wall) / 2 + 0.5
        self.forward_speed = PLAYER_STARTING_SPEED
        self.angle = 0
        self.health = health
        self.player_hit = False
        self.coins_collected = 0
        self.max_speed = max_speed
        self.left_end = left_Wall + 1 + PLAYER_SIZE_SCALE
        self.right_end = right_Wall - PLAYER_SIZE_SCALE
        self.end_distance = end_distance

        self.player_pain = Helper.PrepareSound("player_pain.wav", 0.5)
        self.collect_sound = Helper.PrepareSound("collect.wav", 0.6)
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
        self.animation_frequency = 0.2  #this should be related to player speed forward WIP

    #Teo,Tutorial
    def check_win(self):
        if self.x >= self.end_distance:
            self.game.victory = True

    #chris
    def increase_dif(self, delta_time):
        if self.forward_speed < self.max_speed:
            self.forward_speed += 0.075 * delta_time
        else:
            self.forward_speed = self.max_speed

    #Tutorial
    # Player got hit
    def get_damage(self, damage):
        self.health -= damage
        self.player_hit = True
        self.player_pain.play()
        #Teo
        if self.health < 1:
            self.health = 0
            self.game.game_over = True

    #chris
    # Health up
    def recover_health(self, amount):
        if self.health < 100:
            if self.health + amount > 100:
                self.health = 100
            else:
                self.health += amount

    #Teo
    def total_score(self):
        return int(self.x) + self.coins_collected * COINS_SCORE + self.health

    #Teo
    def movement(self, delta_time):
        dx, dy = self.forward_speed, 0
        speed = PLAYER_SIDEWAYS_SPEED

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dy -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dy += speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= PLAYER_FORWARD_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += PLAYER_FORWARD_SPEED

        self.animation_frequency = self.calculate_anim_frequency(dx)

        self.check_movement(dx * delta_time, dy * delta_time)

    #Teo
    def check_movement(self, dx, dy):
        self.x += dx
        if self.y + dy <= self.right_end and self.y + dy >= self.left_end:
            self.y += dy

    #chris
    def calculate_anim_frequency(self, dx):
        if dx >= 1:
            result = 0.27 - 0.046 * math.sqrt(dx - 1)
        else:  #in case player hits 5 too early
            result = 0.25
        if result < 0.1:
            return 0.1
        return result

    #chris
    def check_collision(self):
        closest = self.game.object_handler.closest_enemy()
        if closest.y < self.y + PLAYER_SIZE_SCALE + closest.size and closest.y > self.y - PLAYER_SIZE_SCALE - closest.size:
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
                self.game.object_handler.remove_obstacle(closest)
        elif closest.x <= self.x:
            self.game.object_handler.remove_obstacle(closest)

    def update(self, delta_time):
        self.timer += delta_time
        self.movement(delta_time)
        self.check_win()
        if self.game.object_handler.obstacle_list:
            self.check_collision()
        self.increase_dif(delta_time)

    #chris
    def render(self, screen):
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