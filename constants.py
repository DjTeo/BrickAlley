from enum import Enum
import math

# GAME PROPERTIES
FPS = 60
GAME_WIDTH = 1600
GAME_HEIGHT = 900
RES = (GAME_WIDTH, GAME_HEIGHT)
HALF_WIDTH = GAME_WIDTH // 2
HALF_HEIGHT = GAME_HEIGHT // 2
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

# WORLD PROPERTIES
END_DISTANCE = 200
LEFT_WALL = 0
RIGHT_WALL = 3

# ENDLESS WORLD PROPERTIES
ENDLESS_DISTANCE = 9000
ENDLESS_RIGHT_WALL = 5
ENDLESS_MIN_RESPAWN = 250  # in ms
ENDLESS_MAX_SPEED = 8
ENDLESS_COIN_RESPAWN = 3000  # in ms
ENDLESS_HEART_DECREASE = 500  # distance
ENDLESS_OBSTACLES_WEIGHTS = [45, 40, 15] 

# PLAYER PROPERTIES
PLAYER_STARTING_SPEED = 2
PLAYER_SIDEWAYS_SPEED = 2
PLAYER_FORWARD_SPEED = 1
PLAYER_SIZE_SCALE = 0.2
PLAYER_MAX_HEALTH = 100
MAX_SPEED = 5

# OBSTACLES PROPERTIES
OBSTACLES_RESPAWN = 1200  # in ms
MIN_RESPAWN = 500  # in ms
OBSTACLES_WEIGHTS = [47, 43, 10]  # running enenmy, ball, health
COINS_SCORE = 5
COIN_RESPAWN = 4000  # in ms

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
GOLD = (255, 215, 0)

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
