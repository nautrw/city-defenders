import pygame
from enum import Enum, auto
from pathlib import Path

class TileRoles(Enum):
    NORMAL = auto()
    ROAD = auto()

class Tile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.FRect | pygame.Rect

    def __init__(self, name: str, role: TileRoles):
        self.name = name
        self.image = pygame.image.load(Path("src", "assets", "tiles", f"{name}.png"))
        self.role = role

TILE_REGISTRY = {
    0: Tile(name="dirt", role=TileRoles.ROAD),
    1: Tile(name="forest_grass", role=TileRoles.NORMAL),
    2: Tile(name="stone", role=TileRoles.NORMAL)
}
