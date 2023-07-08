from helper import Helper
from states.endless_world import EndlessWorld
from states.game_world import GameWorld
from states.state import State
from constants import *
from pygame.rect import Rect
import pygame

#Teo
class MainMenu(State):

    def __init__(self, game):
        State.__init__(self, game)
        self.walls = Helper.LoadTexture("wallTexture.png",
                                        (GAME_WIDTH, GAME_HEIGHT))
        self.brick = Helper.LoadSprite("a-brick.png", (140, 80))
        self.brick_rect = self.brick.get_rect()
        Helper.CenterRect(self.brick_rect, 300 - self.brick.get_height() / 2)
        self.start_sp_SURF, self.start_sp_RECT = Helper.makeText(
            " Start Game ", GOLD)
        self.quit_SURF, self.quit_RECT = Helper.makeText(
            " Exit Game ", NAVY_BLUE)
        Helper.CenterRect(self.start_sp_RECT, 200)
        Helper.CenterRect(self.quit_RECT, 400)

    def update(self, delta_time):
        pass

    def render(self, display):
        display.fill(SKY_BLUE)
        display.blit(self.walls,
                     Rect(0, GAME_HEIGHT - HALF_HEIGHT, GAME_WIDTH, GAME_HEIGHT))
        # display.fill(BROWN, Rect(0, GAME_HEIGHT - 150, GAME_WIDTH, 150))
        Helper.draw_text(display, "Hello Brick, I am Alley!", MAROON, 0, 50,
                         True, True)
        self.draw_button_background(display, button_light, button_dark,
                                    self.start_sp_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.quit_RECT)

        display.blit(self.start_sp_SURF, self.start_sp_RECT)
        display.blit(self.quit_SURF, self.quit_RECT)
        display.blit(self.brick, self.brick_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.quit_RECT.collidepoint(mouse_pos):
                self.game.running = False
            elif self.brick_rect.collidepoint(mouse_pos):
                new_state = EndlessWorld(self.game)
                new_state.enter_state()
            elif self.start_sp_RECT.collidepoint(mouse_pos):
                new_state = GameWorld(self.game)
                new_state.enter_state()
