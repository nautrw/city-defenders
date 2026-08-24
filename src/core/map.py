import pygame
from src.core.config import config as Config
from src.core.utils import Coordinate

class MapTile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect:  pygame.Rect | pygame.FRect

    def __init__(self, map_x: int, map_y: int, tile_img: pygame.Surface):
        super().__init__()

        self.image = tile_img.copy()
        self.rect = self.image.get_rect(topleft=(map_x * Config.TILE_WIDTH, map_y * Config.TILE_HEIGHT))

class GameMap(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, tileset: dict[int, pygame.Surface], map_data: dict) -> None:
        super().__init__()

        self.tileset = tileset
        self.map_data = map_data
        print(self.map_data)

        self.tiles_width = map_data["width"]
        self.tiles_height = map_data["height"]

        self.map_width = self.tiles_width * Config.TILE_WIDTH
        self.map_height = self.tiles_height * Config.TILE_HEIGHT
        
        self.ground_tiles = pygame.sprite.Group()
        self.path_tiles = pygame.sprite.Group()

        self._load_layer(Config.GROUND_TILES_LAYER_NAME, self.ground_tiles)
        self._load_layer(Config.PATH_TILES_LAYER_NAME, self.path_tiles)

        self.image = pygame.Surface((self.map_width, self.map_height))
        self._redraw()

        self.rect = self.image.get_rect(topleft=(0, 0))

    def _load_layer(self, layer_name: str, group: pygame.sprite.Group) -> None:
        layer = self.map_data["layers"][layer_name]["data"]

        for y, row in enumerate(layer):
            for x, tile_id in enumerate(row):
                if tile_id == -1: # empty
                    continue
                
                tile = MapTile(x, y, self.tileset[tile_id])
                group.add(tile)

    def _redraw(self) -> None:
        self.image.fill((0, 0, 0, 0))

        self.ground_tiles.draw(self.image)
        self.path_tiles.draw(self.image)

        pygame.draw.lines(self.image, "black", False, self.map_data["layers"][Config.ENEMY_PATH_LAYER_NAME]["data"], width=2)

    def update(self, dt: int | float) -> None:
        pass
    
    def screen_to_map_coord(self, screen_x: int | float, screen_y: int | float) -> Coordinate:
        return (self.rect.x - screen_x, self.rect.y - screen_y)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
