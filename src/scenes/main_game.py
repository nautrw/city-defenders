from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import load_asset, split_tileset
from src.entities.enemies.slime import Slime
from src.entities.turrets.crossbow import CrossbowTurret
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.container import ElementContainer

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp  # noqa: TC004

class UIStates(Enum):
    COLLAPSED = auto()
    TOWER_MENU = auto()

class MainGameSceneStates(Enum):
    NORMAL = auto()
    PLACING_TURRET = auto()

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
        # crossbow = CrossbowTurret(150, 100)
        # self.turrets_group.add(crossbow)

        self.projectiles_group = pygame.sprite.Group()

        self.dragging_map = False
        self.camera_offset = pygame.Vector2(0, 0)

        self.paused = False
        self.draw_turret_radiuses = False

        self.state: MainGameSceneStates = MainGameSceneStates.NORMAL
        self.turret_to_place = None
        self.can_place_turret = False

        self.ui_elements = []
        self.ui_state = UIStates.COLLAPSED
        self.refresh_ui()

    def refresh_ui(self) -> None:
        self.ui_elements = []

        if self.ui_state == UIStates.COLLAPSED:
            build_icon = load_asset("build_icon")
            build_button = Button("build_towers", 338, 2, 20, 20, image=build_icon)

            self.ui_elements.append(build_button)
        elif self.ui_state == UIStates.TOWER_MENU:
            container_width = 100
            container_height = self.game.screen.height
            tower_menu_cotnainer = ElementContainer("tower_menu", self.game.screen.width - container_width, 0, container_width, container_height, bg_color="black")

            crossbow_turret_icon = pygame.transform.scale(load_asset("crossbow"), (16, 16))
            tower_menu_cotnainer.elements.append(Button("crossbow_turret_button", 2, 2, 20, 20, image=crossbow_turret_icon))

            self.ui_elements.append(tower_menu_cotnainer)

            close_icon = load_asset("close_icon")
            self.ui_elements.append(Button("tower_menu_close_button", 238, 2, 20, 20, image=close_icon))

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mouse_x, mouse_y = pygame.mouse.get_pos()

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
                    if event.button == pygame.BUTTON_LEFT: # noqa: SIM102
                        if self.turret_to_place and self.can_place_turret:
                            self.turrets_group.add(self.turret_to_place)
                            self.state = MainGameSceneStates.NORMAL
                            self.turret_to_place = None

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_MIDDLE:  # noqa: SIM102
                        if self.map.rect.collidepoint(mouse_x, mouse_y):
                            self.dragging_map = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_map:
                        new_offset = pygame.Vector2(
                            mouse_x - self.camera_offset.x, mouse_y - self.camera_offset.y
                        )

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

                    # turret must be moved alongside the map
                    if self.turret_to_place:
                        new_coord = self.map.screen_to_map_coord(mouse_x, mouse_y)
                        self.turret_to_place.move_center(*new_coord)
                        self.can_place_turret = not pygame.sprite.spritecollide(self.turret_to_place, self.map.path_tiles, False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.draw_turret_radiuses = not self.draw_turret_radiuses
            elif event.type == CUSTOM_BUTTON_CLICKED:
                if event.button.id == "build_towers":
                    self.ui_state = UIStates.TOWER_MENU
                    self.refresh_ui()
                elif event.button.id == "tower_menu_close_button":
                    self.ui_state = UIStates.COLLAPSED
                    self.refresh_ui()
                if event.button.id == "crossbow_turret_button":
                    self.state = MainGameSceneStates.PLACING_TURRET
                    self.turret_to_place = CrossbowTurret(mouse_x, mouse_y)

    def update(self, delta_time: float) -> None:
        if not self.paused:
            self.enemies_group.update(delta_time)
            self.turrets_group.update(
                delta_time, self.enemies_group, self.projectiles_group
            )
            self.projectiles_group.update(delta_time, self.enemies_group)

            for element in self.ui_elements:
                element.update(delta_time, pygame.mouse.get_pos())

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

        if self.turret_to_place:
            overlay_color = (0, 255, 0, 255) if self.can_place_turret else (255, 0, 0, 255) 
            self.turret_to_place.draw(self.map.image, True, overlay_color=overlay_color)

        for element in self.ui_elements:
            element.draw(surface)
