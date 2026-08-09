import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from typing import TYPE_CHECKING

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class MainGameScene(Scene):
    def __init__(self, game: GameApp):
        super().__init__(game)
        self.grass_img = pygame.image.load('src/assets/tiles/forest_grass.png')
        self.dirt_img = pygame.image.load('src/assets/tiles/dirt.png')

    def handle_events(self, events: list[pygame.Event]) -> None:
        pass

    def update(self, delta_time: int | float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        for y, row in enumerate(range(5)):
            for x, tile in enumerate(range(5)):
                w = Config.TILE_TOP_WIDTH
                h = Config.TILE_TOP_HEIGHT
                surface.blit(self.grass_img, (150 + x * w - y * w, 100 + x * h + y * h))
