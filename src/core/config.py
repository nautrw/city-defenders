from typing import Any
from enum import Enum, auto
from dataclasses import dataclass

# Dataclasses with frozen=True are immutable
@dataclass(frozen=True)
class DisplayConfig:
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 720
    FPS: int = 120

@dataclass(frozen=True)
class TilesConfig:
    # The full tile sprite dimensions
    FULL_TILE_WIDTH: int = 26
    FULL_TILE_HEIGHT: int = 29
    # The top faces of the tiles; must be used for rendering offsets and such
    TILE_TOP_WIDTH: int = 12
    TILE_TOP_HEIGHT: int = 6

class ConfigurationManager:
    """Manages configuration globals by domain accross the game."""

    def __init__(self) -> None:
        self.display_config = DisplayConfig()
        self.tiles_config = TilesConfig()

    def __getattr__(self, name: str) -> Any:
        domains: tuple = (
            self.display_config,
            self.tiles_config,
        )

        # Treats all attributes from all domains as globals
        # (ex. allows Config.FPS when normally it'd be
        #  Config.DisplayConfig.FPS)
        for domain in domains:
            if hasattr(domain, name):
                return getattr(domain, name)
        
        raise AttributeError(f'{name} config key does not exist')

config = ConfigurationManager()
