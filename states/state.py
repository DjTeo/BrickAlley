import pygame


class State():

    def __init__(self, game):
        self.game = game
        self.clock = game.clock
        self.prev_state = None

    def update(self, delta_time):
        pass

    def render(self, display: pygame.Surface):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()

    def handle_event(self, event: pygame.event):
        pass

    def draw_button_background(self, surface, button_light, button_dark,
                               button_rect):
        # get mouse pos
        mouse = pygame.mouse.get_pos()
        posX = mouse[0]
        posY = mouse[1]

        # check if mouse is over a button
        if (button_rect.x <= posX <= button_rect.x + button_rect.width and
                button_rect.y <= posY <= button_rect.y + button_rect.height):
            pygame.draw.rect(surface, button_light, button_rect)
        else:
            pygame.draw.rect(surface, button_dark, button_rect)
