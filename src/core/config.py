from pathlib import Path

import pygame
from pygame.typing import ColorLike

SCREEN_WIDTH: int = 1440
SCREEN_HEIGHT: int = 960
FLAGS: int = pygame.SCALED
FPS: int = 120


TILE_WIDTH: int = 32
TILE_HEIGHT: int = 32
MAP_SCALE_FACTOR: int = 4
GUI_ICON_SIZE: tuple[int, int] = (64, 64)

GROUND_TILES_LAYER_NAME: str = "ground"
PATH_TILES_LAYER_NAME: str = "path_tiles"
ENEMY_PATH_LAYER_NAME: str = "path_polygon"


LOW_HEALTH_COLOR: ColorLike = (255, 0, 0)
MAX_HEALTH_COLOR: ColorLike = (0, 255, 0)
TURRET_RADIUS_COLOR: ColorLike = (0, 0, 0, 75)

BUTTON_NORMAL_BG: ColorLike = "darkgray"
BUTTON_HOVERED_BG: ColorLike = "lightgray"
BUTTON_PRESSED_BG: ColorLike = "lightcoral"

DARK_BG: ColorLike = "#15191e"

TEXT_NORMAL: ColorLike = "black"

FONT_NORMAL: str = "Oleaguid"
FONT_SIZE_NORMAL: int = 36
FONT_SIZE_HEADER: int = 48


ASSET_PATH: Path = Path("src", "assets")
MAPS_PATH: Path = Path("src", "assets", "maps")
FONTS_PATH: Path = Path("src", "assets", "fonts")
