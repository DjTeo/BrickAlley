import pygame, os

from constants import GAME_WIDTH, PIVOT, TEXTURE_SIZE

#Teo
class Helper:

    def __init__(self):
        # Create pointers to directories
        Helper.assets_dir = os.path.join("assets")
        Helper.sprites_dir = os.path.join(self.assets_dir, "sprites")
        Helper.animated_sprites_dir = os.path.join(self.sprites_dir,
                                                   "animated_sprites")
        Helper.sounds_dir = os.path.join(self.assets_dir, "sounds")
        Helper.textures_dir = os.path.join(self.assets_dir, "textures")
        Helper.font = pygame.font.SysFont("Arial", 26)
        Helper.bold_font = pygame.font.SysFont("Arial", 26, True)
        Helper.big_font = pygame.font.SysFont("Arial", 36)

    @staticmethod
    def LoadSprite(spriteFile: str, size=None) -> pygame.Surface:
        spriteFile = os.path.join(Helper.sprites_dir, spriteFile)
        if not size:
            return pygame.image.load(spriteFile)
        return pygame.transform.smoothscale(pygame.image.load(spriteFile),
                                            size)
        
    #Tutorial
    @staticmethod
    def LoadTexture(textureFile, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        textureFile = os.path.join(Helper.textures_dir, textureFile)
        texture = pygame.image.load(textureFile).convert_alpha()
        return pygame.transform.scale(texture, res)

    @staticmethod
    def makeText(text: str, color):
        # create the Surface and the rectangle for some text.
        surface = Helper.font.render(text, True, color)
        return surface, surface.get_rect()

    @staticmethod
    def draw_text(surface,
                  text,
                  color,
                  x,
                  y,
                  big=False,
                  centerX=False,
                  pivot: PIVOT = PIVOT.center,
                  bold=False):
        if big:
            text_surface = Helper.big_font.render(text, True, color)
        elif bold:
            text_surface = Helper.bold_font.render(text, True, color)
        else:
            text_surface = Helper.font.render(text, True, color)

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
            Helper.CenterRect(text_rect, -1)
        surface.blit(text_surface, text_rect)

    @staticmethod
    def CenterRect(rect: pygame.Rect, y: float):
        rect.centerx = GAME_WIDTH / 2.0
        if y >= 0:
            rect.y = y

    @staticmethod
    def PrepareSound(soundFile: str, volume=1.0) -> pygame.mixer.Sound:
        soundFile = os.path.join(Helper.sounds_dir, soundFile)
        sound = pygame.mixer.Sound(soundFile)
        sound.set_volume(volume)
        return sound

    @staticmethod
    def PlayMusic(soundFile: str, volume=0.5):
        soundFile = os.path.join(Helper.sounds_dir, soundFile)
        pygame.mixer.music.load(soundFile)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)
