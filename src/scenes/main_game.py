import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from typing import TYPE_CHECKING
from src.core.grid import Grid

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class MainGameScene(Scene):
    def __init__(self, game: GameApp):
        super().__init__(game)
        self._grid = Grid(10, 10, 0, 0)

    def handle_events(self, events: list[pygame.Event]) -> None:
        pass

    def update(self, delta_time: int | float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self._grid.draw(surface)
