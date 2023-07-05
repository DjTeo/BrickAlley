import pygame
from constants import *
from helper import Helper


class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_textures()
        self.sky_image = Helper.LoadTexture('sky.png',
                                            (GAME_WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

        self.economy_timer = 0
        self.left_hand = Helper.LoadSprite('leftHand.png',
                                           (GAME_WIDTH / 4, GAME_HEIGHT / 2))
        self.right_hand = Helper.LoadSprite('rightHand.png',
                                            (GAME_WIDTH / 4, GAME_HEIGHT / 2))

        self.left_hand_up = Helper.LoadSprite(
            'leftHandUp.png', (GAME_WIDTH * 0.4, GAME_HEIGHT * 0.8))
        self.right_hand_up = Helper.LoadSprite(
            'rightHandUp.png', (GAME_WIDTH * 0.4, GAME_HEIGHT * 0.8))
        self.time_pre = pygame.time.get_ticks()
        self.animation_stages = 4
        self.animation_frequency = 180  #this should be related to player speed forward WIP
        
        # self.digit_size = 90
        # self.digit_images = [Helper.LoadTexture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
        #                      for i in range(11)]
        # self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = Helper.LoadTexture('game_over.png', RES)
        self.win_image = Helper.LoadTexture('victory.png', RES)

    def draw(self, screen):
        self.draw_background(screen)
        self.render_game_objects(screen)
        self.draw_player_health(screen)
        self.draw_hands(screen)
        self.drawWinLose(screen)

    def drawWinLose(self, screen):
        if self.game.game_over:
            screen.blit(self.game_over_image, (0, 0))
        elif self.game.victory:
            screen.blit(self.win_image, (0, 0))

    def draw_player_health(self, screen):
        health = str(self.game.player.health)
        Helper.draw_text(screen,
                         F'Health: {health}',
                         MAROON,
                         0,
                         20,
                         centerX=True,
                         big=True)
        # for i, char in enumerate(health):
        #     screen.blit(self.digits[char], (i * self.digit_size, 0))
        # screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def draw_background(self, screen):
        self.sky_offset = self.sky_offset % GAME_WIDTH
        screen.blit(self.sky_image, (-self.sky_offset, 0))
        screen.blit(self.sky_image, (-self.sky_offset + GAME_WIDTH, 0))
        # floor
        pygame.draw.rect(screen, BROWN,
                         (0, HALF_HEIGHT, GAME_WIDTH, GAME_HEIGHT))

    def draw_hands(self, screen):

        self.timer = pygame.time.get_ticks()
        if (
            (self.timer - self.time_pre) // self.animation_frequency
        ) % self.animation_stages == 0:  #and self.timer-self.time_pre<2*self.animation_stages:
            screen.blit(self.right_hand,
                        (GAME_WIDTH - GAME_WIDTH / 2, GAME_HEIGHT * 0.65))
            screen.blit(self.left_hand, (GAME_WIDTH / 4, GAME_HEIGHT * 0.65))

        elif ((self.timer - self.time_pre) //
              self.animation_frequency) % self.animation_stages == 1:
            screen.blit(self.left_hand_up,
                        (GAME_WIDTH * 0.15, GAME_HEIGHT / 2))

        elif ((self.timer - self.time_pre) //
              self.animation_frequency) % self.animation_stages == 2:
            screen.blit(self.right_hand,
                        (GAME_WIDTH - GAME_WIDTH / 2, GAME_HEIGHT * 0.65))
            screen.blit(self.left_hand, (GAME_WIDTH / 4, GAME_HEIGHT * 0.65))
        elif ((self.timer - self.time_pre) //
              self.animation_frequency) % self.animation_stages == 3:
            screen.blit(self.right_hand_up,
                        (GAME_WIDTH * 0.5, GAME_HEIGHT / 2))

    def render_game_objects(self, screen):
        list_objects = sorted(self.game.raycasting.objects_to_render,
                              key=lambda t: t[0],
                              reverse=True)
        for depth, image, pos in list_objects:
            screen.blit(image, pos)

    def load_wall_textures(self):
        return {
            0: Helper.LoadTexture('void.png'),
            1: Helper.LoadTexture('wallTexture.png'),
            2: Helper.LoadTexture('wallHoleTexture.png'),
            3: Helper.LoadTexture('doorLeft.png'),
            4: Helper.LoadTexture('doorRight.png'),
        }