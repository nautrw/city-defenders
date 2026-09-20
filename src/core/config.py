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
GUI_ICON_SIZE: int = 64

GROUND_TILES_LAYER_NAME: str = "ground"
BLOCKED_TILES_LAYER_NAME: str = "blocked"
ENEMY_PATH_LAYER_NAME: str = "path"


DARK_RED: ColorLike = "#771a10"
BRIGHT_GREEN: ColorLike = "#61a53f"
TOWER_RADIUS_COLOR: ColorLike = (0, 0, 0, 75)

BUTTON_NORMAL_BG: ColorLike = "#17151640"
BUTTON_HOVERED_BG: ColorLike = "#171516BF"
BUTTON_PRESSED_BG: ColorLike = "#171516E1"

GREEN_BUTTON_NORMAL_BG: ColorLike = "#477238BF"
GREEN_BUTTON_HOVERED_BG: ColorLike = "#293f21BF"
GREEN_BUTTON_PRESSED_BG: ColorLike = "#181c19BF"

RED_BUTTON_NORMAL_BG: ColorLike = "#7a2b24BF"
RED_BUTTON_HOVERED_BG: ColorLike = "#541d19BF"
RED_BUTTON_PRESSED_BG: ColorLike = "#321412BF"

DARK_BG: ColorLike = "#17151650"

TEXT_COLOR_NORMAL: ColorLike = "white"

FONT_NORMAL: str = "Oleaguid"
FONT_SIZE_SMALL: int = 24
FONT_SIZE_NORMAL: int = 36
FONT_SIZE_HEADER: int = 48
FONT_SIZE_BIGGER: int = 60
FONT_SIZE_VERYBIG: int = 72
FONT_SIZE_HUGE: int = 84


ELEMENT_OUTER_PADDING: int = 8
BUTTON_SIZE: int = 70


ASSET_PATH: Path = Path("src", "assets")
MAPS_PATH: Path = Path("src", "maps")
FONTS_PATH: Path = Path("src", "assets", "fonts")
