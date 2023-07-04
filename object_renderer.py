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
        self.blood_screen = Helper.LoadTexture('blood_texture.png', RES)
        # self.digit_size = 90
        # self.digit_images = [Helper.LoadTexture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
        #                      for i in range(11)]
        # self.digits = dict(zip(map(str, range(11)), self.digit_images))
        # self.game_over_image = Helper.LoadTexture('resources/textures/game_over.png', RES)
        # self.win_image = Helper.LoadTexture('resources/textures/win.png', RES)

    def draw(self, screen):
        self.draw_background(screen)
        self.render_game_objects(screen)
        self.draw_player_health(screen)

    def win(self):
        #     self.screen.blit(self.win_image, (0, 0))
        pass

    def game_over(self):
        #     self.screen.blit(self.game_over_image, (0, 0))
        pass

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

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self, screen):
        self.sky_offset = (self.sky_offset +
                           4.5 * self.game.player.rel) % GAME_WIDTH
        screen.blit(self.sky_image, (-self.sky_offset, 0))
        screen.blit(self.sky_image, (-self.sky_offset + GAME_WIDTH, 0))
        # floor
        pygame.draw.rect(screen, BROWN,
                         (0, HALF_HEIGHT, GAME_WIDTH, GAME_HEIGHT))

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