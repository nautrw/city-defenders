from pathlib import Path

import pygame
from pygame.typing import ColorLike

SCREEN_WIDTH: int = 1440
SCREEN_HEIGHT: int = 960
FLAGS: int = pygame.SCALED
FPS: int = 120


TILE_WIDTH: int = 32
TILE_HEIGHT: int = 32
MAP_SCALE_FACTOR: int = 3
GUI_ICON_SIZE: tuple[int, int] = (64, 64)

GROUND_TILES_LAYER_NAME: str = "ground"
BLOCKED_TILES_LAYER_NAME: str = "blocked"
ENEMY_PATH_LAYER_NAME: str = "path"


LOW_HEALTH_COLOR: ColorLike = (255, 0, 0)
MAX_HEALTH_COLOR: ColorLike = (0, 255, 0)
TURRET_RADIUS_COLOR: ColorLike = (0, 0, 0, 75)

BUTTON_NORMAL_BG: ColorLike = "#807b7a"
BUTTON_HOVERED_BG: ColorLike = "#595757"
BUTTON_PRESSED_BG: ColorLike = "#323232"

BUY_BUTTON_NORMAL_BG: ColorLike = "#477238"
BUY_BUTTON_HOVERED_BG: ColorLike = "#293f21"
BUY_BUTTON_PRESSED_BG: ColorLike = "#181c19"

DARK_BG: ColorLike = "#171516"

TEXT_COLOR_NORMAL: ColorLike = "white"

FONT_NORMAL: str = "Oleaguid"
FONT_SIZE_NORMAL: int = 36
FONT_SIZE_HEADER: int = 48
FONT_SIZE_VERYBIG: int = 72


ELEMENT_OUTER_PADDING: int = 8
BUTTON_SIZE: int = 70


ASSET_PATH: Path = Path("src", "assets")
MAPS_PATH: Path = Path("src", "assets", "maps")
FONTS_PATH: Path = Path("src", "assets", "fonts")
