from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.camera import Camera
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.entities.enemies.enemy import ENEMY_KILLED
from src.entities.entity_data import ENEMIES
from src.scenes.main_game_gui_manager import MainGameSceneGUIManager, UIStates

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class MainGameSceneStates(Enum):
    NORMAL = auto()
    SPAWNING_ENEMIES = auto()


class MainGameScene(Scene):
    def __init__(self, game: "GameApp", map: GameMap, map_data: dict):
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

        self.enemies_group = pygame.sprite.Group()

        self.turrets_group = pygame.sprite.Group()

        self.projectiles_group = pygame.sprite.Group()

        self.paused = False
        self.draw_turret_radiuses = False

        self.coins = map_data["initial_balance"]

        self.state: MainGameSceneStates = MainGameSceneStates.NORMAL
        self.turret_to_place = None
        self.can_place_turret = False
        self.selected_tower = None

        self.waves = map_data["waves"]
        self.wave = 0
        self.waves_interval = map_data["waves_interval"]
        self.wave_interval_dt_count = 0

        self.wave_enemy_spawn_index = 0
        self.enemy_spawn_interval = 0.5
        self.enemy_spawn_interval_dt_count = 0

        self.gui_manager = MainGameSceneGUIManager(self)

    def place_selected_tower(self):
        self.turrets_group.add(self.turret_to_place)
        self.gui_manager.switch_state(UIStates.TOWER_PICKER_MENU)
        self.coins -= self.turret_to_place.cost  # ty:ignore[unresolved-attribute]

        # reset everything
        self.can_place_turret = False
        self.turret_to_place = None
        self.gui_manager.switch_state(UIStates.COLLAPSED)
        self.gui_manager.refresh()

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_world_coord = self.camera.viewport_to_world(mouse_x, mouse_y)

            # left ctrl key
            meta_pressed = pygame.key.get_mods() == pygame.KMOD_LCTRL

            if not any(
                element.rect.collidepoint(mouse_x, mouse_y)
                for element in self.gui_manager.elements
            ):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT and not meta_pressed:
                        if self.turret_to_place and self.can_place_turret:
                            self.place_selected_tower()
                        else:
                            for turret in self.turrets_group:
                                if turret.rect.collidepoint(mouse_world_coord):
                                    self.selected_tower = turret
                                    self.gui_manager.switch_state(
                                        UIStates.TOWER_SELECTED
                                    )
                elif event.type == pygame.MOUSEMOTION:
                    if (event.buttons[1]) or (meta_pressed and event.buttons[0]):
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
                            self.turret_to_place, self.map.blocked_tiles, False
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
            self.wave_interval_dt_count += delta_time
            self.enemy_spawn_interval_dt_count += delta_time

            if self.wave_interval_dt_count >= self.waves_interval:
                self.wave += 1
                self.wave_interval_dt_count = 0
                self.wave_enemy_spawn_index = 0

            if (
                self.enemy_spawn_interval_dt_count >= self.enemy_spawn_interval
                and self.wave_enemy_spawn_index < len(self.waves[self.wave])
            ):
                enemy_id = self.waves[self.wave][self.wave_enemy_spawn_index]
                enemy = ENEMIES[enemy_id](self.map.path)
                self.enemies_group.add(enemy)
                self.enemy_spawn_interval_dt_count = 0
                self.wave_enemy_spawn_index += 1

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
