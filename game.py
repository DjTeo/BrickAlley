import os
import time
import pygame
from constants import *
from pygame.locals import *
from helper import Helper
from states.main_menu import MainMenu


class Game():
    sprites_dir: str

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
            ACT.left1: False,
            ACT.right1: False,
            ACT.up1: False,
            ACT.down1: False,
            ACT.jump1: False,
            ACT.left2: False,
            ACT.right2: False,
            ACT.up2: False,
            ACT.down2: False,
            ACT.jump2: False,
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

    def draw_text(self,
                  surface,
                  text,
                  color,
                  x,
                  y,
                  big=False,
                  centerX=False,
                  pivot: PIVOT = PIVOT.center,
                  bold=False):
        if big:
            text_surface = self.big_font.render(text, True, color)
        elif bold:
            text_surface = self.bold_font.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)

        text_rect = text_surface.get_rect()
        match pivot:
            case PIVOT.topLeft:
                text_rect.topleft = (x, y)
            case PIVOT.topRight:
                text_rect.topright = (x, y)
            case PIVOT.bottomLeft:
                text_rect.bottomleft = (x, y)
            case PIVOT.bottomRight:
                text_rect.bottomright = (x, y)
            case _:  # PIVOT.center:
                text_rect.center = (x, y)

        if centerX:
            self.CenterRect(text_rect, -1)
        surface.blit(text_surface, text_rect)

    def CenterRect(self, rect: pygame.Rect, y: float):
        rect.centerx = GAME_WIDTH / 2.0
        if y >= 0:
            rect.y = y

    def makeText(self, text: str, color):
        # create the Surface and the rectangle for some text.
        surface = self.font.render(text, True, color)
        return surface, surface.get_rect()

    def load_assets(self):
        # Create pointers to directories
        # Game.assets_dir = os.path.join("assets")
        # self.font_dir = os.path.join(self.assets_dir, "font")
        # Game.sprites_dir = os.path.join(self.assets_dir, "sprites")
        # Game.textures_dir = os.path.join(self.assets_dir, "textures")
        # self.font = pygame.font.Font(os.path.join(self.font_dir, "myFont.ttf"), 26)
        # self.big_font = pygame.font.Font(os.path.join(self.font_dir, "myFont.ttf"), 36)
        _ = Helper()
        self.font = pygame.font.SysFont("Arial", 26)
        self.bold_font = pygame.font.SysFont("Arial", 26, True)
        self.big_font = pygame.font.SysFont("Arial", 36)

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