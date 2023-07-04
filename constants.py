from enum import Enum
import math

# game properties
FPS = 60
GAME_WIDTH = 1600
GAME_HEIGHT = 900
RES = (GAME_WIDTH, GAME_HEIGHT)
HALF_WIDTH = GAME_WIDTH // 2
HALF_HEIGHT = GAME_HEIGHT // 2

# player properties
PLAYER_POS = 0, 2  # mini_map
PLAYER_ANGLE = 0
PLAYER_STARTING_SPEED = 2
PLAYER_SIDEWAYS_SPEED = 2
PLAYER_ROT_SPEED = 1
PLAYER_SIZE_SCALE = 0.1
PLAYER_MAX_HEALTH = 100
PLAYER_LEFT_END = 1.15
PLAYER_RIGHT_END = 2.85
END_SCALE = 10

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = GAME_WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 30

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = GAME_WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AQUA = (0, 255, 255)
BLUE = (0, 0, 255)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVY_BLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
SILVER = (192, 192, 192)
SKY_BLUE = (135, 205, 235)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
BROWN = (128, 64, 16)

# light shade of the button
button_light = (172, 172, 172)

# dark shade of the button
button_dark = (100, 100, 100)


class PIVOT(Enum):
    center = 0,
    topLeft = 1,
    topRight = 2,
    bottomLeft = 3,
    bottomRight = 4


# define actions
class ACT(Enum):
    pause = 0
    left = 1
    right = 2