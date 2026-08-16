import pygame
from src.core.config import config as Config

class Map(pygame.sprite.Sprite):
    # lsp will scream at me if i don't have these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self, tileset: dict[int, pygame.Surface], data: list[list[int]]) -> None:
        super().__init__()

        self.tiles_width = len(data[0])
        self.tiles_height = len(data)

        self.width = self.tiles_width * Config.TILE_WIDTH
        self.height = self.tiles_height * Config.TILE_HEIGHT
        
        self.data = data
        self.tileset = tileset

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface: pygame.Surface) -> None:
        for y, row in enumerate(self.data):
            for x, tile_id in enumerate(row):
                self.image.blit(self.tileset[tile_id], (x * Config.TILE_WIDTH, y * Config.TILE_HEIGHT))

        surface.blit(self.image, self.rect)
