from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import load_scaled_asset
from src.entities.enemies.slime import Slime
from src.entities.turrets.crossbow import CrossbowTurret
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.container import ElementContainer
from src.gui.gui_manager import GUIManager
from src.gui.text import Text, TextPlacementModes

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp  # noqa: TC004


class UIStates(Enum):
    COLLAPSED = auto()
    TOWER_MENU = auto()
    PLACING_TURRET = auto()
    TURRET_SELECTED = auto()


class MainGameSceneStates(Enum):
    NORMAL = auto()
    PLACING_TURRET = auto()


class MainGameSceneGUIManager(GUIManager):
    def __init__(self, scene: Scene) -> None:
        default_state = UIStates.COLLAPSED

        super().__init__(scene, default_state)

        self.button_external_padding = 8
        self.button_side_length = 70

        self.refresh()

    def refresh(self) -> None:
        self.elements = []

        if self.state == UIStates.COLLAPSED:
            build_icon = load_scaled_asset("build_icon")
            build_button = Button(
                "build_towers",
                (self.scene.game.screen.width - self.button_side_length)
                - self.button_external_padding,
                self.button_external_padding,
                self.button_side_length,
                self.button_side_length,
                image=build_icon,
            )

            self.elements.append(build_button)
        elif self.state == UIStates.TOWER_MENU:
            container_width = 500
            container_height = self.scene.game.screen.height

            tower_menu_container = ElementContainer(
                "tower_menu",
                self.scene.game.screen.width - container_width,
                0,
                container_width,
                container_height,
            )

            crossbow_turret_icon = pygame.transform.scale(
                load_scaled_asset("crossbow"), (64, 64)
            )
            tower_menu_container.elements.append(
                Button(
                    "crossbow_turret_button",
                    self.button_external_padding,
                    self.button_external_padding,
                    self.button_side_length,
                    self.button_side_length,
                    image=crossbow_turret_icon,
                )
            )

            self.elements.append(tower_menu_container)

            close_icon = load_scaled_asset("close_icon")
            self.elements.append(
                Button(
                    "tower_menu_close_button",
                    (self.scene.game.screen.width - container_width)
                    - (self.button_side_length + self.button_external_padding),
                    self.button_external_padding,
                    self.button_side_length,
                    self.button_side_length,
                    image=close_icon,
                )
            )
        elif self.state == UIStates.PLACING_TURRET:
            close_icon = load_scaled_asset("close_icon")
            discard_button = Button(
                "discard_turret_button",
                (self.scene.game.screen.width - self.button_side_length)
                - self.button_external_padding,
                self.button_external_padding,
                self.button_side_length,
                self.button_side_length,
                image=close_icon,
            )
            self.elements.append(discard_button)
        elif self.state == UIStates.TURRET_SELECTED:
            container_width = 100
            container_height = self.scene.game.screen.height
            selected_tower_menu = ElementContainer(
                "selected_tower_menu",
                self.scene.game.screen.width - container_width,
                0,
                container_width,
                container_height,
            )

            tower_name = Text(
                self.scene.selected_turret.display_name,  # ty:ignore[unresolved-attribute]
                container_width // 2,
                10,
                placement_mode=TextPlacementModes.CENTER,
            )

            selected_tower_menu.elements.append(tower_name)

            self.elements.append(selected_tower_menu)

            close_icon = load_scaled_asset("close_icon")
            self.elements.append(
                Button(
                    "selected_tower_menu_close_button", 238, 2, 20, 20, image=close_icon
                )
            )

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            if event.button.id == "build_towers":
                self.switch_state(UIStates.TOWER_MENU)
            elif event.button.id.endswith("_close_button"):
                # elif event.button.id == "tower_menu_close_button":
                # elif event.button.id == "selected_tower_menu_close_button":
                self.switch_state(UIStates.COLLAPSED)
            elif event.button.id == "discard_turret_button":
                self.switch_state(UIStates.TOWER_MENU)
                self.scene.turret_to_place = None  # ty: ignore[unresolved-attribute]
            elif event.button.id == "crossbow_turret_button":
                self.switch_state(UIStates.PLACING_TURRET)

                self.scene.state = (  # ty:ignore[unresolved-attribute]
                    MainGameSceneStates.PLACING_TURRET
                )
                self.scene.turret_to_place = CrossbowTurret(  # ty:ignore[unresolved-attribute]
                    *self.scene.screen_to_world_coord(  # ty:ignore[unresolved-attribute]
                        *pygame.mouse.get_pos()
                    )
                )


class MainGameScene(Scene):
    def __init__(self, game: GameApp, map: GameMap):
        super().__init__(game)

        self.map = map
        self.game_surface = pygame.Surface(self.map.image.size)
        self.game_surface_rect = self.game_surface.get_rect()
        self.scaled_game_surface_size = (
            self.game_surface_rect.width * Config.MAP_SCALE_FACTOR,
            self.game_surface_rect.height * Config.MAP_SCALE_FACTOR,
        )

        self.dragging_map = False
        self.drag_start_mouse = pygame.Vector2()
        self.drag_start_camera = pygame.Vector2()
        self.camera_offset = pygame.Vector2(0, 0)

        self.enemies_group = pygame.sprite.Group()
        slime = Slime(self.map.enemies_path)
        self.enemies_group.add(slime)

        self.turrets_group = pygame.sprite.Group()

        self.projectiles_group = pygame.sprite.Group()

        self.paused = False
        self.draw_turret_radiuses = False

        self.state: MainGameSceneStates = MainGameSceneStates.NORMAL
        self.turret_to_place = None
        self.can_place_turret = False
        self.selected_turret = None

        self.gui_manager = MainGameSceneGUIManager(self)

    def screen_to_world_coord(
        self, screen_x: float, screen_y: float
    ) -> tuple[float, float]:
        screen_pos = pygame.Vector2(screen_x, screen_y)

        world_coord = (screen_pos / Config.MAP_SCALE_FACTOR) + self.camera_offset
        return (world_coord.x, world_coord.y)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_world_coord = self.screen_to_world_coord(mouse_x, mouse_y)

            if not any(
                element.rect.collidepoint(mouse_x, mouse_y)
                for element in self.gui_manager.elements
            ):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_MIDDLE:  # noqa: SIM102
                        if self.game_surface_rect.collidepoint(mouse_world_coord):
                            self.dragging_map = True
                    if event.button == pygame.BUTTON_LEFT:
                        if self.state == MainGameSceneStates.PLACING_TURRET:
                            if self.turret_to_place and self.can_place_turret:
                                self.turrets_group.add(self.turret_to_place)
                                self.state = MainGameSceneStates.NORMAL
                                self.gui_manager.switch_state(UIStates.TOWER_MENU)
                                self.turret_to_place = None
                                self.can_place_turret = False  # reset
                        elif self.state == MainGameSceneStates.NORMAL:
                            for turret in self.turrets_group:
                                if turret.rect.collidepoint(mouse_world_coord):
                                    self.selected_turret = turret
                                    self.gui_manager.switch_state(
                                        UIStates.TURRET_SELECTED
                                    )
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_MIDDLE:
                        self.dragging_map = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_map:
                        mouse_movement = (
                            pygame.Vector2(event.rel) / Config.MAP_SCALE_FACTOR
                        )
                        new_offset = self.camera_offset - mouse_movement

                        if (
                            0
                            < new_offset.x
                            < self.game_surface_rect.width
                            - (self.game.screen.width / Config.MAP_SCALE_FACTOR)
                        ):
                            self.camera_offset.x = new_offset.x

                        if (
                            0
                            < new_offset.y
                            < self.game_surface.height
                            - (self.game.screen.height / Config.MAP_SCALE_FACTOR)
                        ):
                            self.camera_offset.y = new_offset.y

                    # turret must be moved alongside the map
                    if self.turret_to_place:
                        new_coord = pygame.Vector2(mouse_world_coord)
                        self.turret_to_place.move_center(*new_coord)
                        self.can_place_turret = not pygame.sprite.spritecollide(
                            self.turret_to_place, self.map.path_tiles, False
                        ) and not pygame.sprite.spritecollide(
                            self.turret_to_place, self.turrets_group, False
                        )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.draw_turret_radiuses = not self.draw_turret_radiuses

            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        if not self.paused:
            self.enemies_group.update(delta_time)
            self.turrets_group.update(
                delta_time, self.enemies_group, self.projectiles_group
            )
            self.projectiles_group.update(delta_time, self.enemies_group)

            self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())

    def render(self, surface: pygame.Surface) -> None:
        surface.fill("black")

        self.map.draw(self.game_surface)

        # pygame.sprite.Group.draw() only blits the sprite image,
        # but the enemies have a health bar that is drawn in their .draw()
        # method, so I call it normally (the draw function does little more)
        # than that
        for enemy in self.enemies_group:
            enemy.draw(self.game_surface)

        for turret in self.turrets_group:
            turret.draw(self.game_surface, self.draw_turret_radiuses)

        for projectile in self.projectiles_group:
            projectile.draw(self.game_surface)

        if self.turret_to_place:
            overlay_color = (
                (0, 255, 0, 255) if self.can_place_turret else (255, 0, 0, 255)
            )
            self.turret_to_place.draw(
                self.game_surface, True, overlay_color=overlay_color
            )

        scaled_game_surface = pygame.transform.scale(
            self.game_surface, self.scaled_game_surface_size
        )
        # surface.blit(scaled_game_surface, scaled_game_surface.get_rect())

        camera_view = pygame.Rect(
            self.camera_offset.x * Config.MAP_SCALE_FACTOR,
            self.camera_offset.y * Config.MAP_SCALE_FACTOR,
            self.game.screen.width,
            self.game.screen.height,
        )
        surface.blit(scaled_game_surface, (0, 0), camera_view)

        self.gui_manager.render_elements(surface)
