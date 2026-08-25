from pathlib import Path

import pygame
from pygame.typing import ColorLike

SCREEN_WIDTH: int = 360
SCREEN_HEIGHT: int = 240
FLAGS: int = pygame.SCALED
FPS: int = 120


TILE_WIDTH: int = 32
TILE_HEIGHT: int = 32

GROUND_TILES_LAYER_NAME: str = "ground"
PATH_TILES_LAYER_NAME: str = "path_tiles"
ENEMY_PATH_LAYER_NAME: str = "path_polygon"


LOW_HEALTH_COLOR: ColorLike = (255, 0, 0)
MAX_HEALTH_COLOR: ColorLike = (0, 255, 0)
TURRET_RADIUS_COLOR: ColorLike = (185, 69, 29, 100)

BUTTON_NORMAL_BG: ColorLike = "darkgray"
BUTTON_HOVERED_BG: ColorLike = "lightgray"
BUTTON_PRESSED_BG: ColorLike = "lightcoral"

DARK_BG: ColorLike = "#15191e"

TEXT_NORMAL: ColorLike = "black"

FONT_NAME: str = "freesansbold.ttf"
FONT_SIZE_NORMAL = 8


ASSET_PATH: Path = Path("src", "assets")
