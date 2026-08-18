import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from src.core.utils import split_tileset
from typing import TYPE_CHECKING
from src.core.map import GameMap

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class MainGameScene(Scene):
    def __init__(self, game: GameApp, map_data: list[list[int]]):
        super().__init__(game)

        tileset = pygame.image.load("src/assets/tiles/tileset.png").convert_alpha()
        self.tiles = split_tileset(tileset, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.map_data = map_data
        self.map = GameMap(self.tiles, map_data)

        self.dragging_map = False
        self.camera_offset = pygame.Vector2(0, 0)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mx, my = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE:
                    if self.map.rect.collidepoint(mx, my):
                        self.dragging_map = True
                        self.camera_offset = pygame.Vector2(mx - self.map.rect.x, my - self.map.rect.y)
                if event.button == pygame.BUTTON_LEFT:
                    print(self.map.screen_to_map_coord(mx, my))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_MIDDLE:
                    if self.map.rect.collidepoint(mx, my):
                        self.dragging_map = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_map:
                    new_offset = pygame.Vector2(
                            mx - self.camera_offset.x,
                            my - self.camera_offset.y
                        )

                    # lowk idk why u have to multiply the width by 1/3 but ig it works
                    if ((-self.game.screen.width * 1/3) < new_offset.x < 0) and (-self.game.screen.height < new_offset.y < 0):
                        self.map.rect.topleft = new_offset

    def update(self, delta_time: int | float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.map.draw(surface)
