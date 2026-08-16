import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from src.core.map import Map
from src.core.utils import split_tileset
from typing import TYPE_CHECKING

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class MainGameScene(Scene):
    def __init__(self, game: GameApp):
        super().__init__(game)
        data = [
         [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8, 11, 11, 11, 11, 11, 11,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8, 11,  8,  8,  8,  8, 11,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8, 11,  8,  8,  8,  8, 11,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8, 11,  8,  8,  8,  8, 11,  8,  8,  8, 11,  8,  8, ],
         [  8,  8,  8, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,  8,  8, ],
         [  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8,  8,  8,  8,  8, ],
         [  8,  8,  8, 11, 11, 11,  8,  8, 11,  8,  8,  8,  8,  8,  8, ],
         [  8,  8,  8, 11,  8, 11,  8,  8, 11,  8,  8,  8,  8,  8,  8, ],
         [  8,  8,  8, 11, 11, 11, 11, 11, 11,  8,  8,  8,  8,  8,  8, ],
         [  8,  8,  8,  8,  8, 11,  8,  8,  8,  8,  8,  8,  8,  8,  8, ],
         [  8,  8,  8,  8,  8, 11,  8,  8,  8,  8,  8,  8,  8,  8,  8, ],
        ]

        tileset = pygame.image.load("src/assets/tiles/tileset.png").convert()
        tiles = split_tileset(tileset, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.map = Map(tiles, data)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mx, my = pygame.mouse.get_pos()

    def update(self, delta_time: int | float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.map.draw(self.game.screen)
