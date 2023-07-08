import pygame
import math
from constants import *

#Tutorial
class RayCasting:

    def __init__(self,
                 game,
                 leftWall=LEFT_WALL,
                 rightWall=RIGHT_WALL,
                 end_distance=END_DISTANCE):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
        self.leftWall = leftWall
        self.rightWall = rightWall
        self.middleLeft = int((leftWall + rightWall) / 2.0)
        self.middleRight = self.middleLeft + 1
        self.end_distance = end_distance

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < GAME_HEIGHT:
                wall_surface = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_surface = pygame.transform.scale(wall_surface,
                                                     (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * GAME_HEIGHT / proj_height
                wall_surface = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),
                    HALF_TEXTURE_SIZE - texture_height // 2, SCALE,
                    texture_height)
                wall_surface = pygame.transform.scale(wall_surface,
                                                     (SCALE, GAME_HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_surface, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        remain_dist = (self.end_distance - ox)

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor[1] == self.leftWall or tile_hor[
                        1] == self.rightWall:
                    if tile_hor[0] % 23 == 0 and tile_hor[1] == self.rightWall:
                        texture_hor = 2
                        break
                    if tile_hor[0] % 17 == 0 and tile_hor[1] == self.leftWall:
                        texture_hor = 2
                        break
                    texture_hor = 1
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                #RENDER THE EXIT DOOR AT MAX DEPTH
                if i == int(remain_dist):
                    if tile_vert[1] == self.middleLeft:
                        texture_vert = 3
                        break
                    elif tile_vert[1] == self.middleRight:
                        texture_vert = 4
                        break
                    else:
                        texture_vert = 1
                        break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append(
                (depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()