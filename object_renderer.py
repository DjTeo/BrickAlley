import random
import pygame
from constants import *
from helper import Helper


class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_textures()
        self.sky_image = Helper.LoadTexture(F'sky.png',
                                            (GAME_WIDTH, HALF_HEIGHT))
        self.game_over_image = Helper.LoadTexture('game_over.png', RES)
        self.win_image = Helper.LoadTexture('victory.png', RES)

    def draw(self, screen):
        self.draw_background(screen)
        self.render_game_objects(screen)

    def drawUI(self, screen, score):
        if self.game.game_over:
            screen.blit(self.game_over_image, (0, 0))
        elif self.game.victory:
            screen.blit(self.win_image, (0, 0))
        if self.game.game_over or self.game.victory:
            Helper.draw_text(screen,
                             F'Total Score: {score}',
                             SILVER,
                             0,
                             50,
                             pivot=PIVOT.topRight,
                             centerX=True,
                             big=True)

        Helper.draw_text(screen,
                         F'Distance: {int(self.game.player.x)}',
                         NAVY_BLUE,
                         10,
                         5,
                         pivot=PIVOT.topLeft,
                         big=True)
        Helper.draw_text(screen,
                         F'Health: {self.game.player.health}',
                         MAROON,
                         0,
                         5,
                         pivot=PIVOT.topLeft,
                         centerX=True,
                         big=True)
        Helper.draw_text(screen,
                         F'Coins: {self.game.player.coins_collected}',
                         GOLD,
                         GAME_WIDTH - 10,
                         5,
                         pivot=PIVOT.topRight,
                         big=True)

    def draw_background(self, screen):
        # Sky
        screen.blit(self.sky_image, (0, 0))
        # Floor
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