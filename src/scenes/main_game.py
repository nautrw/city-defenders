from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import load_asset, split_tileset
from src.entities.enemies.slime import Slime
from src.entities.turrets.crossbow import CrossbowTurret
from src.gui.button import Button, CUSTOM_BUTTON_CLICKED

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp  # noqa: TC004


class MainGameScene(Scene):
    def __init__(self, game: GameApp, map: GameMap):
        super().__init__(game)

        tileset = load_asset("tileset")
        self.tiles = split_tileset(tileset, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.map = map

        self.enemies_group = pygame.sprite.Group()
        slime = Slime(self.map.enemies_path)
        self.enemies_group.add(slime)

        self.turrets_group = pygame.sprite.Group()
        crossbow = CrossbowTurret(150, 100)
        self.turrets_group.add(crossbow)

        self.projectiles_group = pygame.sprite.Group()

        self.dragging_map = False
        self.camera_offset = pygame.Vector2(0, 0)

        self.paused = False
        self.draw_turret_radiuses = False

        build_icon = load_asset("build_icon")

        button = Button(5, 215, 20, 20, image=build_icon)
        self.ui_elements = [button]

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mx, my = pygame.mouse.get_pos()

            self.handle_map_dragging(event, mx, my)
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.draw_turret_radiuses = not self.draw_turret_radiuses
            elif event.type == CUSTOM_BUTTON_CLICKED:
                print(event.button.rect)

    def handle_map_dragging(self, event: pygame.Event, mouse_x: int, mouse_y: int):
        if not any(
            element.rect.collidepoint(mouse_x, mouse_y) for element in self.ui_elements
        ):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE:  # noqa: SIM102
                    if self.map.rect.collidepoint(mouse_x, mouse_y):
                        self.dragging_map = True
                        self.camera_offset = pygame.Vector2(
                            mouse_x - self.map.rect.x, mouse_y - self.map.rect.y
                        )
                if event.button == pygame.BUTTON_LEFT:
                    print(self.map.screen_to_map_coord(mouse_x, mouse_y))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_MIDDLE:  # noqa: SIM102
                    if self.map.rect.collidepoint(mouse_x, mouse_y):
                        self.dragging_map = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_map:
                    new_offset = pygame.Vector2(
                        mouse_x - self.camera_offset.x, mouse_y - self.camera_offset.y
                    )

                    #                     print(f"""
                    # new offset: {new_offset}
                    # screen size: {self.game.screen.get_size()}
                    # map size: {self.map.rect.size}""")
                    if (
                        0
                        < -new_offset.x
                        < (self.map.map_width - self.game.screen.width)
                    ):
                        self.map.rect.x = new_offset.x

                    if (
                        0
                        < -new_offset.y
                        < (self.map.map_height - self.game.screen.height)
                    ):
                        self.map.rect.y = new_offset.y

                        # self.map.rect.topleft = new_offset

    def update(self, delta_time: float) -> None:
        if not self.paused:
            self.enemies_group.update(delta_time)
            self.turrets_group.update(
                delta_time, self.enemies_group, self.projectiles_group
            )
            self.projectiles_group.update(delta_time, self.enemies_group)

            for element in self.ui_elements:
                element.update(delta_time)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.map.draw(surface)

        # pygame.sprite.Group.draw() only blits the sprite image,
        # but the enemies have a health bar that is drawn in their .draw()
        # method, so I call it normally (the draw function does little more)
        # than that
        for enemy in self.enemies_group:
            enemy.draw(self.map.image)

        for turret in self.turrets_group:
            turret.draw(self.map.image, self.draw_turret_radiuses)

        for projectile in self.projectiles_group:
            projectile.draw(self.map.image)

        for element in self.ui_elements:
            element.draw(surface)
