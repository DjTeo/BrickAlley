from states.state import State
from constants import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *


class GameWorld(State):

    def __init__(self, game):
        State.__init__(self, game)
        self.game_over = False
        self.victory = False
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)

    def update(self, delta_time):
        pygame.display.set_caption(
            f'Brick Alley - {self.clock.get_fps() :.1f}FPS')
        if not self.game_over and not self.victory:
            self.player.update(delta_time)
            self.raycasting.update()
            self.object_handler.update(delta_time)

    def render(self, display):
        self.object_renderer.render(display)
        self.player.render(display)
        self.object_renderer.renderUI(display, self.player.total_score())

    def handle_event(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and
            (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE)):
            if self.game_over or self.victory:
                self.exit_state()
            else:
                self.game.pause_game()
