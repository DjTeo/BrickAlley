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
        self.groundOffset = 55
        self.game_over = False
        self.victory = False
        self.itemsCount = 10
        self.playerNum = 1
        self.current_distance: float = 0
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)

    def update(self, delta_time, actions):
        pygame.display.set_caption(
            f'Brick Alley - {self.clock.get_fps() :.1f}FPS')
        if not self.game_over and not self.victory:
            self.player.update(delta_time)
            self.raycasting.update()
            self.object_handler.update()

    def render(self, display):
        #display.fill('black')
        self.object_renderer.draw(display)
        self.player.draw(display)

    def handle_event(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.exit_state()
        self.player.single_fire_event(event)
