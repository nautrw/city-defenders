from pygame.typing import SequenceLike
from dataclasses import dataclass
from typing import Any

import pygame


# Dataclasses with frozen=True are immutable
@dataclass(frozen=True)
class DisplayConfig:
    screen_width: int = 360
    screen_height: int = 240
    flags: int = pygame.SCALED
    fps: int = 120


@dataclass(frozen=True)
class TilesConfig:
    tile_width: int = 32
    tile_height: int = 32
    ground_tiles_layer_name: str = "ground"
    path_tiles_layer_name: str = "path_tiles"
    enemy_path_layer_name: str = "path_polygon"

@dataclass(frozen=True)
class ColorsConfig:
    low_health_color: SequenceLike[int] | str | int = (255, 0, 0)
    max_health_color: SequenceLike[int] | str | int = (0, 255, 0)

DISPLAY = DisplayConfig()
TILES = TilesConfig()
COLORS = ColorsConfig()
