import pygame
from helper import Helper
from states.state import State
from constants import *


class PauseMenu(State):

    def __init__(self, game):
        State.__init__(self, game)
        # Set the menu
        self.resume_game_SURF, self.resume_game_RECT = Helper.makeText(
            " Resume Game ", GOLD)
        self.exit_game_SURF, self.exit_game_RECT = Helper.makeText(
            " Exit to Main Menu ", NAVY_BLUE)

        Helper.CenterRect(self.resume_game_RECT, 200)
        Helper.CenterRect(self.exit_game_RECT, 300)

    def update(self, delta_time):
        pass

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        self.prev_state.render(display)

        self.draw_button_background(display, button_light, button_dark,
                                    self.resume_game_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.exit_game_RECT)
        display.blit(self.resume_game_SURF, self.resume_game_RECT)
        display.blit(self.exit_game_SURF, self.exit_game_RECT)

    def handle_event(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and
            (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE)):
            self.exit_state()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.resume_game_RECT.collidepoint(mouse_pos):
                self.exit_state()
            if self.exit_game_RECT.collidepoint(mouse_pos):
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()
