import pygame, os

from constants import TEXTURE_SIZE


class Helper:
    assets_dir: str
    sprites_dir: str
    textures_dir: str

    def __init__(self):
        Helper.assets_dir=os.path.join("assets")
        Helper.sprites_dir = os.path.join(self.assets_dir, "sprites")
        Helper.textures_dir = os.path.join(self.assets_dir, "textures")

    @staticmethod
    def LoadSprite(spriteFile: str, size=None) -> pygame.Surface:
        spriteFile = os.path.join(Helper.sprites_dir, spriteFile)
        if not size:
            return pygame.image.load(spriteFile)
        return pygame.transform.smoothscale(pygame.image.load(spriteFile),
                                            size)

    @staticmethod
    def LoadTexture(textureFile, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        textureFile = os.path.join(Helper.textures_dir, textureFile)
        texture = pygame.image.load(textureFile).convert_alpha()
        return pygame.transform.scale(texture, res)