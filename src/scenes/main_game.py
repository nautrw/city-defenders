from typing import TYPE_CHECKING

import pygame

from src.core.config import config as Config
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import split_tileset

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp  # noqa: TC004


class MainGameScene(Scene):
    def __init__(self, game: GameApp, map: GameMap):
        super().__init__(game)

        tileset = pygame.image.load("src/assets/tiles/tileset.png").convert_alpha()
        self.tiles = split_tileset(tileset, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.map = map

        self.dragging_map = False
        self.camera_offset = pygame.Vector2(0, 0)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mx, my = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE: # noqa: SIM102
                    if self.map.rect.collidepoint(mx, my):
                        self.dragging_map = True
                        self.camera_offset = pygame.Vector2(
                            mx - self.map.rect.x, my - self.map.rect.y
                        )
                if event.button == pygame.BUTTON_LEFT:
                    print(self.map.screen_to_map_coord(mx, my))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_MIDDLE: # noqa: SIM102
                    if self.map.rect.collidepoint(mx, my):
                        self.dragging_map = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_map:
                    new_offset = pygame.Vector2(
                        mx - self.camera_offset.x, my - self.camera_offset.y
                    )

                    #                     print(f"""
                    # new offset: {new_offset}
                    # screen size: {self.game.screen.get_size()}
                    # map size: {self.map.rect.size}""")
                    if (
                        0
                        < -new_offset.x
                        < (self.map.map_width - self.game.screen.width)
                    ) and (
                        0
                        < -new_offset.y
                        < (self.map.map_height - self.game.screen.height)
                    ):
                        self.map.rect.topleft = new_offset

                    # self.map.rect.topleft = new_offset

    def update(self, delta_time: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.map.draw(surface)
