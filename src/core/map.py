import pygame
from src.core.config import config as Config

class Map(pygame.sprite.Sprite):
    # lsp will scream at me if i don't have these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self, tileset: dict[int, pygame.Surface], data: list[list[int]]) -> None:
        super().__init__()

        self.tiles_width = len(data)
        self.tiles_height = len(data[0])

        self.width = self.tiles_width * Config.TILE_WIDTH
        self.height = self.tiles_height * Config.TILE_HEIGHT
        
        self.data = data
        self.tileset = tileset

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft=(0, 0))

    def draw(self, surface: pygame.Surface) -> None:
        for y, column in enumerate(self.data):
            for x, row in enumerate(column):
                tile_id = self.data[y][x]
            
                tile_rect = pygame.Rect(x * Config.TILE_WIDTH, y * Config.TILE_HEIGHT, Config.TILE_WIDTH, Config.TILE_HEIGHT)
                self.surface.blit(self.tileset[tile_id], tile_rect)

        surface.blit(self.surface, self.rect)
