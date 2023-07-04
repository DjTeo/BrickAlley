import os
import time
import pygame
from constants import *
from pygame.locals import *
from helper import Helper
from states.main_menu import MainMenu

class Game():

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        # set game title
        pygame.display.set_caption("Brick Alley")

        # set screen resolution
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT),
                                              DOUBLEBUF)
        self.centerX = self.screen.get_width() / 2
        self.centerY = self.screen.get_height() / 2
        self.running = True
        self.actions = {
            ACT.pause: False,
            ACT.left: False,
            ACT.right: False,
        }
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_states()
        print("Game initialized:")
        print(f"Game size is {(GAME_WIDTH, GAME_HEIGHT)} at {FPS} FPS")

    def game_loop(self):
        self.get_dt()
        self.get_events()
        self.update()
        self.render()
        self.clock.tick(FPS)

    def get_events(self):
        for event in pygame.event.get():
            self.state_stack[-1].handle_event(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.KEYUP:
                pass

    def update(self):
        try:
            self.state_stack[-1].update(self.dt, self.actions)
        except Exception as e:
            print(f"Error in update: {e.args}")
            self.restart()

    def render(self):
        try:
            # Render currest state
            self.state_stack[-1].render(self.screen)
            # Update the display
            pygame.display.flip()
        except Exception as e:
            print(f"Error in render: {e.args}")
            self.restart()

    def restart(self):
        self.state_stack.clear()
        self.load_states()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def load_assets(self):
        # Create pointers to directories
        _ = Helper()

    def load_states(self):
        self.title_screen = MainMenu(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def PlayMusic(self, soundFile: str, volume=0.5):
        soundFile = os.path.join(self.assets_dir, soundFile)
        pygame.mixer.music.load(soundFile)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)

    def PrepareSound(self, soundFile: str, volume=1.0) -> pygame.mixer.Sound:
        soundFile = os.path.join(self.assets_dir, soundFile)
        sound = pygame.mixer.Sound(soundFile)
        sound.set_volume(volume)
        return sound


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
    pygame.quit()