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
        self._tiles: np.ndarray = np.array([[0 for _ in range(self.width)] for _ in range(self.height)])
        
        self.surface_width = (
        (self.width + self.height - 2) * Config.TILE_TOP_WIDTH
        + Config.FULL_TILE_WIDTH * 2 # it clips a little to the right
        )

        self.surface_height = (
        (self.width + self.height - 2) * Config.TILE_TOP_HEIGHT
        + Config.FULL_TILE_HEIGHT
        )
        self._surface = pygame.Surface(
        (self.surface_width, self.surface_height),
        pygame.SRCALPHA,
        )
        self.rect = self._surface.get_rect()
        self.rect.topleft = (screen_x, screen_y)
        self.grid_drawing_offset = self.height * Config.TILE_TOP_WIDTH

    def draw(self, surface: pygame.Surface):
        for y, row in enumerate(self._tiles):
            for x, tile in enumerate(row):
                tile = TILE_REGISTRY[tile]
                isometric_x_position = (x * Config.TILE_TOP_WIDTH) - (y * Config.TILE_TOP_WIDTH) + self.grid_drawing_offset
                isometric_y_position = (x * Config.TILE_TOP_HEIGHT) + (y * Config.TILE_TOP_HEIGHT)
                self._surface.blit(tile.image, (isometric_x_position, isometric_y_position))

        surface.blit(self._surface, self.rect)

    def screen_coord_to_grid(self, screen_x: int | float, screen_y: int | float) -> tuple[int | float, int | float]:
        relative_x = (screen_x - self.rect.topleft[0]) - self.grid_drawing_offset
        relative_y = screen_y - self.rect.topleft[1]

        x_coord = ((relative_x / Config.TILE_TOP_WIDTH) + (relative_y / Config.TILE_TOP_HEIGHT)) // 2
        y_coord = ((relative_y / Config.TILE_TOP_HEIGHT) - (relative_x / Config.TILE_TOP_WIDTH)) // 2

        return int(x_coord) - 1, int(y_coord)

