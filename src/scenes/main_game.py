from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.camera import Camera
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import load_asset, load_scaled_asset
from src.entities.enemies.enemy import ENEMY_KILLED
from src.entities.enemies.slime import Slime
from src.entities.turrets.crossbow import CrossbowTurret
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.container import ElementContainer
from src.gui.gui_manager import GUIManager
from src.gui.icon import Icon
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp  # noqa: TC004


class UIStates(Enum):
    COLLAPSED = auto()
    TOWER_PICKER_MENU = auto()
    PLACING_TURRET = auto()
    TOWER_SELECTED = auto()


class MainGameSceneStates(Enum):
    NORMAL = auto()
    PLACING_TURRET = auto()


class MainGameSceneGUIManager(GUIManager):
    def __init__(self, scene: Scene) -> None:
        default_state = UIStates.COLLAPSED

        super().__init__(scene, default_state)

        self.refresh()

    def refresh(self) -> None:
        self.elements = []

        # COINS DISPLAY ALWAYS SHOWN
        coin_icon_size = 48

        coins_text = Text(
            "coins_text",
            str(self.scene.coins),  # ty:ignore[unresolved-attribute]
            Config.ELEMENT_OUTER_PADDING
            + coin_icon_size
            + Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            Config.FONT_SIZE_HEADER,
        )

        coin_display_container_width = (
            (Config.ELEMENT_OUTER_PADDING * 3) + coin_icon_size + coins_text.rect.width
        )
        coins_display_container_height = (
            Config.ELEMENT_OUTER_PADDING * 2
        ) + coin_icon_size

        coin_icon = Icon(
            "coin_icon",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            coin_icon_size,
            coin_icon_size,
            load_asset("coin"),
            RectAnchorMode.TOPLEFT,
        )

        coin_display_container = ElementContainer(
            "coin_display_container",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            coin_display_container_width,
            coins_display_container_height,
        )

        coin_display_container.add_element(coin_icon)
        coin_display_container.add_element(coins_text)

        self.elements.append(coin_display_container)

        if self.state == UIStates.COLLAPSED:
            build_icon = load_scaled_asset("build_icon")
            build_button = Button(
                "tower_picker_menu_button",
                (
                    Config.SCREEN_WIDTH
                    - Config.BUTTON_SIZE
                    - Config.ELEMENT_OUTER_PADDING
                ),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                image=build_icon,
                anchor=RectAnchorMode.TOPRIGHT,
            )
            self.elements.append(build_button)
        elif self.state == UIStates.TOWER_PICKER_MENU:
            container_width = 500

            tower_picker_container = ElementContainer(
                "tower_picker_menu",
                (Config.SCREEN_WIDTH - container_width),
                0,
                container_width,
                Config.SCREEN_HEIGHT,
            )

            close_icon = load_scaled_asset("close_icon")
            tower_picker_close_button = Button(
                "tower_picker_close_button",
                ((Config.SCREEN_WIDTH - container_width) - Config.BUTTON_SIZE)
                - Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                image=close_icon,
            )

            crossbow_turret_icon = load_scaled_asset("crossbow")
            tower_picker_container.add_element(
                Button(
                    "build_crossbow_turret_button",
                    Config.ELEMENT_OUTER_PADDING,
                    Config.ELEMENT_OUTER_PADDING,
                    Config.BUTTON_SIZE,
                    Config.BUTTON_SIZE,
                    image=crossbow_turret_icon,
                )
            )

            self.elements.append(tower_picker_close_button)
            self.elements.append(tower_picker_container)
        elif self.state == UIStates.PLACING_TURRET:
            close_icon = load_scaled_asset("close_icon")
            tower_discard_button = Button(
                "tower_discard_button",
                (
                    Config.SCREEN_WIDTH
                    - Config.BUTTON_SIZE
                    - Config.ELEMENT_OUTER_PADDING
                ),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                image=close_icon,
                anchor=RectAnchorMode.TOPRIGHT,
            )

            self.elements.append(tower_discard_button)
        elif self.state == UIStates.TOWER_SELECTED:
            container_width = 500

            selected_tower_menu = ElementContainer(
                "selected_tower_menu",
                Config.SCREEN_WIDTH - container_width,
                0,
                container_width,
                Config.SCREEN_HEIGHT,
            )

            tower_name = Text(
                "selected_tower_display_name",
                self.scene.selected_tower.display_name,  # ty:ignore[unresolved-attribute]
                container_width // 2,
                Config.ELEMENT_OUTER_PADDING,
                anchor=RectAnchorMode.MIDTOP,
                size=Config.FONT_SIZE_HEADER,
            )

            tower_description = Text(
                "selected_tower_description",
                self.scene.selected_tower.description,  # ty:ignore[unresolved-attribute]
                Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING + tower_name.rect.height,
                wrap_length=container_width,
            )

            selected_tower_menu.add_element(tower_name)
            selected_tower_menu.add_element(tower_description)

            self.elements.append(selected_tower_menu)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            if event.button.id == "tower_picker_menu_button":
                self.switch_state(UIStates.TOWER_PICKER_MENU)
            elif event.button.id == "tower_picker_close_button":
                self.switch_state(UIStates.COLLAPSED)
            elif event.button.id == "build_crossbow_turret_button":
                self.switch_state(UIStates.PLACING_TURRET)

                self.scene.state = MainGameSceneStates.PLACING_TURRET  # ty:ignore[unresolved-attribute]
                self.scene.turret_to_place = CrossbowTurret(  # ty:ignore[unresolved-attribute]
                    *self.scene.camera.viewport_to_world(*pygame.mouse.get_pos())  # ty:ignore[unresolved-attribute]
                )
            elif event.button.id == "tower_discard_button":
                self.switch_state(UIStates.TOWER_PICKER_MENU)
                self.scene.state = MainGameSceneStates.NORMAL  # ty:ignore[unresolved-attribute]
                self.scene.turret_to_place = None  # ty:ignore[unresolved-attribute]


class MainGameScene(Scene):
    def __init__(self, game: GameApp, map: GameMap, initial_coins_balance: int):
        super().__init__(game)

        self.map = map
        self.game_surface = pygame.Surface(self.map.image.size)
        self.game_surface_rect = self.game_surface.get_frect()
        self.scaled_game_surface_size = (
            self.game_surface_rect.width * Config.MAP_SCALE_FACTOR,
            self.game_surface_rect.height * Config.MAP_SCALE_FACTOR,
        )

        self.camera = Camera(
            *self.game.screen.size,
            *self.game_surface_rect.size,
            Config.MAP_SCALE_FACTOR,
        )
        self.dragging_camera = False

        self.enemies_group = pygame.sprite.Group()
        slime = Slime(self.map.enemies_path)
        self.enemies_group.add(slime)

        self.turrets_group = pygame.sprite.Group()

        self.projectiles_group = pygame.sprite.Group()

        self.paused = False
        self.draw_turret_radiuses = False

        self.coins = initial_coins_balance

        self.state: MainGameSceneStates = MainGameSceneStates.NORMAL
        self.turret_to_place = None
        self.can_place_turret = False
        self.selected_tower = None

        self.gui_manager = MainGameSceneGUIManager(self)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_world_coord = self.camera.viewport_to_world(mouse_x, mouse_y)

            if not any(
                element.rect.collidepoint(mouse_x, mouse_y)
                for element in self.gui_manager.elements
            ):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_MIDDLE:  # noqa: SIM102
                        if self.game_surface_rect.collidepoint(mouse_world_coord):
                            self.dragging_camera = True
                    if event.button == pygame.BUTTON_LEFT:
                        if self.state == MainGameSceneStates.PLACING_TURRET:
                            if self.turret_to_place and self.can_place_turret:
                                self.turrets_group.add(self.turret_to_place)
                                self.state = MainGameSceneStates.NORMAL
                                self.gui_manager.switch_state(
                                    UIStates.TOWER_PICKER_MENU
                                )
                                self.turret_to_place = None
                                self.can_place_turret = False  # reset
                        elif self.state == MainGameSceneStates.NORMAL:
                            for turret in self.turrets_group:
                                if turret.rect.collidepoint(mouse_world_coord):
                                    self.selected_tower = turret
                                    self.gui_manager.switch_state(
                                        UIStates.TOWER_SELECTED
                                    )
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_MIDDLE:
                        self.dragging_camera = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_camera:
                        # event.rel is the amount of mouse movement
                        mouse_movement = (
                            pygame.Vector2(event.rel) / Config.MAP_SCALE_FACTOR
                        )

                        self.camera.move(int(mouse_movement.x), int(mouse_movement.y))

                    # turret must be moved alongside the map
                    if self.turret_to_place:
                        new_coord = pygame.Vector2(mouse_world_coord)
                        self.turret_to_place.move_center(*new_coord)
                        self.can_place_turret = not pygame.sprite.spritecollide(
                            self.turret_to_place, self.map.path_tiles, False
                        ) and not pygame.sprite.spritecollide(
                            self.turret_to_place, self.turrets_group, False
                        )
                elif event.type == ENEMY_KILLED:
                    self.coins += event.entity.coins_drop
                    self.gui_manager.get_element_by_id("coins_text").update_text(  # ty:ignore[unresolved-attribute]
                        self.coins
                    )
                    self.gui_manager.refresh()

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

        camera_view = pygame.Rect(
            self.camera.offset.x * Config.MAP_SCALE_FACTOR,
            self.camera.offset.y * Config.MAP_SCALE_FACTOR,
            self.game.screen.width,
            self.game.screen.height,
        )
        surface.blit(scaled_game_surface, (0, 0), camera_view)

        self.gui_manager.render_elements(surface)
