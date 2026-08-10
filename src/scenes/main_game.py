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
        self._grid = Grid(10, 10, 100, 100)
        self._grid_offset = pygame.Vector2()
        self._dragging_grid = False

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mx, my = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE:
                    if self._grid.rect.collidepoint(mx, my):
                        self._dragging_grid = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_MIDDLE:
                    self._dragging_grid = False
            elif event.type == pygame.MOUSEMOTION:
                if self._dragging_grid:
                    self._grid.rect.topleft = mx, my

    def update(self, delta_time: int | float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self._grid.draw(surface)
