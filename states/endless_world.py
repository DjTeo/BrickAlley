from states.state import State
from constants import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *


class EndlessWorld(State):

    def __init__(self, game):
        State.__init__(self, game)
        self.game_over = False
        self.victory = False
        self.player = Player(self,
                             right_Wall=ENDLESS_RIGHT_WALL,
                             obstacle_min_timer=ENDLESS_MIN_RESPAWN,
                             max_speed=ENDLESS_MAX_SPEED,
                             coin_timer=ENDLESS_COIN_RESPAWN,
                             end_distance=ENDLESS_DISTANCE)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self,
                                     rightWall=ENDLESS_RIGHT_WALL,
                                     end_distance=ENDLESS_DISTANCE)
        self.object_handler = ObjectHandler(self,
                                            rightWall=ENDLESS_RIGHT_WALL,
                                            weights=ENDLESS_OBSTACLES_WEIGHTS,
                                            endless=True)

    def update(self, delta_time):
        pygame.display.set_caption(
            f'Brick Alley - {self.clock.get_fps() :.1f}FPS')
        if not self.game_over and not self.victory:
            self.player.update(delta_time)
            self.raycasting.update()
            self.object_handler.update(delta_time)

    def render(self, display):
        self.object_renderer.draw(display)
        self.player.draw(display)
        self.object_renderer.drawUI(display, self.player.total_score())

    def handle_event(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.exit_state()
