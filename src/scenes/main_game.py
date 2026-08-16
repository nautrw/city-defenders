import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from src.core.utils import split_tileset
from typing import TYPE_CHECKING

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class MainGameScene(Scene):
    def __init__(self, game: GameApp, map_data: list[list[int]]):
        super().__init__(game)

        self.tileset_img = pygame.image.load("src/assets/tiles/tileset.png").convert()
        self.tileset = split_tileset(self.tileset_img, Config.TILE_WIDTH, Config.TILE_HEIGHT)

        self.tiles_width = len(map_data[0])
        self.tiles_height = len(map_data)

        self.map_width = self.tiles_width * Config.TILE_WIDTH
        self.map_height = self.tiles_height * Config.TILE_HEIGHT

        self.map_data = map_data
        self.map_surf = pygame.Surface((self.map_width, self.map_height))
        self.map_rect = self.map_surf.get_rect(topleft=(0,0))

        self.dragging_map = False
        self.map_offset = pygame.Vector2()

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mx, my = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE:
                    if self.map_rect.collidepoint(mx, my):
                        self.dragging_map = True
                        self.map_offset = pygame.Vector2(mx - self.map_rect.x, my - self.map_rect.y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_MIDDLE:
                    if self.map_rect.collidepoint(mx, my):
                        self.dragging_map = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_map:
                    self.map_rect.topleft = pygame.Vector2(
                        mx - self.map_offset.x,
                        my - self.map_offset.y
                    )

    def update(self, delta_time: int | float) -> None:
        pass
    
    def _draw_map(self) -> None:
        for y, row in enumerate(self.map_data):
            for x, tile_id in enumerate(row):
                self.map_surf.blit(self.tileset[tile_id], (x * Config.TILE_WIDTH, y * Config.TILE_HEIGHT))

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self._draw_map()
        surface.blit(self.map_surf, self.map_rect)
