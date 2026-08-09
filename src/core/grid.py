import pygame
import numpy as np
from src.entities.tiles import Tile, TILE_REGISTRY
from src.core.config import config as Config

class Grid(pygame.sprite.Sprite):
    rect: pygame.FRect | pygame.Rect
    image: pygame.Surface

    def __init__(self, width: int, height: int, screen_x: int | float, screen_y: int | float):
        # dimensions are in numbers of tiles
        self.width = width
        self.height = height
        self._tiles: np.ndarray = np.zeros((5, 5))
        self._surface = pygame.Surface((self.width * Config.FULL_TILE_WIDTH, self.height * Config.FULL_TILE_HEIGHT))
        self.rect = self._surface.get_rect()
        self.rect.topleft = (screen_x, screen_y)

    def draw(self, surface: pygame.Surface):
        for y, row in enumerate(self._tiles):
            for x, tile in enumerate(row):
                tile = TILE_REGISTRY[tile]
                self._surface.blit(tile.image, (((x * Config.TILE_TOP_WIDTH) - (y * Config.TILE_TOP_WIDTH)), (x * Config.TILE_TOP_HEIGHT) + (y * Config.TILE_TOP_HEIGHT)))

        surface.blit(self._surface, self.rect)
