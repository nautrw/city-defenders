from pygame.examples.headless_no_windows_needed import screen
import pygame
from src.core.config import config as Config
from src.core.utils import Coordinate

class GameMap(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, tileset: dict[int, pygame.Surface], map_data: list[list[int]]) -> None:
        super().__init__()

        self.tileset = tileset
        self.map_data = map_data

        self.tiles_width = len(map_data[0])
        self.tiles_height = len(map_data)

        self.map_width = self.tiles_height * Config.TILE_WIDTH
        self.map_height = self.tiles_height * Config.TILE_HEIGHT

        self.image = pygame.Surface((self.map_width, self.map_height))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def update(self, dt: int | float) -> None:
        pass
    
    def screen_to_map_coord(self, offset: Coordinate, screen_coords: Coordinate) -> Coordinate:
        print(f"offset: {offset}")
        print(f"screen coords: {screen_coords}")
        print(f"map rect: {self.rect.x, self.rect.y}")
        # return (screen_coords[0] - offset[0], screen_coords[1] - offset[1])
        return (self.rect.x - screen_coords[0], self.rect.y - screen_coords[1])

    def draw(self, surface: pygame.Surface) -> None:
        for y, row in enumerate(self.map_data):
            for x, tile_id in enumerate(row):
                self.image.blit(self.tileset[tile_id], (x * Config.TILE_WIDTH, y * Config.TILE_HEIGHT))

        surface.blit(self.image, self.rect)
