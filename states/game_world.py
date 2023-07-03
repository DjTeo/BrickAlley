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
        self.itemsCount = 10
        self.playerNum = 1
        self.current_distance: float = 0
        self.player: Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)

    def update(self, delta_time, actions):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def render(self, display):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def handle_event(self, event):
        self.global_trigger = False
        for event in pg.event.get():
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.exit_state()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)